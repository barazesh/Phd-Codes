import numpy as np
from ElectricityTariff import ElectricityTariff
from Prosumer import Prosumer
from RegularConsumer import RegularConsumer


class Utility:
    def __init__(
        self,
        generationPrice: float,
        fixedCosts: list,
        rateBase: list,
        fixed2VariableRatio:float,
        authorizedRoR: float,
        lossRate: float,
        residentialShare:float,
        rateCorrectionFreq: int,
        retailTariff: ElectricityTariff,
        buybackTariff: ElectricityTariff,
        regularConsumer: RegularConsumer,
        prosumer: Prosumer,
    ) -> None:
        assert ((fixed2VariableRatio >= 0) & (fixed2VariableRatio <=1))
        self.__generationPrice = generationPrice
        self.__fixedCosts = fixedCosts
        self.__rateBase = rateBase
        self.__fixed2VariableRatio=fixed2VariableRatio
        self.__authorizedRoR = authorizedRoR
        self.__lossRate = lossRate
        self.__rateCorrectionFreq = rateCorrectionFreq
        self.__residentialShare=residentialShare
        self.retailTariff = retailTariff
        self.buybackTariff = buybackTariff
        self.regularConsumer = regularConsumer
        self.prosumers = prosumer
        self.saleHistory = []
        self.budgetDeficit = [0.0]
        self.__CalculateSale(0)

    def Iterate(self):
        pass

    def __CalculateSale(self, month: int) -> None:
        sale = (
            self.regularConsumer.GetMonthlyConsumption(month)
            * self.regularConsumer.currentNumber
            + self.prosumers.GetMonthlyConsumption(month) * self.prosumers.currentNumber
        )
        self.saleHistory.append(sale)

    def __CalculateCost(self, month: int) -> None:
        self.costs = (
            self.__fixedCosts[month]*self.__residentialShare
            + self.saleHistory[-1] * (1 + self.__lossRate) * self.__generationPrice
            + self.prosumers.GetMonthlyProduction(month)
            * (self.buybackTariff.currentVariablePrice - self.__generationPrice)
        )

    def __CalculateActualRevenue(self) -> float:
        variableRevenue = self.saleHistory[-1] * self.retailTariff.currentVariablePrice
        fixedRevenue = (
            self.regularConsumer.currentNumber + self.prosumers.currentNumber
        ) * self.retailTariff.currentFixedPrice
        return variableRevenue + fixedRevenue

    def __CalculateRevenueRequirement (self,month) -> float:
        return self.costs +self.__rateBase[month]* (1 + self.__authorizedRoR)

    def CalculateFinances(self, month: int) -> None:
        self.__CalculateSale(month)
        self.__CalculateCost(month)
        self.budgetDeficit.append(
            self.budgetDeficit[-1]
            + self.__CalculateRevenueRequirement (month)
            - self.__CalculateActualRevenue()
        )

    def CalculateNewTariff(self, time) -> None:
        totalSale = sum(self.saleHistory[-self.__rateCorrectionFreq :])
        fixedPriceChange = self.__fixed2VariableRatio*self.budgetDeficit[-1] / (self.prosumers.currentNumber+self.regularConsumer.currentNumber)
        variablePriceChange = (1-self.__fixed2VariableRatio)*self.budgetDeficit[-1] / totalSale
        self.retailTariff.SetNewTariff(
            time, fixedPriceChange=fixedPriceChange,variablePriceChange=variablePriceChange
        )

    def GetYearlySale(self) -> np.ndarray:
        n = 12
        result = [
            sum(self.saleHistory[i : i + n]) for i in range(0, len(self.saleHistory), n)
        ]
        return np.array(result)
