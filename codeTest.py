import pysd
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def main():
    vensimDirectory='./Simulation Files/Prosumers & defectors'
    vensimFile ='net metering-no fixed tariff.mdl'
    filepath = Path(vensimDirectory,vensimFile)
    model = pysd.read_vensim(str(filepath))
    index=3
    paramaters={
        'population growth rate':0.001,
        'time to adjust Prosumer Demand':1,
        'time to adjust Regular Consumer demand':1,
        'Tariff Correction Period':3,
        'TIME STEP': 2**-index
        }
    price = model.run(params=paramaters,return_columns=['Electricity Tariff'])

    dif=differentiate(price.loc[:,'Electricity Tariff'].to_numpy(),index=index,period=paramaters['Tariff Correction Period'])

    (extrema_loc,extrema_val)=findExtrema(dif)

    calculateFrequency(extrema_loc)

def findExtrema(data):
    extrema_loc=[]
    extrema_val=[]
    for i,p in enumerate(data):
        if i!=0 and i!=len(data)-1:
            if (p < data[i+1] and p < data[i-1]) or (p > data[i+1] and p > data[i-1]):
                extrema_loc.append(i)
                extrema_val.append(p)
    print(extrema_loc)
    return (extrema_loc,extrema_val)

def differentiate(data,index,period):
    s=2**index
    dif=[]
    for i,p in enumerate(data):
        if (i-1)%(s*period)==0:
            dif.append(data[i]-data[i-1])
    return dif

def calculateFrequency(extrema_loc):
    distance=np.diff(extrema_loc)
    fr= 1/(2*np.mean(distance))
    # print(distance)
    # print(f'Average : {np.mean(distance)}')
    # print(f'Standard Deviation : {np.std(distance)}')
    # print(f'Variance : {np.var(distance)}')
    # print(f'Frequency : {fr}')
    return fr

if __name__ =='__main__':
    main()