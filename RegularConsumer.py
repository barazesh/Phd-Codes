import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
import Helper as hlp


class RegularConsumer(Consumer):
    pass

    def GetMonthlyConsumption(self, month: int) -> float:
        moy = hlp.GetMonthofYear(month)
        result = np.sum(
            hlp.SliceMonth(array=self.DemandProfile, month=moy), dtype=float
        )
        return result

    def GetYearlyConsumption(self) -> float:
        return np.sum(self.DemandProfile, dtype=float)

    def GetYearlyExpenditure(self, consumptionTariff: ElectricityTariff) -> float:
        demand = self.GetYearlyConsumption()
        fixedEx= 12*consumptionTariff.currentFixedPrice
        variableEx= demand * consumptionTariff.currentVariablePrice

        return fixedEx+variableEx
