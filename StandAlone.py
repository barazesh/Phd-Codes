from Battery import Battery
from ElectricityTariff import ElectricityTariff
from PV import PV
import numpy as np
import Helper as hlp


class StandAloneSystem:
    def __init__(self, pv: PV, battery: Battery) -> None:
        self.__pv = pv
        self.__battery = battery

    def OptimizeSystemSize(self, demandProfile: np.ndarray):
        annaulPVGeneration = self.__pv.hourlyEnergyOutput.sum()
        annualDemand = demandProfile.sum()
        bestPVSize = annualDemand / annaulPVGeneration
        # bestPVSize = 32
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
        acceptableViolation = 24 #number of unsupported hours acceptable
        tollerance = 5 #number of unsupported hours acceptable
        lower, upper = self.__FindRange(PVsize, demandProfile, acceptableViolation)

        while lower[1] - upper[1] > tollerance:
            # tempbattery=self.__FindMiddlePointAdaptive(targetViolation, lower, upper)
            battery = self.__FindMiddlePoint(lower, upper)
            violations = self.__EvaluateSystem(PVsize, battery, demandProfile)
            if violations > acceptableViolation:
                lower = (battery, violations)
            elif violations < acceptableViolation:
                upper = (battery, violations)
            else:
                return battery

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

    def __FindMiddlePoint(self, lower, upper):
        return (lower[0] + upper[0]) / 2

    def __EvaluateSystem(
        self, pvsize: float, batterySize: float, demandProfile: np.ndarray
    ) -> int:
        (_, violation) = hlp.cumsum_with_limits(
            input=pvsize * self.__pv.hourlyEnergyOutput - demandProfile,
            initialValue=batterySize * 0.8,
            upperLimit=batterySize,
            lowerLimit=0,
        )
        return violation
