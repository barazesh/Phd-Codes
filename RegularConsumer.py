import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
import Helper as hlp


class RegularConsumer(Consumer):
    pass

    def GetMonthlyConsumption(self, month: int) -> float:
        month = int(np.ceil(month % 12)) if (month % 12) > 0 else 12
        result = np.sum(
            hlp.SliceMonth(array=self.demandProfile, month=month), dtype=float
        )
        return result

    def GetYearlyConsumption(self) -> float:
        return np.sum(self.demandProfile, dtype=float)

    def GetYearlyExpenditure(self, consumptionTariff: ElectricityTariff) -> float:
        demand = self.GetYearlyConsumption()
        fixedEx= 12*consumptionTariff.currentFixedPrice
        variableEx= demand * consumptionTariff.currentVariablePrice

        return fixedEx+variableEx
