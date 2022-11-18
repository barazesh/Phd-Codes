import numpy as np
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
        self.pv = PV(initialPrice=inputData["initialPVPrice"],
                     normalReductionRate=inputData["normalPVCostReductionRate"],
                     minimumPrice=inputData["minimumPVPrice"],
                     effectiveLife=inputData["PVEffectiveLife"],
                     monthlyEnergyOutput=inputData["PVMonthlyEnergyOutput"],
                     )

        self.battery = Battery(initialPrice=inputData["initialBatteryPrice"],
                               normalReductionRate=inputData["normalBatteryCostReductionRate"],
                               minimumPrice=inputData["minimumBatteryPrice"],
                               effectiveLife=inputData["BatteryEffectiveLife"],
                               )
        self.totalHousholds = [
            inputData["initialRegularConsumerNumber"]+inputData["initialProsumerNumber"]]

        self.tariff = self.__CreateTariff(inputData)
        self.prosumers = self.__CreateProsumer(inputData)
        self.regularConsumers = self.__CreateRegularConsumer(inputData)
        self.defectors = self.__CreateDefector(inputData)
        self.utility = Utility(generationPrice=inputData["generationPrice"],
                               fixedCosts=inputData["fixedCosts"],
                               permittedRoR=inputData["permittedRoR"],
                               lossRate=inputData["lossRate"],
                               rateCorrectionFreq=inputData["rateCorrectionFreq"],
                               tariff=self.tariff,
                               regularConsumer=self.regularConsumers,
                               prosumer=self.prosumers)
        self.standAlone = StandAloneSystem(battery=self.battery, pv=self.pv)
        self.imitationFactor = inputData["imitationFactor"]
        self.innovationFactor = inputData["innovationFactor"]
        self.interestRate = inputData["DiscountRate"]
        self.populationGrowthRate = inputData["populationGrowthRate"]

    def __CreateTariff(self, data) -> ElectricityTariff:
        return ElectricityTariff(data["initialTariff"])

    def __CreateProsumer(self, data) -> Prosumer:
        return Prosumer(data["initialProsumerNumber"],
                        data["initialProsumerMonthlyDemand"],
                        data["prosumerPriceElasticity"],
                        data["prosumerDemandChangeLimit"])

    def __CreateDefector(self, data) -> Defector:
        return Defector(data["initialProsumerNumber"])

    def __CreateRegularConsumer(self, data) -> RegularConsumer:
        return RegularConsumer(data["initialRegularConsumerNumber"],
                               data["initialRegularConsumerMonthlyDemand"],
                               data["regularConsumerPriceElasticity"],
                               data["regularConsumerDemandChangeLimit"])

    def __CalculatePVPenetrationRatio(self) -> float:
        totalPVHousholds = self.prosumers.currentNumber + self.defectors.currentNumber
        totalHousholds = self.regularConsumers.currentNumber + \
            self.prosumers.currentNumber+self.defectors.currentNumber
        result = totalPVHousholds / totalHousholds

        return result

    def __CalculateBatteryPenetrationRatio(self) -> float:
        totalHousholds = self.regularConsumers.currentNumber + \
            self.prosumers.currentNumber+self.defectors.currentNumber
        result = self.defectors.currentNumber / totalHousholds

        return result

    def Iterate(self, time):
        self.utility.CalculateNewTariff()
        self.regularConsumers.ChangeDemand(tariff=self.tariff)
        self.prosumers.ChangeDemand(tariff=self.tariff)
        pvRatio = self.__CalculatePVPenetrationRatio()
        self.pv.DecreasePrice(pvRatio)
        batteryRatio = self.__CalculateBatteryPenetrationRatio()
        self.battery.DecreasePrice(batteryRatio)
        NPVProsumer = self.pv.CalculateNPV(
            self.tariff.currentPrice, hlp.ConvertYearly2MonthlyRate(self.interestRate))
        NPVstandAlone = self.standAlone.CalculateNPV(
            hlp.ConvertYearly2MonthlyRate(self.interestRate), self.tariff, self.regularConsumers.monthlyDemand)
        self.__MigrateHouseholds(
            pvRatio, batteryRatio, NPVProsumer, NPVstandAlone)

    def __MigrateHouseholds(self, pvRatio, batteryRatio, NPVProsumer, NPVstandAlone):
        p2d = self.__CalculateBassMigration(
            batteryRatio, NPVstandAlone-NPVProsumer, self.prosumers.currentNumber)
        r2d = self.__CalculateBassMigration(
            batteryRatio, NPVstandAlone, self.regularConsumers.currentNumber)
        r2p = self.__CalculateBassMigration(
            pvRatio, NPVProsumer, self.regularConsumers.currentNumber)
        r,p,d = self.__GrowPopulation()
        self.regularConsumers.ChangeNumber(r-(r2d+r2p))
        self.prosumers.ChangeNumber(p+r2p-p2d)
        self.defectors.ChangeNumber(d+r2d+p2d)
        self.totalHousholds.append(self.regularConsumers.currentNumber +
                                   self.prosumers.currentNumber+self.defectors.currentNumber)
        # print(
        #     f"Electricity Price:{self.tariff.currentPrice:.3f}--PV Price:{self.pv.currentPrice:.2f}--NPV:{NPVRatio}")

    def __CalculateBassMigration(self, penetration, NPVRatio, sourcePopulation) -> float:
        financialEffect = hlp.Logistic(L=2, k=-4, b=1, x0=2, input=NPVRatio)
        adaoptionrate = financialEffect * \
            (self.innovationFactor+self.imitationFactor * penetration)
        return adaoptionrate*sourcePopulation

    def __GrowPopulation(self)-> tuple:
        r=(hlp.ConvertYearly2MonthlyRate(self.populationGrowthRate))*self.regularConsumers.currentNumber
        p=(hlp.ConvertYearly2MonthlyRate(self.populationGrowthRate))*self.prosumers.currentNumber
        d=(hlp.ConvertYearly2MonthlyRate(self.populationGrowthRate))*self.defectors.currentNumber
        return (r,p,d)
        
    def ShowResults(self):
        mpl.rc('lines', linewidth=1.5, markersize=4)
        mpl.rc('grid', linewidth=0.5, linestyle='--')
        mpl.rc('font', size=7, family='Times New Roman')
        fig, ax = plt.subplots(3)
        ax[0].plot(self.regularConsumers.GetNumberHistory(),
                   label='Regular Consumers')
        ax[0].plot(self.prosumers.GetNumberHistory(), label='Prosumers')
        ax[0].plot(self.defectors.GetNumberHistory(), label='Defectors')
        ax[0].plot(self.totalHousholds, label='Total')
        ax[0].legend()
        ax[0].set_title("Number of Consumers")
        ax[1].plot(self.utility.saleHistory)
        ax[1].set_title("Utility Sales")
        ax[2].plot(self.tariff.GetHistory())
        ax[2].set_title("Electricity tariff")
        for a in ax:
            a.grid(True)
        plt.show()
