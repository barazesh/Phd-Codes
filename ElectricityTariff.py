class ElectricityTariff:
    def __init__(self, initialTariff) -> None:
        self.__initialTariff = initialTariff
        self.__history = [(0,initialTariff)]
        self.currentPrice = initialTariff

    def SetNewTariff(self,time,newTariff:float)->None:
        self.__history.append((time,self.currentPrice))
        self.currentPrice = newTariff

    def GetPriceChange(self)->float:
        return self.currentPrice - self.__history[-1][1]

    def GetHistory(self):
        return self.__history

