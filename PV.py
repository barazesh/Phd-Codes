import numpy as np

from Helper import Logistic


class PV:
    def __init__(self, initialPrice, normalReductionRate, minimumPrice, effectiveLife, monthlyEnergyOutput, interestRate) -> None:
        self.__initialPrice = initialPrice
        self.__priceHistory = []
        self.currentPrice = initialPrice
        self.__minimumPrice = minimumPrice
        self.__normalReductionRate = normalReductionRate
        self.__effectiveLife = effectiveLife
        self.__monthlyEnergyOutput = monthlyEnergyOutput
        self.__interestRate = ((1+interestRate)**(1/12)-1)

    def DecreasePrice(self, penetrationRatio) -> None:
        penetrationEffect = Logistic(b=1, L=-1, k=15, x0=1/3, input=penetrationRatio)
        indicatedReduction = penetrationEffect * \
            self.__normalReductionRate*self.currentPrice
        tempPrice = self.currentPrice-indicatedReduction
        limitEffect = self.__GetLimitEffect(tempPrice)
        self.__priceHistory.append(self.currentPrice)
        self.currentPrice = self.currentPrice-indicatedReduction*limitEffect

    def __GetLimitEffect(self, tempPrice) -> float:
        ratio = self.__minimumPrice/tempPrice
        result = Logistic(b=1, L=-1, k=15, x0=1/3, input=ratio)
        return result

    def CalculateNPV(self, electricityPrice) -> float:
        I = self.__monthlyEnergyOutput*electricityPrice
        NPVI = I*((1+self.__interestRate)**self.__effectiveLife+1) / \
            self.__interestRate
        result = NPVI-self.currentPrice
        return result
