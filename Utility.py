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
        self._generationPrice = generationPrice
        self._fixedCosts = fixedCosts
        self._rateBase = rateBase
        self._fixed2VariableRatio=fixed2VariableRatio
        self._authorizedRoR = authorizedRoR
        self._lossRate = lossRate
        self._rateCorrectionFreq = rateCorrectionFreq
        self._residentialShare=residentialShare
        self.retailTariff = retailTariff
        self.buybackTariff = buybackTariff
        self.regularConsumer = regularConsumer
        self.prosumers = prosumer
        self.saleHistory = []
        self.revenueHistory = []
        self.budgetDeficit = [0.0]
        self._CalculateSale(0)
        self._CalculateActualRevenue()

    def Iterate(self):
        pass

    def _CalculateSale(self, month: int) -> None:
        sale = (
            self.regularConsumer.GetMonthlyConsumption(month)
            * self.regularConsumer.currentNumber
            + self.prosumers.GetMonthlyConsumption(month) * self.prosumers.currentNumber
        )
        self.saleHistory.append(sale)

    def _CalculateCost(self, month: int) -> None:
        self.costs = (
            self._fixedCosts[month]*self._residentialShare
            + self.saleHistory[-1] * (1 + self._lossRate) * self._generationPrice
            + self.prosumers.GetMonthlyProduction(month)
            * (self.buybackTariff.currentVariablePrice - self._generationPrice)
        )

    def _CalculateActualRevenue(self) -> None:
        variableRevenue = self.saleHistory[-1] * self.retailTariff.currentVariablePrice
        fixedRevenue = (
            self.regularConsumer.currentNumber + self.prosumers.currentNumber
        ) * self.retailTariff.currentFixedPrice
        self.revenueHistory.append(variableRevenue + fixedRevenue) 

    def _CalculateRevenueRequirement (self,month) -> float:
        return self.costs +self._rateBase[month]* self._authorizedRoR

    def CalculateFinances(self, month: int) -> None:
        self._CalculateSale(month)
        self._CalculateActualRevenue()
        self._CalculateCost(month)
        self.budgetDeficit.append(
            self.budgetDeficit[-1]
            + self._CalculateRevenueRequirement (month)
            - self.revenueHistory[-1]
        )

    def CalculateNewTariff(self, time) -> None:
        fixedPriceChange = self._fixed2VariableRatio*self.budgetDeficit[-1] / (self.prosumers.currentNumber+self.regularConsumer.currentNumber)
        totalSale = sum(self.saleHistory[-self._rateCorrectionFreq :])
        variablePriceChange = (1-self._fixed2VariableRatio)*self.budgetDeficit[-1] / totalSale
        self.retailTariff.SetNewTariff(
            time, fixedPriceChange=fixedPriceChange,variablePriceChange=variablePriceChange
        )

    def GetYearlySale(self) -> np.ndarray:
        n = 12
        result = [
            sum(self.saleHistory[i : i + n]) for i in range(0, len(self.saleHistory), n)
        ]
        return np.array(result)
