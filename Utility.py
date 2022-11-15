from ElectricityTariff import ElectricityTariff
from Prosumer import Prosumer
from RegularConsumer import RegularConsumer


class Utility:
    def __init__(self, generationPrice, fixedCosts, permittedRoR, lossRate, rateCorrectionFreq, tariff: ElectricityTariff, regularConsumer: RegularConsumer, prosumer: Prosumer) -> None:
        self.__generationPrice = generationPrice
        self.__fixedCosts = fixedCosts
        self.__permittedRoR = permittedRoR
        self.__lossRate = lossRate
        self.__rateCorrectionFreq = rateCorrectionFreq
        self.tariff = tariff
        self.regularConsumer = regularConsumer
        self.prosumers = prosumer
        self.saleHistory=[]

    def Iterate(self):
        pass

    def __CalculateSale(self) -> None:
        sale = self.regularConsumer.monthlyDemand*self.regularConsumer.currentNumber + \
            self.prosumers.monthlyDemand*self.prosumers.currentNumber
        self.saleHistory.append(sale)

    def __CalculateCost(self) -> None:
        self.costs = self.__fixedCosts+self.saleHistory[-1] * \
            (1+self.__lossRate)*self.__generationPrice

    def __CalculateActualIncome(self) -> None   :
        self.ActualIncome = self.saleHistory[-1] * self.tariff.currentPrice

    def __CalculateExpectedIncome(self) -> None:
        self.ExpectedIncome = self.costs * (1+self.__permittedRoR)

    def CalculateNewTariff(self) -> None:
        self.__CalculateSale()
        self.__CalculateCost()
        self.__CalculateActualIncome()
        self.__CalculateExpectedIncome()
        newprice1 = self.__CalculateNewTariff()

    def __CalculateNewTariff(self) -> None:
        budgetDeficit = self.ExpectedIncome - self.ActualIncome
        priceChange = budgetDeficit/self.saleHistory[-1]
        self.tariff.SetNewTariff(self.tariff.currentPrice + priceChange)
