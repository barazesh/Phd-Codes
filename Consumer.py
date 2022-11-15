import numpy as np
from ElectricityTariff import ElectricityTariff
from Helper import Logistic


class Consumer:
    def __init__(self, initialNumber, initialMonthlyDemand, priceElasticity, demandChangeLimit) -> None:
        self.__numberHistory = []
        self.__demandHistory = []
        self.__priceElasticity = priceElasticity
        self.__demandChangeLimit = demandChangeLimit
        self.currentNumber = initialNumber
        self.monthlyDemand = initialMonthlyDemand


    def ChangeDemand(self,tariff:ElectricityTariff)->None:
        self.__demandHistory.append(self.monthlyDemand)
        indicatedChange = self.__priceElasticity*tariff.GetPriceChange()*self.monthlyDemand/tariff.currentPrice
        limitEffect = self.__GetLimitEffect(indicatedChange)
        self.monthlyDemand = self.monthlyDemand +indicatedChange*limitEffect

    def __GetLimitEffect(self,input)->float:
        ratio = input/self.monthlyDemand/self.__demandChangeLimit
        result=Logistic(b=1,L=-1,k=15,x0=1/3,input=ratio)
        return result

    def ChangeNumber(self,value)->None:
        self.__numberHistory.append(self.currentNumber)
        self.currentNumber = self.currentNumber +value

    def GetNumberHistory(self):
        return self.__numberHistory