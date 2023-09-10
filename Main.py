import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from PV import PV
from Environment import Environment
import pandas as pd

duration = 240
timeStep = 1
time = range(0, duration + timeStep, timeStep)

inputdata = {
    "generationPrice": 0.06,
    "fixedCosts": 1.4e8,
    "fixed2VariableRatio":0,
    "permittedRoR": 0.15,
    "lossRate": 0.1,
    "initialFixedTariff": 0.001,
    "initialVariableTariff": 0.14,
    "rateCorrectionFreq": 12,
    # "populationGrowthRate": 0.00,
    "populationGrowthRate": 0.004,
    "innovationFactor": 0.01 / 12,
    "imitationFactor": 0.02 / 12,
    "initialRegularConsumerMonthlyDemand": 500,
    "regularConsumerPriceElasticity": -0.1,
    # "regularConsumerPriceElasticity": 0,
    "regularConsumerDemandChangeLimit": 0.2,
    "initialProsumerMonthlyDemand": 275,
    # "prosumerPriceElasticity": 0,
    "prosumerPriceElasticity": -0.2,
    "prosumerDemandChangeLimit": 0.2,
    "BatteryEffectiveLife": 7,
    "initialBatteryPrice": 600,
    "initialPVPrice": 4000,
    "minimumBatteryPrice": 100,
    "minimumPVPrice": 100,
    "normalBatteryCostReductionRate": 0.06,
    "normalPVCostReductionRate": 0.15,
    "initialProsumerNumber": 0,
    "initialRegularConsumerNumber": 4000000,
    "PVEffectiveLife": 25,
    "pvPotential": 0.3,
    "PVSize": 5,
    "PVHourlyEnergyOutput": [],
    "ConsumptionProfile": [],
}

def AddProfilestoInputData():
    hourlyData = pd.read_csv("./Data/LosAngles.csv", index_col=0)
    inputdata["PVHourlyEnergyOutput"] = hourlyData["Solar Output"].to_numpy()
    inputdata["ConsumptionProfile"] = hourlyData["Demand"].to_numpy()


def main():
    # RunBaseCae()
    RunSensitivityAnalysis()

def RunBaseCae():
    AddProfilestoInputData()
    temp = {}
    index = time
    Env = Environment(inputData=inputdata)
    for t in time:
        if t == 0:
            continue
        print(t)
        Env.Iterate(t)
    Env.GetResults(list(index)).to_csv('./Outputs/baseCaseResults.csv')

def RunSensitivityAnalysis():
    period = range(12, 40, 6)
    ratio= np.linspace(0.6,1,5,endpoint=False)
    temp = {}
    index = time
    # for p in period:
    for p in ratio:
        AddProfilestoInputData()
        # print(f"###rate correction frequency:{p}###")
        print(f"###fixed to variable price ratio:{p}###")
        # inputdata["rateCorrectionFreq"] = p
        inputdata["fixed2VariableRatio"] = p
        Env = Environment(inputData=inputdata)
        for t in time:
            if t != 0:
                print(t)
                Env.Iterate(t)
        temp[str(p)] = Env.GetResults(list(index))

    vars = temp[str(period[0])].columns
    # result = {}
    with pd.ExcelWriter("./Outputs/sensitivity_period.xlsx") as writer:
        for v in vars:
            df = pd.DataFrame(index=index)
            for p in temp.keys():
                df[p] = temp[p][v]
            df.to_excel(writer, sheet_name=v) 


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
