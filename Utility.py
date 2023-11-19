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
        fixed2VariableRatio: float,
        authorizedRoR: float,
        lossRate: float,
        residentialShare: float,
        rateCorrectionFreq: int,
        retailTariff: ElectricityTariff,
        buybackTariff: ElectricityTariff,
        regularConsumer: RegularConsumer,
        prosumer: Prosumer,
    ) -> None:
        assert (fixed2VariableRatio >= 0) & (fixed2VariableRatio <= 1)
        self._generationPrice = generationPrice
        self._fixedCosts = fixedCosts
        self._rateBase = rateBase
        self._fixed2VariableRatio = fixed2VariableRatio
        self._authorizedRoR = authorizedRoR
        self._lossRate = lossRate
        self._rateCorrectionFreq = rateCorrectionFreq
        self._residentialShare = residentialShare
        self.retailTariff = retailTariff
        self.buybackTariff = buybackTariff
        self.regularConsumer = regularConsumer
        self.prosumers = prosumer
        self.saleHistory: list[float] = []
        self.revenueHistory: list[float] = []
        self.budgetDeficit: list[float] = [0.0]
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
            self._fixedCosts[month] * self._residentialShare
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

    def _CalculateRevenueRequirement(self, month: int) -> float:
        return (
            self.costs
            + self._rateBase[month] * self._authorizedRoR * self._residentialShare
        )

    def CalculateFinances(self, month: int) -> None:
        self._CalculateSale(month)
        self._CalculateActualRevenue()
        self._CalculateCost(month)
        self.budgetDeficit.append(
            self.budgetDeficit[-1]
            + self._CalculateRevenueRequirement(month)
            - self.revenueHistory[-1]
        )

    def CalculateNewTariff(self, time: int) -> None:
        self._CalculateNewTariff_deficit(time)

    def _CalculateNewTariff_deficit(self, time: int) -> None:
        # this method calculates the price change based on distributing the budget deficit
        fixedPriceChange = (
            self._fixed2VariableRatio
            * self.budgetDeficit[-1]
            / (self.prosumers.currentNumber + self.regularConsumer.currentNumber)
        )
        totalSale = sum(self.saleHistory[-self._rateCorrectionFreq :])
        variablePriceChange = (
            (1 - self._fixed2VariableRatio) * self.budgetDeficit[-1] / totalSale
        )
        self.retailTariff.ChangeTariff(
            time,
            fixedPriceChange=fixedPriceChange,
            variablePriceChange=variablePriceChange,
        )

    def _CalculateNewTariff_cost(self, time: int) -> None:
        # this method calculates the new tariff based on costs and rate base of the testyear
        fixedCost_testYear = sum(self._fixedCosts[time - 12 : time])
        revenueRequirement_testYear = (
            sum(self._rateBase[time - 12 : time]) * self._authorizedRoR
        )
        total_fixedCost = (
            fixedCost_testYear + revenueRequirement_testYear + self.budgetDeficit[-1]
        ) * self._residentialShare

        fixedPrice = (self._fixed2VariableRatio * total_fixedCost) / (
            self.prosumers.currentNumber + self.regularConsumer.currentNumber
        )

        totalSale = sum(self.saleHistory[-12:])
        variablePrice = (1 + self._lossRate) * self._generationPrice + (
            1 - self._fixed2VariableRatio
        ) * total_fixedCost / totalSale

        self.retailTariff.SetNewTariff(
            time, new_fixedPrice=fixedPrice, new_variablePrice=variablePrice
        )

    def GetYearlySale(self) -> np.ndarray:
        n = 12
        result = [
            sum(self.saleHistory[i : i + n]) for i in range(0, len(self.saleHistory), n)
        ]
        return np.array(result)
