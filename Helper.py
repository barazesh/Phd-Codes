import numpy as np


def Logistic(b,L,k,x0,input)-> float:
    return b+ L/(1+np.exp(-k*(input-x0)))

def ConvertYearly2MonthlyRate(yearly):
        return ((1+yearly)**(1/12)-1)

def Logistic4RatioLimit(input)->float:
        result = Logistic(b=1, L=-1, k=25, x0=0.7, input=input)
        return result