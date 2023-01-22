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
