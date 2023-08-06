class ElectricityTariff:
    def __init__(self, initialTariff: float) -> None:
        # self.__initialTariff = initialTariff
        self.__history = [(0, initialTariff)]
        self.currentPrice = initialTariff

    def SetNewTariff(self, time, newTariff: float) -> None:
        self.__history.append((time, self.currentPrice))
        self.currentPrice = newTariff

    def GetPriceChangeValue(self) -> float:
        return self.currentPrice - self.__history[-1][1]

    def GetPriceChangeRatio(self) -> float:
        return self.GetPriceChangeValue() / self.__history[-1][1]

    def GetHistory(self):
        return self.__history
