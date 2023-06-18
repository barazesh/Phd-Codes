import numpy as np
import pandas as pd
from Defector import Defector
from ElectricityTariff import ElectricityTariff
import Helper as hlp
from PV import PV
from Battery import Battery
from Prosumer import Prosumer
from RegularConsumer import RegularConsumer
from StandAlone import StandAloneSystem
from Utility import Utility
import matplotlib.pyplot as plt
import matplotlib as mpl


class Environment:
    def __init__(self, inputData) -> None:
        self.pv = PV(
            initialPrice=inputData["initialPVPrice"],
            normalReductionRate=inputData["normalPVCostReductionRate"],
            minimumPrice=inputData["minimumPVPrice"],
            effectiveLife=inputData["PVEffectiveLife"],
            hourlyEnergyOutput=inputData["PVHourlyEnergyOutput"],
        )

        self.battery = Battery(
            initialPrice=inputData["initialBatteryPrice"],
            normalReductionRate=inputData["normalBatteryCostReductionRate"],
            minimumPrice=inputData["minimumBatteryPrice"],
            effectiveLife=inputData["BatteryEffectiveLife"],
        )
        self.totalHousholds = [
            inputData["initialRegularConsumerNumber"]
            + inputData["initialProsumerNumber"]
        ]

        self.tariff = self.__CreateTariff(inputData)
        self.prosumers = self.__CreateProsumer(inputData)
        self.regularConsumers = self.__CreateRegularConsumer(inputData)
        self.defectors = self.__CreateDefector(inputData)
        self.utility = Utility(
            generationPrice=inputData["generationPrice"],
            fixedCosts=inputData["fixedCosts"],
            permittedRoR=inputData["permittedRoR"],
            lossRate=inputData["lossRate"],
            rateCorrectionFreq=inputData["rateCorrectionFreq"],
            tariff=self.tariff,
            regularConsumer=self.regularConsumers,
            prosumer=self.prosumers,
        )
        self.standAlone = StandAloneSystem(battery=self.battery, pv=self.pv)
        self.imitationFactor = inputData["imitationFactor"]
        self.innovationFactor = inputData["innovationFactor"]
        self.populationGrowthRate = inputData["populationGrowthRate"]
        self.rateCorrectionFreq = inputData["rateCorrectionFreq"]
        self.pvPotential = inputData["pvPotential"]

    def __CreateTariff(self, data) -> ElectricityTariff:
        return ElectricityTariff(data["initialTariff"])

    def __CreateProsumer(self, data) -> Prosumer:
        return Prosumer(
            initialNumber=data["initialProsumerNumber"],
            initialDemandProfile=data["ConsumptionProfile"],
            priceElasticity=data["prosumerPriceElasticity"],
            demandChangeLimit=data["prosumerDemandChangeLimit"],
            PVSystem=self.pv,
            PVSize=data["PVSize"],
        )

    def __CreateDefector(self, data) -> Defector:
        return Defector(
            initialNumber=data["initialProsumerNumber"],
            initialDemandProfile=data["ConsumptionProfile"],
            priceElasticity=0,
            demandChangeLimit=0,
            PVSystem=self.pv,
            battery=self.battery,
        )

    def __CreateRegularConsumer(self, data) -> RegularConsumer:
        return RegularConsumer(
            initialNumber=data["initialRegularConsumerNumber"],
            initialDemandProfile=data["ConsumptionProfile"],
            priceElasticity=data["regularConsumerPriceElasticity"],
            demandChangeLimit=data["regularConsumerDemandChangeLimit"],
        )

    def __CalculatePVPenetrationRatio(self) -> float:
        totalPVHousholds = self.prosumers.currentNumber + self.defectors.currentNumber
        totalHousholds = (
            self.regularConsumers.currentNumber
            + self.prosumers.currentNumber
            + self.defectors.currentNumber
        )
        result = totalPVHousholds / totalHousholds

        return result

    def __CalculateBatteryPenetrationRatio(self) -> float:
        totalHousholds = (
            self.regularConsumers.currentNumber
            + self.prosumers.currentNumber
            + self.defectors.currentNumber
        )
        result = self.defectors.currentNumber / totalHousholds

        return result

    def Iterate(self, time):
        self.utility.CalculateFinances(time)
        if time % self.rateCorrectionFreq == 0:
            self.utility.CalculateNewTariff(time)
            self.regularConsumers.ChangeDemand(tariff=self.tariff)
            self.prosumers.ChangeDemand(tariff=self.tariff)

        pvRatio = self.__CalculatePVPenetrationRatio()
        self.pv.DecreasePrice(pvRatio)
        batteryRatio = self.__CalculateBatteryPenetrationRatio()
        self.battery.DecreasePrice(batteryRatio)
        self.__MigrateHouseholds(pvRatio, batteryRatio)

    def _CalculateRegular2ProsumerIRR(self, period: int) -> float:
        proEx = self.prosumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff, productionTariff=self.tariff
        )
        regEx = self.regularConsumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff
        )
        saving = regEx - proEx
        cost = self.prosumers.PVSystemSize * self.pv.currentPrice
        irr = hlp.CalculateIRR(inflow=saving, outflow=cost, period=period)
        return irr

    def _CalculateRegular2DefectorIRR(self, period: int) -> float:
        # calculate the saving
        saving = self.regularConsumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff
        )
        # calculate the cost
        pvsize, batterysize, cost = self.standAlone.OptimizeSystemSize(
            self.regularConsumers.demandProfile
        )
        # print(f'optimal system size-> PV: {pvsize:.2f}, Battery:{batterysize:.2f}, Cost:{cost}')
        irr = hlp.CalculateIRR(inflow=saving, outflow=cost, period=period)
        return irr

    def _CalculateProsumer2DefectorIRR(self, period: int) -> float:
        # calculate the saving
        saving = self.prosumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff, productionTariff=self.tariff
        )
        # calculate the cost
        pvsize, batterysize, _ = self.standAlone.OptimizeSystemSize(
            self.regularConsumers.demandProfile
        )

        pvsize -= self.prosumers.PVSystemSize
        batterychanges = int(self.pv.effectiveLife / self.battery.effectiveLife)
        cost = (
            pvsize * self.pv.currentPrice
            + batterysize * self.battery.currentPrice * batterychanges
        )
        irr = hlp.CalculateIRR(inflow=saving, outflow=cost, period=period)
        return irr

    def __MigrateHouseholds(self, pvRatio, batteryRatio):
        pvLimitEffect = hlp.Logistic4RatioLimit(pvRatio / self.pvPotential)
        projectLife = 25
        # from regular consumer to prosumer
        r2p = pvLimitEffect * self.__CalculateBassMigration(
            pvRatio,
            self._CalculateRegular2ProsumerIRR(projectLife),
            self.regularConsumers.currentNumber,
            multiplier=3,
        )

        # from regular consumer to defector
        r2d = pvLimitEffect * self.__CalculateBassMigration(
            batteryRatio,
            self._CalculateRegular2DefectorIRR(projectLife),
            self.regularConsumers.currentNumber,
        )

        # from prosumer to defector
        p2d = self.__CalculateBassMigration(
            batteryRatio,
            self._CalculateProsumer2DefectorIRR(projectLife),
            self.prosumers.currentNumber,
        )

        r, p, d = self.__GrowPopulation()
        self.regularConsumers.ChangeNumber(r - (r2d + r2p))
        self.prosumers.ChangeNumber(p + r2p - p2d)
        self.defectors.ChangeNumber(d + r2d + p2d)
        self.totalHousholds.append(
            self.regularConsumers.currentNumber
            + self.prosumers.currentNumber
            + self.defectors.currentNumber
        )
        # print(
        #     f"Electricity Price:{self.tariff.currentPrice:.3f}--PV Price:{self.pv.currentPrice:.2f}--NPV:{NPVRatio}")

    def __CalculateBassMigration(
        self, penetration, irr, sourcePopulation, multiplier=1
    ) -> float:
        financialEffect = hlp.Logistic(L=2, k=40, b=1, x0=0.2, input=irr)
        adaoptionrate = financialEffect * (
            self.innovationFactor + multiplier * self.imitationFactor * penetration
        )
        return adaoptionrate * sourcePopulation

    def __GrowPopulation(self) -> tuple:
        r = (
            hlp.ConvertYearly2MonthlyRate(self.populationGrowthRate)
        ) * self.regularConsumers.currentNumber
        p = (
            hlp.ConvertYearly2MonthlyRate(self.populationGrowthRate)
        ) * self.prosumers.currentNumber
        d = (
            hlp.ConvertYearly2MonthlyRate(self.populationGrowthRate)
        ) * self.defectors.currentNumber
        return (r, p, d)

    def ShowResults(self):

        mpl.rc("lines", linewidth=1.5, markersize=4)
        mpl.rc("grid", linewidth=0.5, linestyle="--")
        plt.rcParams["axes.grid"] = True
        mpl.rc("font", size=11, family="Times New Roman")
        fig, ax = plt.subplots(
            nrows=3, ncols=2, sharex=True, sharey=False, figsize=(21, 9)
        )
        ax[0, 0].plot(
            self.regularConsumers.GetNumberHistory(), label="Regular Consumers"
        )
        ax[0, 0].plot(self.prosumers.GetNumberHistory(), label="Prosumers")
        ax[0, 0].plot(self.defectors.GetNumberHistory(), label="Defectors")
        ax[0, 0].plot(self.totalHousholds, label="Total")
        ax[0, 0].legend()
        ax[0, 0].set_title("Number of Consumers")
        ax[0, 1].plot(
            self.regularConsumers.GetNumberHistory() / np.array(self.totalHousholds),
            label="Regular Consumers",
        )
        ax[0, 1].plot(
            self.prosumers.GetNumberHistory() / np.array(self.totalHousholds),
            label="Prosumers",
        )
        ax[0, 1].plot(
            self.defectors.GetNumberHistory() / np.array(self.totalHousholds),
            label="Defectors",
        )
        ax[0, 1].legend()
        ax[0, 1].set_title("Share of Consumers")
        ax[1, 0].plot(self.utility.saleHistory)
        ax[1, 0].set_title("Utility Sales")

        ax[1, 1].plot(
            [t[0] for t in self.tariff.GetHistory()],
            [t[1] for t in self.tariff.GetHistory()],
            marker="o",
        )

        # ax[2].bar([t[0] for t in self.tariff.GetHistory()],[t[1] for t in self.tariff.GetHistory()])
        ax[1, 1].set_title("Electricity tariff")
        ax[2, 0].plot(self.utility.budgetDeficit)
        ax[2, 0].set_title("Utility Budget Deficit")
        ax[2, 1].plot(
            [
                a[0] / a[1]
                for a in zip(self.utility.budgetDeficit, self.utility.saleHistory)
            ]
        )
        ax[2, 1].set_title("Utility Budget Deficit fraction")
        # plt.savefig(f'result-{self.rateCorrectionFreq}.jpg',dpi=600,bbox_inches='tight')
        fig2, ax2 = plt.subplots()
        ax2.plot(self.utility.GetYearlySale())
        ax2.xaxis.set_ticks(ticks=list(range(20)), labels=np.arange(1, 21, 1).tolist())
        plt.tight_layout()
        plt.show()

    def SaveResults(self):

        mpl.rc("lines", linewidth=1.5, markersize=4)
        mpl.rc("grid", linewidth=0.5, linestyle="--")
        plt.rcParams["axes.grid"] = True
        mpl.rc("font", size=8, family="Times New Roman")
        fig, ax = plt.subplots(nrows=2, figsize=(3.25, 4.5), sharex=True)
        ax[0].plot(
            [t[0] for t in self.tariff.GetHistory()],
            [t[1] for t in self.tariff.GetHistory()],
            marker="o",
            color="k",
        )
        ax[0].set_title("Electricity tariff")
        ax[0].set_ylabel("Price (dollar)")

        ax[1].plot(self.utility.saleHistory, color="k")
        ax[1].set_title("Total Monthly Utility Sales")
        ax[1].set_xlabel("Time (Month)")
        ax[1].set_xlim(-5, 245)
        ax[1].set_ylabel("Total Sales (dollar)")
        fig.savefig("result_base.pdf", bbox_inches="tight")

    def GetResults(self, time: list) -> pd.DataFrame:
        result = pd.DataFrame(index=time)
        result["Regular_Consumers"] = self.regularConsumers.GetNumberHistory()
        result["Prosumers"] = self.prosumers.GetNumberHistory()
        result["Defectors"] = self.defectors.GetNumberHistory()
        result["Total_Housholds"] = self.totalHousholds
        result["Utility_Sales"] = self.utility.saleHistory
        result["Utility_Deficit"] = self.utility.budgetDeficit
        result["Utility_Deficit_Fraction"] = (
            result["Utility_Deficit"] / result["Utility_Sales"]
        )
        tariff_list=np.ones_like(time,dtype=float)
        for t in self.tariff.GetHistory():
            tariff_list[t[0]:]=t[1]
        result["Tariff"] = tariff_list
        return result
