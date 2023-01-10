import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
import Helper as hlp


class RegularConsumer(Consumer):
    pass

    def GetMonthlyConsumption(self, time: float)-> float:
        month = np.ceil(time % 12)
        result = np.sum(hlp.SliceMonth(
            array=self.demandProfile, month=month))
        return result