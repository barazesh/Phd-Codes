import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px
from scipy.stats import linregress
from scipy.optimize import curve_fit
import numpy as np
from PV import PV
from Environment import Environment
import pandas as pd
import visualization
import json
import time

duration = 360
timeStep = 1
months = range(0, duration + timeStep, timeStep)


def AddProfilestoInputData(inputdata: dict, profilesPath: str):
    hourlyData = pd.read_csv(profilesPath, index_col=0)
    inputdata["PVHourlyEnergyOutput"] = hourlyData["Solar Output"].to_numpy()
    inputdata["ConsumptionProfile"] = (
        inputdata["AvgAnualResidentialConsumption"]
        * hourlyData["Demand"]
        / hourlyData["Demand"].sum()
    ).to_numpy()


def AddUtilityFinancialtoInputData(inputdata: dict, fielpath: str):
    starting_year = 2010
    end_year = 2050
    data = pd.read_csv(fielpath, index_col=0)
    for c in data.columns:
        if "ror" in c.lower():
            # result = [item for item in EstimateRoR_exp(data, starting_year, end_year) for _ in range(12)]
            # result = [item for item in EstimateRoR_line(data, starting_year, end_year) for _ in range(12)]
            result = [item for item in EstimateRoR_constant(data, starting_year, end_year) for _ in range(12)]
        else:
            res = linregress(data[c].dropna().index, data[c].dropna())
            temp = [
                1e6 * (res.slope * y + res.intercept) for y in range(starting_year, end_year)
            ]
            result = [item / 12 for item in temp for _ in range(12)]

        if "cost" in c.lower():
            inputdata["fixedCosts"] = result
        elif "ratebase" in c.lower():
            inputdata["rateBase"] = result
        elif "ror" in c.lower():
            inputdata["authorizedRoR"] = result


def EstimateRoR_exp(data: pd.DataFrame, starting_year: int, end_year: int):
    def exponential_curve(x, A, B, x_0):
        return A * B ** (x - x_0)

    x_data = data["RoR_permitted"].dropna().index
    y_data = data["RoR_permitted"].dropna()
    params, covariance = curve_fit(exponential_curve, x_data, y_data)
    est_A, est_B, est_x_0 = params

    starting_year = 2010
    fitted_curve = 1e-2*exponential_curve(
        range(starting_year, end_year), est_A, est_B, est_x_0
    )
    return fitted_curve


def EstimateRoR_line(data: pd.DataFrame, starting_year: int, end_year: int):
    x_data = data["RoR_permitted"].dropna().index
    y_data = data["RoR_permitted"].dropna()
    regression = linregress(x_data, y_data)
    result = [
        (regression.slope * y + regression.intercept) * 1e-2
        for y in range(starting_year, end_year)
    ]
    return result


def EstimateRoR_constant(data: pd.DataFrame, starting_year: int, end_year: int):
    result=[]
    for y in range(starting_year, end_year):
        if y in data["RoR_permitted"].dropna().index:
            result.append(float(data.loc[y,"RoR_permitted"])*1e-2)
        else:
            result.append(result[-1])

    return result


def main():
    # RunBaseCae("California")

    # RunSensitivityAnalysis(
    #     case="California",
    #     parameter="populationGrowthRate",
    #     evaluationRange=[0.002,0.005,0.015],
    # )
    # RunSensitivityAnalysis(
    #     case="California",
    #     parameter="rateCorrectionFreq",
    #     evaluationRange=list(range(12, 40, 12)),
    # )
    # RunSensitivityAnalysis(
    #     case="California",
    #     parameter="pvPotential",
    #     evaluationRange=[0.2,0.4,0.7],
    # )
    RunSensitivityAnalysis(
        case="California",
        parameter="fixed2VariableRatio",
        evaluationRange=[0, 0.2, 0.3],
    )


def RunBaseCae(case: str):
    inputData = json.load(open(f"./Data/{case}.json"))
    AddProfilestoInputData(inputdata=inputData, profilesPath="./Data/LosAngles.csv")
    AddUtilityFinancialtoInputData(
        inputdata=inputData, fielpath="./Data/SCE_financial.csv"
    )
    index = months
    Env = Environment(inputData=inputData)
    for t in months:
        if t == 0:
            continue
        print(t)
        Env.Iterate(t)
    result = Env.GetResults(list(index))
    # print(f"{result.loc[120,['Prosumers','Defectors']]}")
    # print(f"total with PV: {result.loc[120,['Prosumers','Defectors']].sum()}")
    # print(f"defector share: {result.loc[120,'Defectors']/result.loc[120,['Prosumers','Defectors']].sum()}")
    result.to_csv("./Outputs/baseCaseResults.csv")
    visualization.PlotBaseCase()


def RunSensitivityAnalysis(case: str, parameter: str, evaluationRange: list):
    inputData = json.load(open(f"./Data/{case}.json"))
    temp = {}
    index = months
    # for p in period:
    for s in evaluationRange:
        AddProfilestoInputData(inputdata=inputData, profilesPath="./Data/LosAngles.csv")
        AddUtilityFinancialtoInputData(
            inputdata=inputData, fielpath="./Data/SCE_financial.csv"
        )
        # for e in inputData.keys():
        #     if 'elasticity' in e.lower():
        #         inputData[e]=0
                
        print(f"###{parameter}:{s}###")
        inputData[parameter] = s
        Env = Environment(inputData)
        for t in months:
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
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print("Execution time:", elapsed_time, "seconds")
