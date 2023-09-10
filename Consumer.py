import numpy as np
from ElectricityTariff import ElectricityTariff
from Helper import Logistic
import Helper as hlp


class Consumer:
    def __init__(
        self,
        initialNumber: int,
        initialDemandProfile: np.ndarray,
        priceElasticity: float,
        demandChangeLimit: float,
    ) -> None:
        self.__numberHistory = [float(initialNumber)]
        self.__demandChangeHistory = []
        self.__priceElasticity = priceElasticity
        self.__demandChangeLimit = demandChangeLimit
        self.currentNumber = initialNumber
        self.__demandProfile = initialDemandProfile

    def ChangeDemand(self, tariff: ElectricityTariff) -> None:

        indicatedChange = self.__priceElasticity * tariff.GetPriceChangeRatio()['variable']
        limitEffect = self.__GetLimitEffect(indicatedChange)
        changeFactor = 1 + indicatedChange * limitEffect
        self.__demandChangeHistory.append(changeFactor)
        # TODO: implement the change in demand correctly
        # self.monthlyDemand = self.monthlyDemand*changeFactor
        self.__demandProfile *= changeFactor

    def __GetLimitEffect(self, input: float) -> float:
        ratio = np.abs(input) / self.__demandChangeLimit
        result = Logistic(b=1, L=-1, k=15, x0=1 / 3, input=ratio)
        if result < 1e-6:
            result = 0.2/input
        return result

    def ChangeNumber(self, value: float) -> None:
        self.__numberHistory.append(self.currentNumber)
        self.currentNumber = self.currentNumber + value

    def GetNumberHistory(self) -> np.ndarray:
        return np.array(self.__numberHistory)
    
    def _GetDemandProfile(self):
        return self.__demandProfile
    
    DemandProfile = property(fget=_GetDemandProfile)
