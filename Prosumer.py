import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
from PV import PV
import Helper as hlp


class Prosumer(Consumer):
    def __init__(self, initialNumber, initialDemandProfile, priceElasticity, demandChangeLimit, PVSystem: PV, PVSize: int) -> None:
        super().__init__(initialNumber, initialDemandProfile,
                         priceElasticity, demandChangeLimit)

        self.PVSystem = PVSystem
        self.PVSystemSize = PVSize

    def __CalculateNetDemand(self)->list:
        return self.demandProfile-self.PVSystem.hourlyEnergyOutput*self.PVSystemSize

    def GetMonthlyConsumption(self, month: float) -> float:
        net = self.__CalculateNetDemand()
        consumptionOnly = [0 if i < 0 else i for i in net]
        result = np.sum(hlp.SliceMonth(
            array=np.array(consumptionOnly), month=month))
        return result

    def GetMonthlyProduction(self, month: float) -> float:
        net = self.__CalculateNetDemand()
        productionOnly = [0 if i > 0 else -i for i in net]
        result = np.sum(hlp.SliceMonth(
            array=np.array(productionOnly), month=month))
        return result

    def CalculateNPV(self,tariff:ElectricityTariff):
        pass