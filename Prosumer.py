import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
from PV import PV
import Helper as hlp



class Prosumer(Consumer):
    def __init__(self, initialNumber, initialDemandProfile, priceElasticity, demandChangeLimit,PVSystem:PV,PVSize:int) -> None:
        super().__init__(initialNumber, initialDemandProfile, priceElasticity, demandChangeLimit)

        self.PVSystem=PVSystem
        self.PVSystemSize=PVSize

    def __CalculateNetDemand(self):
        return self.demandProfile-self.PVSystem.hourlyEnergyOutput*self.PVSystemSize

    def GetMonthlyConsumption(self,time:float):
        month = np.ceil(time%12)
        first = hlp.CalculateFirstHour(month)
        last = hlp.CalculateLastHour(month)
        if last ==-1:
            consumption = np.sum(self.demandProfile[first:])
        else:
            consumption = np.sum(self.demandProfile[first:last])

        return consumption

        



