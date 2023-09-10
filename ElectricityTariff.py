class ElectricityTariff:
    def __init__(self, initialFixedTariff: float,initialVariableTariff: float) -> None:
        self.__history = [{'time':0, 'fixed':initialFixedTariff,'variable':initialVariableTariff}]
        self.currentFixedPrice = initialFixedTariff
        self.currentVariablePrice = initialVariableTariff

    def SetNewTariff(self, time:int, variablePriceChange:float, fixedPriceChange:float) -> None:
        temp={
            'time':time,
            'fixed':self.currentFixedPrice,
            'variable':self.currentVariablePrice
        }
        self.__history.append(temp)
        self.currentFixedPrice += fixedPriceChange
        self.currentVariablePrice += variablePriceChange

    def GetPriceChangeValue(self) -> dict:
        result={
            'fixed':self.currentFixedPrice-self.__history[-1]['fixed'],
            'variable':self.currentVariablePrice-self.__history[-1]['variable']
        }
        return result

    def GetPriceChangeRatio(self) -> dict:
        priceChange=self.GetPriceChangeValue()
        result={}
        for k in priceChange.keys():
            result[k]=priceChange[k]/ self.__history[-1][k]
        return result

    def GetHistory(self):
        return self.__history
