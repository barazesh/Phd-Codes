import numpy as np
import Helper as hlp


class PV:
    def __init__(
        self,
        initialPrice: float,
        normalReductionRate: float,
        minimumPrice: float,
        effectiveLife: int,
        hourlyEnergyOutput: np.ndarray,
    ) -> None:
        self.__priceHistory = []
        self.currentPrice = initialPrice
        self.__minimumPrice = minimumPrice
        self.__normalReductionRate = normalReductionRate
        self.effectiveLife = effectiveLife
        self.hourlyEnergyOutput = hourlyEnergyOutput

    def DecreasePrice(self, penetrationRatio: float) -> None:
        penetrationEffect = hlp.Logistic(
            b=1, L=0.5, k=15, x0=1 / 3, input=penetrationRatio
        )
        indicatedReduction = (
            penetrationEffect * self.__normalReductionRate * self.currentPrice
        )
        limitEffect = self.__CalculateLimitEffect(
            self.currentPrice - indicatedReduction
        )
        self.__priceHistory.append(self.currentPrice)
        self.currentPrice = self.currentPrice - indicatedReduction * limitEffect

    def __CalculateLimitEffect(self, tempPrice: float) -> float:
        ratio = self.__minimumPrice / tempPrice
        return hlp.Logistic4RatioLimit(ratio)
