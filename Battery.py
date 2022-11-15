import numpy as np
from Helper import Logistic


class Battery:
    def __init__(self, initialPrice, normalReductionRate, minimumPrice) -> None:
        self.__initialPrice = initialPrice
        self.history = [initialPrice]
        self.currentPrice = initialPrice
        self.__minimumPrice = minimumPrice
        self.__normalReductionRate = normalReductionRate

    def DecreasePrice(self,penetrationRatio) -> None:
        effect= Logistic(b=1, L=-1, k=15, x0=1/3, input=penetrationRatio)
        self.currentPrice = (1-effect*self.__normalReductionRate)*self.history[-1]
        self.history.append(self.currentPrice)