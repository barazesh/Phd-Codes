import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
import Helper as hlp


class RegularConsumer(Consumer):
    pass

    def GetMonthlyConsumption(self, month: int)-> float:
        month = int(np.ceil(month % 12)) if (month % 12)>0 else 12
        result = np.sum(hlp.SliceMonth(
            array=self.demandProfile, month=month))
        return result