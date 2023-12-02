import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from Defector import Defector
from ElectricityTariff import ElectricityTariff
import Helper as hlp
from PV import PV
from Battery import Battery
from Prosumer import Prosumer
from RegularConsumer import RegularConsumer
from StandAlone import StandAloneSystem
from Utility import Utility


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
            + inputData["initialDefectorNumber"]
        ]

        self._CreateTariff(inputData)
        self.prosumers = self._CreateProsumer(inputData)
        self.regularConsumers = self._CreateRegularConsumer(inputData)
        self.defectors = self._CreateDefector(inputData)
        self.utility = self.CreateUtility(inputData)
        self.standAlone = StandAloneSystem(battery=self.battery, pv=self.pv)
        self.imitationFactor = inputData["imitationFactor"]
        self.innovationFactor = inputData["innovationFactor"]
        self.populationGrowthRate = inputData["populationGrowthRate"]
        self.rateCorrectionFreq = inputData["rateCorrectionFreq"]
        self.pvPotential = inputData["pvPotential"]
        self.BASSp2d = inputData["BASSp2d"]
        self.BASSr2d = inputData["BASSr2d"]
        self.r2pIRR: list[float] = [0]
        self.r2dIRR: list[float] = [0]
        self.p2dIRR: list[float] = [0]

    def CreateUtility(self, inputData):
        return Utility(
            generationPrice=inputData["generationPrice"],
            fixedCosts=inputData["fixedCosts"],
            rateBase=inputData["rateBase"],
            fixed2VariableRatio=inputData["fixed2VariableRatio"],
            authorizedRoR=inputData["authorizedRoR"],
            lossRate=inputData["lossRate"],
            residentialShare=inputData["residentialShare"],
            rateCorrectionFreq=inputData["rateCorrectionFreq"],
            rateCorrectionMethod=inputData["rateCorrectionMethod"],
            retailTariff=self.tariff,
            buybackTariff=self.tariff,  # net metering: the price of buyback is equal to retail price
            regularConsumer=self.regularConsumers,
            prosumer=self.prosumers,
        )

    def _CreateTariff(self, data) -> None:
        self.tariff = ElectricityTariff(
            initialFixedTariff=data["initialFixedTariff"],
            initialVariableTariff=data["initialVariableTariff"],
        )

    def _CreateProsumer(self, data) -> Prosumer:
        return Prosumer(
            initialNumber=data["initialProsumerNumber"],
            initialDemandProfile=np.copy(data["ConsumptionProfile"]),
            priceElasticity=data["prosumerPriceElasticity"],
            demandChangeLimit=data["prosumerDemandChangeLimit"],
            PVSystem=self.pv,
            PVSize=data["PVSize"],
        )

    def _CreateDefector(self, data) -> Defector:
        return Defector(
            initialNumber=data["initialDefectorNumber"],
            initialDemandProfile=np.copy(data["ConsumptionProfile"]),
            priceElasticity=0,
            demandChangeLimit=0,
            PVSystem=self.pv,
            battery=self.battery,
        )

    def _CreateRegularConsumer(self, data) -> RegularConsumer:
        return RegularConsumer(
            initialNumber=data["initialRegularConsumerNumber"],
            initialDemandProfile=np.copy(data["ConsumptionProfile"]),
            priceElasticity=data["regularConsumerPriceElasticity"],
            demandChangeLimit=data["regularConsumerDemandChangeLimit"],
        )

    def _CalculatePVPenetrationRatio(self) -> float:
        totalPVHousholds = self.prosumers.currentNumber + self.defectors.currentNumber
        totalHousholds = (
            self.regularConsumers.currentNumber
            + self.prosumers.currentNumber
            + self.defectors.currentNumber
        )
        result = totalPVHousholds / totalHousholds

        return result

    def _CalculateBatteryPenetrationRatio(self) -> float:
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

        pvRatio = self._CalculatePVPenetrationRatio()
        self.pv.DecreasePrice(pvRatio)
        batteryRatio = self._CalculateBatteryPenetrationRatio()
        self.battery.DecreasePrice(batteryRatio)
        self._MigrateHouseholds(pvRatio, batteryRatio)

    def _MigrateHouseholds(self, pvRatio, batteryRatio):
        pvLimitEffect = hlp.Logistic4RatioLimit(pvRatio / self.pvPotential)
        projectLife = 25
        # from regular consumer to prosumer
        r2p = pvLimitEffect * self._CalculateBassMigration(
            pvRatio,
            self._CalculateRegular2ProsumerIRR(projectLife),
            self.regularConsumers.currentNumber,
            multiplier=4,
        )

        # from regular consumer to defector
        r2d = (
            self.BASSr2d
            * pvLimitEffect
            * self._CalculateBassMigration(
                batteryRatio,
                self._CalculateRegular2DefectorIRR(projectLife),
                self.regularConsumers.currentNumber,
            )
        )

        # from prosumer to defector
        p2d = self.BASSp2d * self._CalculateBassMigration(
            batteryRatio,
            self._CalculateProsumer2DefectorIRR(projectLife),
            self.prosumers.currentNumber,
        )

        r, p, d = self._GrowPopulation()
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

    def _CalculateBassMigration(
        self, penetration, irr, sourcePopulation, multiplier=1
    ) -> float:
        financialEffect = hlp.Logistic(L=2.5, k=10, b=0.5, x0=0.3, input=irr)
        # financialEffect = hlp.Logistic(L=2, k=40, b=1, x0=0.2, input=irr)
        adaoptionrate = financialEffect * (
            self.innovationFactor + multiplier * self.imitationFactor * penetration
        )
        return adaoptionrate * sourcePopulation

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
        # print(f'Regular2Prosumer IRR: {irr}')
        self.r2pIRR.append(irr)
        return irr

    def _CalculateRegular2DefectorIRR(self, period: int) -> float:
        # calculate the saving
        saving = self.regularConsumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff
        )
        # calculate the cost
        pvsize, batterysize, cost = self.standAlone.OptimizeSystemSize(
            self.regularConsumers.DemandProfile
        )
        # print(f'optimal system size-> PV: {pvsize:.2f}, Battery:{batterysize:.2f}, Cost:{cost}')
        irr = hlp.CalculateIRR(inflow=saving, outflow=cost, period=period)
        # print(f'Regular2Defector IRR: {irr}')
        self.r2dIRR.append(irr)

        return irr

    def _CalculateProsumer2DefectorIRR(self, period: int) -> float:
        # calculate the saving
        saving = self.prosumers.GetYearlyExpenditure(
            consumptionTariff=self.tariff, productionTariff=self.tariff
        )
        # calculate the cost
        pvsize, batterysize, _ = self.standAlone.OptimizeSystemSize(
            self.regularConsumers.DemandProfile
        )

        pvsize -= self.prosumers.PVSystemSize
        batterychanges = int(self.pv.effectiveLife / self.battery.effectiveLife)
        cost = (
            pvsize * self.pv.currentPrice
            + batterysize * self.battery.currentPrice * batterychanges
        )
        irr = hlp.CalculateIRR(inflow=saving, outflow=cost, period=period)
        # print(f'Prosumer2Defector IRR: {irr}')
        self.p2dIRR.append(irr)
        return irr

    def _GrowPopulation(self) -> tuple:
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

    def GetResults(self, time: list) -> pd.DataFrame:
        result = pd.DataFrame(index=time)
        result["Regular_Consumers"] = self.regularConsumers.GetNumberHistory()
        result["Prosumers"] = self.prosumers.GetNumberHistory()
        result["Defectors"] = self.defectors.GetNumberHistory()
        result["Total_Housholds"] = self.totalHousholds
        result["Utility_Sales"] = self.utility.saleHistory
        result["Utility_Deficit"] = self.utility.budgetDeficit
        result["Utility_Deficit_Fraction"] = (
            result["Utility_Deficit"] / self.utility.revenueHistory
        )
        result["Regular2ProsumerIRR"] = self.r2pIRR
        result["Regular2DefectorIRR"] = self.r2dIRR
        result["Prosumer2DefectorIRR"] = self.p2dIRR
        tariff_list_var = np.ones_like(time, dtype=float)
        tariff_list_fix = np.ones_like(time, dtype=float)
        for t in self.tariff.GetHistory():
            tariff_list_var[t["time"] :] = t["variable"]
            tariff_list_fix[t["time"] :] = t["fixed"]
        result["Tariff_var"] = tariff_list_var
        result["Tariff_fix"] = tariff_list_fix
        result["Prosumers_Demand_Change"] = self.GetDemandChangeHistory(
            self.prosumers._demandChangeHistory
        )
        result["Regular_Consumers_Demand_Change"] = self.GetDemandChangeHistory(
            self.regularConsumers._demandChangeHistory
        )
        return result

    def GetDemandChangeHistory(self, history):
        temp = np.cumprod(history)
        result = [
            item for item in temp[:-1] for _ in range(self.rateCorrectionFreq)
        ] + [temp[-1]]
        return result
