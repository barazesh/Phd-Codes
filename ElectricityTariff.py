class ElectricityTariff:
    def __init__(self, initialFixedTariff: float,initialVariableTariff: float) -> None:
        self.__history = [{'time':0, 'fixed':initialFixedTariff,'variable':initialVariableTariff}]
        self.currentFixedPrice = initialFixedTariff
        self.currentVariablePrice = initialVariableTariff

    def ChangeTariff(self, time:int, variablePriceChange:float, fixedPriceChange:float) -> None:
        temp={
            'time':time,
            'fixed':self.currentFixedPrice,
            'variable':self.currentVariablePrice
        }
        self.__history.append(temp)
        self.currentFixedPrice += fixedPriceChange
        if self.currentFixedPrice < 0:
            self.currentFixedPrice=0
        self.currentVariablePrice += variablePriceChange
        if self.currentVariablePrice < 0:
            self.currentVariablePrice=0

    def SetNewTariff(self, time:int, new_variablePrice:float, new_fixedPrice:float) -> None:
        temp={
            'time':time,
            'fixed':self.currentFixedPrice,
            'variable':self.currentVariablePrice
        }
        self.__history.append(temp)
        self.currentFixedPrice = new_fixedPrice
        if self.currentFixedPrice < 0:
            self.currentFixedPrice=0
        self.currentVariablePrice = new_variablePrice
        if self.currentVariablePrice < 0:
            self.currentVariablePrice=0

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
            if self.__history[-1][k] == 0:
                result[k]=priceChange[k]/ 1e-5
            else:
                result[k]=priceChange[k]/ self.__history[-1][k]
        return result

    def GetHistory(self):
        return self.__history
