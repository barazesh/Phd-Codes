from Battery import Battery
from ElectricityTariff import ElectricityTariff
from PV import PV
import numpy as np
import Helper as hlp


class StandAloneSystem:
    def __init__(self, pv: PV, battery: Battery) -> None:
        self.__pv = pv
        self.__battery = battery

    def CalculateNPV(
        self, interestRate, elecTariff: ElectricityTariff, monthlyDemand
    ) -> float:
        pvSize = self.__CalculatePVSize(monthlyDemand)
        batterySize = self.__CalculateBatterySizeOld(monthlyDemand)
        cost = (
            pvSize * self.__pv.currentPrice
            + batterySize
            * self.__battery.currentPrice
            * int(self.__pv.effectiveLife / self.__battery.effectiveLife)
        )
        saving = self.__CalculateSaving(interestRate, elecTariff, monthlyDemand)
        return saving - cost

    def __CalculateSaving(self, interestRate, elecTariff, monthlyDemand):
        saving = (
            elecTariff.currentPrice
            * monthlyDemand
            * ((1 + interestRate) ** self.__pv.effectiveLife + 1)
            / interestRate
        )
        return saving

    def __CalculateBatterySizeOld(self, monthlyDemand) -> int:
        result = int(0.5 * monthlyDemand / 30) + 1
        return result

    def __CalculatePVSize(self, monthlyDemand) -> int:
        result = int(monthlyDemand * 1.5 / self.__pv.monthlyEnergyOutput) + 1
        return result

    def CalculateNPVnew(
        self,
        interestRate: float,
        elecTariff: ElectricityTariff,
        demandProfile: np.ndarray,
    ) -> float:
        _, _, cost = self.OptimizeSystemSize(demandProfile)
        saving = self.__CalculateSaving(
            interestRate, elecTariff, demandProfile.sum() / 12
        )

        return saving - cost

    def OptimizeSystemSize(self, demandProfile: np.ndarray):
        annaulPVGeneration = self.__pv.hourlyEnergyOutput.sum()
        annualDemand = demandProfile.sum()
        bestPVSize = annualDemand / annaulPVGeneration
        currentSystem = self.__DesignSystem(bestPVSize, demandProfile)
        bestSystem = currentSystem
        systems = []
        initial_temperature = 100
        for i in range(initial_temperature):
            temperature = initial_temperature / float(i + 1)
            newPVSize = currentSystem[0] + np.random.normal() * temperature
            newSystem = self.__DesignSystem(newPVSize, demandProfile)
            systems.append(newSystem)
            if bestSystem[2] > newSystem[2]:
                bestSystem = newSystem
            diff = newSystem[2] - currentSystem[2]
            threshold = np.exp(-diff / temperature)
            if (diff < 0) or (np.random.uniform() < threshold):
                currentSystem = newSystem
        return bestSystem

    def __DesignSystem(self, pvsize: float, demandProfile: np.ndarray):
        batsize = self.__CalculateBatterySize(pvsize, demandProfile)
        batterychanges = int(self.__pv.effectiveLife / self.__battery.effectiveLife)
        cost = (
            pvsize * self.__pv.currentPrice
            + batsize * self.__battery.currentPrice * batterychanges
        )
        return (pvsize, batsize, cost)

    def __CalculateBatterySize(self, PVsize: float, demandProfile: np.ndarray) -> float:
        targetViolation = 24
        tollerance = 5
        lower, upper = self.__FindRange(PVsize, demandProfile, targetViolation)

        while lower[1] - upper[1] > tollerance:
            # tempbattery=self.__FindMiddlePointAdaptive(targetViolation, lower, upper)
            tempbattery = self.__FindMiddlePoint(lower, upper)
            tempviolation = self.__EvaluateSystem(PVsize, tempbattery, demandProfile)
            if tempviolation > targetViolation:
                lower = (tempbattery, tempviolation)
            elif tempviolation < targetViolation:
                upper = (tempbattery, tempviolation)
            else:
                return tempbattery

        # print(f'second loop:{c}')
        return upper[0]

    def __FindRange(self, PVsize, demandProfile, targetViolation):
        mismatch = self.__pv.hourlyEnergyOutput * PVsize - demandProfile
        accumulatedMismatch = mismatch.cumsum()
        batterysize = np.abs(accumulatedMismatch).max()
        violation = self.__EvaluateSystem(PVsize, batterysize, demandProfile)
        newbatterysize = batterysize
        newviolation = violation

        c = 0
        while (targetViolation - violation) * (targetViolation - newviolation) > 0:
            batterysize = newbatterysize
            violation = newviolation
            if violation == 0:
                m = 1 / targetViolation
            else:
                m = violation / targetViolation
            newbatterysize = batterysize * m
            newviolation = self.__EvaluateSystem(PVsize, newbatterysize, demandProfile)
            c += 1

        # print(f'PV Size:{PVsize}')
        # print(f'first loop:{c}')

        if newviolation > violation:
            lower = (newbatterysize, newviolation)
            upper = (batterysize, violation)
        else:
            upper = (newbatterysize, newviolation)
            lower = (batterysize, violation)
        return lower, upper

    def __FindMiddlePointAdaptive(self, targetViolation, lower, upper):
        L = lower[1] - targetViolation
        U = targetViolation - upper[1]
        a = U / (U + L)
        result = a * lower[0] + (1 - a) * upper[0]
        return result

    def __FindMiddlePoint(self, lower, upper):
        a = 0.5
        tempbattery = a * lower[0] + (1 - a) * upper[0]
        return tempbattery

    def __EvaluateSystem(
        self, pvsize: float, batterySize: float, demandProfile: np.ndarray
    ) -> int:
        (result, violation) = hlp.cumsum_with_limits(
            input=pvsize * self.__pv.hourlyEnergyOutput - demandProfile,
            initialValue=batterySize * 0.8,
            upperLimit=batterySize,
            lowerLimit=0,
        )
        return violation
