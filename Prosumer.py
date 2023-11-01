import numpy as np
from Consumer import Consumer
from ElectricityTariff import ElectricityTariff
from PV import PV
import Helper as hlp


class Prosumer(Consumer):
    def __init__(
        self,
        initialNumber,
        initialDemandProfile,
        priceElasticity,
        demandChangeLimit,
        PVSystem: PV,
        PVSize: int,
    ) -> None:
        super().__init__(
            initialNumber, initialDemandProfile, priceElasticity, demandChangeLimit
        )

        self.PVSystem = PVSystem
        self.PVSystemSize = PVSize

    def _CalculateNetDemand(self) -> np.ndarray:
        return self.DemandProfile - self.PVSystem.hourlyEnergyOutput * self.PVSystemSize

    def GetMonthlyConsumption(self, month: int) -> float:
        moy = hlp.GetMonthofYear(month)
        net = self._CalculateNetDemand()
        consumptionOnly = [0 if i < 0 else i for i in net]
        result = np.sum(
            hlp.SliceMonth(array=np.array(consumptionOnly), month=moy), dtype=float
        )
        return result

    def GetMonthlyProduction(self, month: int) -> float:
        moy = hlp.GetMonthofYear(month)
        net = self._CalculateNetDemand()
        productionOnly = [0 if i > 0 else -i for i in net]
        result = np.sum(
            hlp.SliceMonth(array=np.array(productionOnly), month=moy), dtype=float
        )
        return result

    def GetYearlyExpenditure(
        self, consumptionTariff: ElectricityTariff, productionTariff: ElectricityTariff
    ) -> float:
        net = self._CalculateNetDemand()
        result = [
            i * consumptionTariff.currentVariablePrice
            if i > 0
            else i * productionTariff.currentVariablePrice
            for i in net
        ]
        return consumptionTariff.currentFixedPrice * 12 + np.sum(result, dtype=float)
