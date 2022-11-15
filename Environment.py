import numpy as np
from ElectricityTariff import ElectricityTariff
from Helper import Logistic
from PV import PV
from Battery import Battery
from Prosumer import Prosumer
from RegularConsumer import RegularConsumer
from Utility import Utility
import matplotlib.pyplot as plt


class Environment:
    def __init__(self, inputData) -> None:
        self.pv = PV(initialPrice=inputData["initialPVPrice"],
                     normalReductionRate=inputData["normalPVCostReductionRate"],
                     minimumPrice=inputData["minimumPVPrice"],
                     effectiveLife=inputData["PVEffectiveLife"],
                     monthlyEnergyOutput=inputData["PVMonthlyEnergyOutput"],
                     interestRate=inputData["DiscountRate"])
        self.battery = Battery(initialPrice=inputData["initialBatteryPrice"],
                               normalReductionRate=inputData["normalBatteryCostReductionRate"],
                               minimumPrice=inputData["minimumBatteryPrice"])
        self.tariff = self.__CreateTariff(inputData)
        self.prosumers = self.__CreateProsumer(inputData)
        self.regularConsumers = self.__CreateRegularConsumer(inputData)
        self.utility = Utility(generationPrice=inputData["generationPrice"],
                               fixedCosts=inputData["fixedCosts"],
                               permittedRoR=inputData["permittedRoR"],
                               lossRate=inputData["lossRate"],
                               rateCorrectionFreq=inputData["rateCorrectionFreq"],
                               tariff=self.tariff,
                               regularConsumer=self.regularConsumers,
                               prosumer=self.prosumers)
        self.imitationFactor = inputData["imitationFactor"]
        self.innovationFactor = inputData["innovationFactor"]

    def __CreateTariff(self, data) -> ElectricityTariff:
        return ElectricityTariff(data["initialTariff"])

    def __CreateProsumer(self, data) -> Prosumer:
        return Prosumer(data["initialProsumerNumber"],
                        data["initialProsumerMonthlyDemand"],
                        data["prosumerPriceElasticity"],
                        data["prosumerDemandChangeLimit"])

    def __CreateRegularConsumer(self, data) -> RegularConsumer:
        return RegularConsumer(data["initialRegularConsumerNumber"],
                               data["initialRegularConsumerMonthlyDemand"],
                               data["regularConsumerPriceElasticity"],
                               data["regularConsumerDemandChangeLimit"])

    def __ChangeConsumerNumber(self, pvPenetrationratio, NPVRatio):
        effectOfPVNPV = Logistic(L=2, k=-4, b=1, x0=2, input=NPVRatio)
        innovators = effectOfPVNPV*self.innovationFactor * \
            self.regularConsumers.currentNumber

        imitators = effectOfPVNPV*self.imitationFactor * \
            pvPenetrationratio * self.regularConsumers.currentNumber
        totalConvertion2Prosumer = innovators+imitators
        self.prosumers.ChangeNumber(totalConvertion2Prosumer)
        self.regularConsumers.ChangeNumber(-totalConvertion2Prosumer)

    def __CalculatePVPenetrationRatio(self) -> float:
        totalNumberOfPVResidence = self.prosumers.currentNumber
        totalNumerOfResidences = self.regularConsumers.currentNumber + \
            self.prosumers.currentNumber
        result = totalNumberOfPVResidence / totalNumerOfResidences

        return result

    def Iterate(self, time):
        self.utility.CalculateNewTariff()
        self.regularConsumers.ChangeDemand(tariff=self.tariff)
        self.prosumers.ChangeDemand(tariff=self.tariff)
        pvRatio = self.__CalculatePVPenetrationRatio()
        self.pv.DecreasePrice(pvRatio)
        NPVRatio = self.pv.CalculateNPV(
            electricityPrice=self.tariff.currentPrice)/self.pv.currentPrice
        self.__ChangeConsumerNumber(pvRatio, NPVRatio)

        print(
            f"Electricity Price:{self.tariff.currentPrice:.3f}--PV Price:{self.pv.currentPrice:.2f}--NPV:{NPVRatio}")

    def ShowResults(self):
        fig, ax = plt.subplots(3)
        ax[0].plot(self.regularConsumers.GetNumberHistory())
        ax[0].set_title("Number of Regular Consumers")
        ax[1].plot(self.utility.saleHistory)
        ax[1].set_title("Utility Sales")
        ax[2].plot(self.tariff.GetHistory())
        ax[2].set_title("Electricity tariff")
        plt.show()
    