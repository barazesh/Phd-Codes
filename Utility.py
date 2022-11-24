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
        self.saleHistory = []
        self.budgetDeficit = [0.0]

    def Iterate(self):
        pass

    def __CalculateSale(self) -> None:
        sale = self.regularConsumer.monthlyDemand*self.regularConsumer.currentNumber + \
            self.prosumers.monthlyDemand*self.prosumers.currentNumber
        self.saleHistory.append(sale)

    def __CalculateCost(self) -> None:
        self.costs = self.__fixedCosts+self.saleHistory[-1] * \
            (1+self.__lossRate)*self.__generationPrice

    def __CalculateActualIncome(self) -> float:
        return self.saleHistory[-1] * self.tariff.currentPrice

    def __CalculateExpectedIncome(self) -> float:
        return self.costs * (1+self.__permittedRoR)

    def CalculateFinances(self) -> None:
        self.__CalculateSale()
        self.__CalculateCost()
        self.budgetDeficit.append(
            self.budgetDeficit[-1]+self.__CalculateExpectedIncome()-self.__CalculateActualIncome())

    def CalculateNewTariff(self, time):
        priceChange = self.budgetDeficit[-1]/self.saleHistory[-1]
        priceChange = priceChange/6
        # priceChange = priceChange/self.__rateCorrectionFreq
        self.tariff.SetNewTariff(time, self.tariff.currentPrice + priceChange)
