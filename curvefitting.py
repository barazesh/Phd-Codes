from scipy.optimize import curve_fit as cf
from scipy import stats
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

def main():
    directoryPath = Path.cwd().joinpath('Outputs')
    params = Batch_Fitting(directoryPath)
    params.to_excel(directoryPath.joinpath('fitting_params_period.xlsx'))
    # params['f2'].plot()
    # print(params)

def Batch_Fitting(directoryPath):
    data = ExtractData(directoryPath,'period')
    maxTime=data.idxmax()
    n_rows= math.ceil(len(data.columns)/2)
    fig,ax =plt.subplots(n_rows,2,sharex=True)
    fig.set_size_inches(20,n_rows*5)

    params=pd.DataFrame(columns=['a1','b1','c1','d1','f1','phi1','a2','b2','c2','d2','f2','phi2'])
    for i,p in enumerate(data.columns):
        first_x, first_line, second_x, second_line, sin_pars1,sin_pars2 = Fit_Sinus_Line(data[p], maxTime[p])
        params.loc[p]=[*sin_pars1,*sin_pars2]
        cur_ax=ax[i//2,i%2]
        cur_ax.set_title(p)
        cur_ax.plot(data.loc[:maxTime[p],p])
        cur_ax.plot(data.loc[maxTime[p]:,p])
        cur_ax.plot(first_x,sinus_line_line(first_x,*sin_pars1))
        cur_ax.plot(second_x,sinus_line_line(second_x,*sin_pars2))
        cur_ax.plot(first_x,first_line.slope*first_x+first_line.intercept)
        cur_ax.plot(second_x,second_line.slope*second_x+second_line.intercept)
        total_x=data.index.to_numpy()
        total_y=data[p].to_numpy()
        # ax[i].plot(total_x,sinus(total_x,0,*sin_pars[1:]))
    plt.show()
    # for i,p in enumerate(data.columns):
    #     first_x, first_line, second_x, second_line, sin_pars1,sin_pars2 = Fit_Sinus_Line(data[p], maxTime[p])
    #     params.loc[p]=[*sin_pars1,*sin_pars2]
    #     plt.title(label=p)
    #     plt.plot(data.loc[:maxTime[p],p])
    #     plt.plot(data.loc[maxTime[p]:,p])
    #     plt.plot(first_x,sinus_line_line(first_x,*sin_pars1))
    #     plt.plot(second_x,sinus_line_line(second_x,*sin_pars2))
    #     plt.plot(first_x,first_line.slope*first_x+first_line.intercept)
    #     plt.plot(second_x,second_line.slope*second_x+second_line.intercept)
    #     plt.show()
    return params

def Fit_Sinus_Line(data, maxTime):
    first_x=data[:maxTime].index.to_numpy()
    first_y=data[:maxTime].to_numpy()
    first_line=stats.linregress(x=first_x,y=first_y)
    second_x=data[maxTime:].index.to_numpy()
    second_y=data[maxTime:].to_numpy()
    second_line=stats.linregress(x=second_x,y=second_y)
    siny=second_y-(second_line.slope*second_x+second_line.intercept)
    a,b,f,phi = Estimate_Sinus_Params(second_x, siny)
    sin_pars1, cov = cf(f=sinus_line_line,xdata=first_x,ydata=first_y,p0=[first_line.slope,first_line.intercept,first_line.slope,b,f,0], maxfev=14000)
    sin_pars2, cov = cf(f=sinus_line_line,xdata=second_x,ydata=second_y,p0=[second_line.slope,second_line.intercept,second_line.slope,b,f,phi], maxfev=14000)
    return first_x,first_line,second_x,second_line,sin_pars1,sin_pars2

def Estimate_Sinus_Params(x, y):
    a=np.average(y)
    b=np.max(y)        
    T=np.median(np.diff(x[np.nonzero(np.diff(np.sign(y)))[0]]))
    f=1/(2*T)
    phi=np.arcsin(y[0]/b)-2*np.pi*f*x[0]
    return a,b,f,phi

def ExtractData(directoryPath,sensitivity_var):
    data=pd.DataFrame()
    for s in directoryPath.glob(f'{sensitivity_var}_*.csv'):
        sv = float(s.stem.split('_')[1])
        result=pd.read_csv(s,squeeze=True,index_col=0,dtype='float64')
        data[sv]=result['Electricity Tariff']
    data.sort_index(axis=1,inplace=True)
    return data


def sinus(x,a,b,f,phi):
    return a+b*np.sin(x*2*np.pi*f+phi)

def sinus_line_line(x,a,b,c,d,f,phi):
    return a*x+b+(c*x+d)*np.sin(x*2*np.pi*f+phi)

if __name__=='__main__':
    main()