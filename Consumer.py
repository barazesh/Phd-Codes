import numpy as np
from ElectricityTariff import ElectricityTariff
from Helper import Logistic
import Helper as hlp


class Consumer:
    def __init__(self, initialNumber: int, initialDemandProfile: np.ndarray, priceElasticity: float, demandChangeLimit: float) -> None:
        self.__numberHistory = [float(initialNumber)]
        self.__demandChangeHistory = []
        self.__priceElasticity = priceElasticity
        self.__demandChangeLimit = demandChangeLimit
        self.currentNumber = initialNumber
        self.demandProfile = initialDemandProfile

    def ChangeDemand(self, tariff: ElectricityTariff) -> None:

        indicatedChange = self.__priceElasticity*tariff.GetPriceChangeRatio()
        limitEffect = self.__GetLimitEffect(indicatedChange)
        changeFactor = 1+indicatedChange*limitEffect
        self.__demandChangeHistory.append(changeFactor)
        # TODO: implement the change in demand correctly
        # self.monthlyDemand = self.monthlyDemand*changeFactor
        self.demandProfile *= changeFactor

    def __GetLimitEffect(self, input: float) -> float:
        ratio = input/self.__demandChangeLimit
        result = Logistic(b=1, L=-1, k=15, x0=1/3, input=ratio)
        return result

    def ChangeNumber(self, value: float) -> None:
        self.__numberHistory.append(self.currentNumber)
        self.currentNumber = self.currentNumber + value

    def GetNumberHistory(self)->np.ndarray:
        return np.array(self.__numberHistory)
