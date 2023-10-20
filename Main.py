import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
import numpy as np
from PV import PV
from Environment import Environment
import pandas as pd
import visualization
import json

duration = 240
timeStep = 1
time = range(0, duration + timeStep, timeStep)


def AddProfilestoInputData(inputdata: dict, profilesPath: str):
    hourlyData = pd.read_csv(profilesPath, index_col=0)
    inputdata["PVHourlyEnergyOutput"] = hourlyData["Solar Output"].to_numpy()
    inputdata["ConsumptionProfile"] = hourlyData["Demand"].to_numpy()

def AddUtilityFinancialtoInputData(inputdata: dict, fielpath: str):
    starting_year=2010
    data=pd.read_csv(fielpath,index_col=0)
    for c in data.columns:
        res=linregress(data[c].dropna().index,data[c].dropna())
        temp= [res.slope*y + res.intercept for y in range(2010,2050)]
        result =[item/12 for item in temp for _ in range(12)]
        if 'cost' in c.lower():
            inputdata['fixedCosts']=result
        elif 'ratebase' in c.lower():
            inputdata['rateBase']=result



        


def main():
    RunBaseCae("California")

    # RunSensitivityAnalysis(
    #     case="California",
    #     parameter="fixed2VariableRatio",
    #     evaluationRange=np.arange(0,0.4,0.1).tolist(),
    # )
    # RunSensitivityAnalysis(
    #     case="California",
    #     parameter="rateCorrectionFreq",
    #     evaluationRange=list(range(12, 40, 6)),
    # )
    # RunSensitivityAnalysis(
    #     case="California",
    #     parameter="fixed2VariableRatio",
    #     evaluationRange=[0, 0.1, 0.2, 0.3],
    # )


def RunBaseCae(case: str):
    inputData = json.load(open(f"./Data/{case}.json"))
    AddProfilestoInputData(inputdata=inputData, profilesPath="./Data/LosAngles.csv")
    AddUtilityFinancialtoInputData(inputdata=inputData, fielpath="/.Data/SCE_financial.csv")
    index = time
    Env = Environment(inputData=inputData)
    for t in time:
        if t == 0:
            continue
        print(t)
        Env.Iterate(t)
    result=Env.GetResults(list(index))
    # print(f"{result.loc[120,['Prosumers','Defectors']]}")
    # print(f"total with PV: {result.loc[120,['Prosumers','Defectors']].sum()}")
    # print(f"defector share: {result.loc[120,'Defectors']/result.loc[120,['Prosumers','Defectors']].sum()}")
    result.to_csv("./Outputs/baseCaseResults.csv")
    visualization.PlotBaseCase()


def RunSensitivityAnalysis(case: str, parameter: str, evaluationRange: list):
    inputData = json.load(open(f"./Data/{case}.json"))
    temp = {}
    index = time
    # for p in period:
    for s in evaluationRange:
        AddProfilestoInputData(inputdata=inputData, profilesPath="./Data/LosAngles.csv")
        print(f"###{parameter}:{s}###")
        inputData[parameter] = s
        Env = Environment(inputData)
        for t in time:
            if t != 0:
                print(t, end="\r")
                Env.Iterate(t)
        temp[str(s)] = Env.GetResults(list(index))

    vars = temp[str(evaluationRange[0])].columns
    # result = {}
    with pd.ExcelWriter(f"./Outputs/sensitivity_{parameter}.xlsx") as writer:
        for v in vars:
            df = pd.DataFrame(index=index)
            for s in temp.keys():
                df[s] = temp[s][v]
            df.to_excel(writer, sheet_name=v)
    visualization.PlotSensitivity(parameter)


def PlotResults(input):
    mpl.rc("lines", linewidth=1, markersize=4)
    mpl.rc("grid", linewidth=0.5, linestyle="--")
    plt.rcParams["axes.grid"] = True
    mpl.rc("font", size=8, family="Times New Roman")
    vars = ["Tariff"]
    for v in vars:
        fig, ax = plt.subplots(figsize=(6, 3.7))
        input[v].plot(ax=ax)
        ax.set_xlabel("Time (Month)")
        ax.set_xlim(-5, 245)
        ax.set_title("Electricity tariff")
        ax.set_ylabel("Price (dollar)")
        fig.savefig(f"{v}_period.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
