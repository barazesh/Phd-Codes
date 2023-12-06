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
        self._numberHistory = [float(initialNumber)]
        self._demandChangeHistory = [1]
        self._priceElasticity = priceElasticity
        self._demandChangeLimit = demandChangeLimit
        self.currentNumber = initialNumber
        self._demandProfile = initialDemandProfile

    def ChangeDemand(self, tariff: ElectricityTariff) -> None:

        indicatedChange = self._priceElasticity * tariff.GetPriceChangeRatio()['variable']
        limitEffect = self.__GetLimitEffect(indicatedChange)
        changeFactor = 1 + indicatedChange * limitEffect
        self._demandChangeHistory.append(changeFactor)
        # TODO: implement the change in demand correctly
        # self.monthlyDemand = self.monthlyDemand*changeFactor
        self._demandProfile *= changeFactor

    def __GetLimitEffect(self, input: float) -> float:
        if np.abs(input) < self._demandChangeLimit:
            return 1
        else:
            return self._demandChangeLimit/np.abs(input)

        ratio = np.abs(input) / self._demandChangeLimit
        result = Logistic(b=1, L=-1, k=60, x0=0.9, input=ratio)
        if result < 1e-6:
            result = 0.1/input
        return result

    def ChangeNumber(self, value: float) -> None:
        self._numberHistory.append(self.currentNumber)
        self.currentNumber = self.currentNumber + value

    def GetNumberHistory(self) -> np.ndarray:
        return np.array(self._numberHistory)
    
    def _GetDemandProfile(self):
        return self._demandProfile
    
    DemandProfile = property(fget=_GetDemandProfile)
