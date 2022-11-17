import numpy as np


def Logistic(b,L,k,x0,input)-> float:
    return b+ L/(1+np.exp(-k*(input-x0)))

def ConvertYearly2MonthlyRate(yearly):
        return ((1+yearly)**(1/12)-1)

