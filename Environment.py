# import numpy as np
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
            monthlyEnergyOutput=inputData["PVMonthlyEnergyOutput"],
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
        self.interestRate = inputData["DiscountRate"]
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

        # from regular consumer to prosumer
        self.CalculateRegular2ProsumerIRR()

        # from regular consumer to defector
        self.CalculateRegular2DefectorIRR()

        # from prosumer to defector
        self.CalculateProsumer2DefectorIRR()

        NPVProsumer = self.prosumers.CalculateNPV(
            consumptionTariff=self.tariff,
            productionTariff=self.tariff,
            interestRate=self.interestRate,
        )
        # NPVstandAlone = self.standAlone.CalculateNPV(
        #     hlp.ConvertYearly2MonthlyRate(self.interestRate),
        #     self.tariff,
        #     self.regularConsumers.GetMonthlyConsumption(time),
        # )

        NPVstandAlone = self.standAlone.CalculateNPVnew(
            hlp.ConvertYearly2MonthlyRate(self.interestRate),
            self.tariff,
            self.regularConsumers.demandProfile,
        )

        self.__MigrateHouseholds(pvRatio, batteryRatio, NPVProsumer, NPVstandAlone)

    def CalculateRegular2ProsumerIRR(self)->float:
        proEx = self.prosumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff, productionTariff=self.tariff
        )
        regEx=self.regularConsumers.GetYearlyExpenditure(consumptionTariff=self.tariff)
        saving=regEx-proEx
        cost=self.prosumers.PVSystemSize*self.pv.currentPrice
        irr=hlp.CalculateIRR(inflow=saving,outflow=cost,period=25)
        return irr

    def CalculateRegular2DefectorIRR(self)->float:
        # calculate the saving
        saving=0
        # calculate the cost
        cost=0
        irr=hlp.CalculateIRR(inflow=saving,outflow=cost,period=25)
        return irr
    
    def CalculateProsumer2DefectorIRR(self)->float:
        # calculate the saving
        saving=0
        # calculate the cost
        cost=0
        irr=hlp.CalculateIRR(inflow=saving,outflow=cost,period=25)
        return irr

    def __MigrateHouseholds(self, pvRatio, batteryRatio, NPVProsumer, NPVstandAlone):
        pvLimitEffect = hlp.Logistic4RatioLimit(pvRatio / self.pvPotential)
        p2d = self.__CalculateBassMigration(
            batteryRatio, NPVstandAlone - NPVProsumer, self.prosumers.currentNumber
        )
        r2d = pvLimitEffect * self.__CalculateBassMigration(
            batteryRatio, NPVstandAlone, self.regularConsumers.currentNumber
        )
        r2p = pvLimitEffect * self.__CalculateBassMigration(
            pvRatio, NPVProsumer, self.regularConsumers.currentNumber, multiplier=3
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
        self, penetration, NPVRatio, sourcePopulation, multiplier=1
    ) -> float:
        financialEffect = hlp.Logistic(L=2, k=4, b=1, x0=2, input=NPVRatio)
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
        mpl.rc("font", size=11, family="Times New Roman")
        fig, ax = plt.subplots(5, sharex=True)
        ax[0].plot(self.regularConsumers.GetNumberHistory(), label="Regular Consumers")
        ax[0].plot(self.prosumers.GetNumberHistory(), label="Prosumers")
        ax[0].plot(self.defectors.GetNumberHistory(), label="Defectors")
        ax[0].plot(self.totalHousholds, label="Total")
        ax[0].legend()
        ax[0].set_title("Number of Consumers")
        ax[1].plot(self.utility.saleHistory)
        ax[1].set_title("Utility Sales")

        a = self.tariff.GetHistory()[0]
        ax[2].scatter(
            [t[0] for t in self.tariff.GetHistory()],
            [t[1] for t in self.tariff.GetHistory()],
        )
        # ax[2].bar([t[0] for t in self.tariff.GetHistory()],[t[1] for t in self.tariff.GetHistory()])
        ax[2].set_title("Electricity tariff")
        ax[3].plot(self.utility.budgetDeficit)
        ax[3].set_title("Utility Budget Deficit")
        ax[4].plot(
            [
                a[0] / a[1]
                for a in zip(self.utility.budgetDeficit, self.utility.saleHistory)
            ]
        )
        ax[4].set_title("Utility Budget Deficit fraction")
        for a in ax:
            a.grid(True)
        plt.show()
