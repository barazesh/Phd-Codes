import numpy as np
import Helper as hlp

class Battery:
    def __init__(self, initialPrice, normalReductionRate,  minimumPrice, effectiveLife) -> None:
        self.__priceHistory = []
        self.currentPrice = initialPrice
        self.__minimumPrice = minimumPrice
        self.__normalReductionRate = normalReductionRate
        self.effectiveLife = effectiveLife


    def DecreasePrice(self, penetrationRatio) -> None:
        penetrationEffect = hlp.Logistic(
            b=1, L=-1, k=15, x0=1/3, input=penetrationRatio)
        indicatedReduction = penetrationEffect * \
            self.__normalReductionRate*self.currentPrice
        limitEffect = self.__GetLimitEffect(
            self.currentPrice-indicatedReduction)
        self.__priceHistory.append(self.currentPrice)
        self.currentPrice = self.currentPrice-indicatedReduction*limitEffect

    def __GetLimitEffect(self, tempPrice) -> float:
        ratio = self.__minimumPrice/tempPrice
        result = hlp.Logistic(b=1, L=-1, k=15, x0=1/3, input=ratio)
        return result