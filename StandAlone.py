from Battery import Battery
from ElectricityTariff import ElectricityTariff
from PV import PV


class StandAloneSystem:
    def __init__(self, pv: PV, battery: Battery) -> None:
        self.__pv = pv
        self.__battery = battery

    def CalculateNPV(self,interestRate,elecTariff:ElectricityTariff,monthlyDemand) -> float:
        pvSize = self.__CalculatePVSize(monthlyDemand)
        batterySize = self.__CalculateBatterySize(monthlyDemand)
        cost = pvSize*self.__pv.currentPrice+batterySize*self.__battery.currentPrice * \
            int(self.__pv.effectiveLife/self.__battery.effectiveLife)
        saving = self.__CalculateSaving(interestRate, elecTariff, monthlyDemand)
        return saving-cost

    def __CalculateSaving(self, interestRate, elecTariff, monthlyDemand):
        saving= elecTariff.currentPrice*monthlyDemand*((1+interestRate)**self.__pv.effectiveLife+1) / interestRate
        return saving
    def __CalculateBatterySize(self,monthlyDemand) -> int:
        result = int(0.5*monthlyDemand/30)+1
        return result

    def __CalculatePVSize(self,monthlyDemand) -> int:
        result = int(monthlyDemand*1.5/self.__pv.monthlyEnergyOutput)+1
        return result
