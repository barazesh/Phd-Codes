class ElectricityTariff:
    def __init__(self, initialFixedTariff: float,initialVariableTariff: float) -> None:
        self._history = [{'time':0, 'fixed':initialFixedTariff,'variable':initialVariableTariff}]
        self.currentFixedPrice = initialFixedTariff
        self.currentVariablePrice = initialVariableTariff

    def SetTariffbyChange(self, time:int, variablePriceChange:float, fixedPriceChange:float) -> None:
        self.currentFixedPrice += fixedPriceChange
        if self.currentFixedPrice < 0:
            self.currentFixedPrice=0
        self.currentVariablePrice += variablePriceChange
        if self.currentVariablePrice < 0:
            self.currentVariablePrice=0
        self.AppendHistory(time)

    def SetTariffbvNewValue(self, time:int, new_variablePrice:float, new_fixedPrice:float) -> None:
        self.currentFixedPrice = new_fixedPrice
        if self.currentFixedPrice < 0:
            self.currentFixedPrice=0
        self.currentVariablePrice = new_variablePrice
        if self.currentVariablePrice < 0:
            self.currentVariablePrice=0
        self.AppendHistory(time)

    def AppendHistory(self, time):
        temp={
            'time':time,
            'fixed':self.currentFixedPrice,
            'variable':self.currentVariablePrice
        }
        self._history.append(temp)

    def GetPriceChangeValue(self) -> dict:
        result={
            'fixed':self._history[-1]['fixed']-self._history[-2]['fixed'],
            'variable':self._history[-1]['variable']-self._history[-2]['variable']
        }
        return result

    def GetPriceChangeRatio(self) -> dict:
        priceChange=self.GetPriceChangeValue()
        result={}
        for k in priceChange.keys():
            if self._history[-2][k] == 0:
                result[k]=priceChange[k]/ 1e-5
            else:
                result[k]=priceChange[k]/ self._history[-2][k]
        return result

    def GetHistory(self):
        return self._history
