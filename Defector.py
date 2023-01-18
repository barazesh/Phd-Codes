from Consumer import Consumer
from PV import PV
from Battery import Battery
import numpy as np


class Defector(Consumer):
    def __init__(self, initialNumber, initialDemandProfile, priceElasticity, demandChangeLimit, PVSystem: PV, battery: Battery) -> None:
        super().__init__(initialNumber, initialDemandProfile,
                         priceElasticity, demandChangeLimit)
        self.PVSystem = PVSystem
        self.Battery = battery

    def OptimizeSystemSize(self):
        annaulPVGeneration=self.PVSystem.hourlyEnergyOutput.sum()
        annualDemand=self.demandProfile.sum()
        minPVSize=annualDemand/annaulPVGeneration
        maxPVSize=4*minPVSize
        batsize=self.__CalculateBatterySize(minPVSize)
        batsize1=self.__CalculateBatterySize(maxPVSize)
        

    def __CalculateBatterySize(self,PVsize:float)->float:
        mismatch=self.PVSystem.hourlyEnergyOutput*PVsize-self.demandProfile
        accumulatedMismatch=mismatch.cumsum()
        batterysize=np.abs(accumulatedMismatch)
        return max(batterysize)


