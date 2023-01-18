import numpy as np
import Helper as hlp


class PV:
    def __init__(self, initialPrice, normalReductionRate, minimumPrice, effectiveLife, monthlyEnergyOutput,hourlyEnergyOutput:np.ndarray) -> None:
        self.__priceHistory = []
        self.currentPrice = initialPrice
        self.__minimumPrice = minimumPrice
        self.__normalReductionRate = normalReductionRate
        self.effectiveLife = effectiveLife
        self.monthlyEnergyOutput = monthlyEnergyOutput
        self.hourlyEnergyOutput = hourlyEnergyOutput


    def ConvertYearly2MonthlyRate(self, yearly):
        return ((1+yearly)**(1/12)-1)

    def DecreasePrice(self, penetrationRatio) -> None:
        penetrationEffect = hlp.Logistic(
            b=1, L=0.5, k=15, x0=1/3, input=penetrationRatio)
        indicatedReduction = penetrationEffect * \
            self.__normalReductionRate*self.currentPrice
        limitEffect = self.__CalculateLimitEffect(
            self.currentPrice-indicatedReduction)
        self.__priceHistory.append(self.currentPrice)
        self.currentPrice = self.currentPrice-indicatedReduction*limitEffect

    def __CalculateLimitEffect(self, tempPrice) -> float:
        ratio = self.__minimumPrice/tempPrice
        return hlp.Logistic4RatioLimit(ratio)

    def CalculateNPV(self, electricityPrice:float, interestRate:float) -> float:
        I = self.monthlyEnergyOutput*electricityPrice
        NPVI = I*((1+interestRate)**self.effectiveLife+1) / interestRate
        result = NPVI-self.currentPrice
        return result

