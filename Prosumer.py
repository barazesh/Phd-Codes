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

    def __CalculateNetDemand(self)->np.ndarray:
        return self.demandProfile-self.PVSystem.hourlyEnergyOutput*self.PVSystemSize

    def GetMonthlyConsumption(self, month: int) -> float:
        month = int(np.ceil(month % 12)) if (month % 12)>0 else 12
        net = self.__CalculateNetDemand()
        consumptionOnly = [0 if i < 0 else i for i in net]
        result = np.sum(hlp.SliceMonth(
            array=np.array(consumptionOnly), month=month))
        return result

    def GetMonthlyProduction(self, month: int) -> float:
        month = int(np.ceil(month % 12)) if (month % 12)>0 else 12
        net = self.__CalculateNetDemand()
        productionOnly = [0 if i > 0 else -i for i in net]
        result = np.sum(hlp.SliceMonth(
            array=np.array(productionOnly), month=month))
        return result

    def CalculateNPV(self,consumptionTariff:ElectricityTariff,productionTariff:ElectricityTariff,interestRate:float)->float:
        pvCost=self.PVSystem.currentPrice*self.PVSystemSize
        pvIncome=0
        for i,e in enumerate(self.PVSystem.hourlyEnergyOutput):
            if e > self.demandProfile[i]: #Prosumer in production mode
                pvIncome+=e*productionTariff.currentPrice
            else:
                pvIncome+=e*consumptionTariff.currentPrice
        pvIncomeNPV=(pvIncome/12)*((1+interestRate)**self.PVSystem.effectiveLife+1) / interestRate
        return pvIncomeNPV-pvCost

        

