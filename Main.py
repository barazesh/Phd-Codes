import numpy as np
from PV import PV
from Environment import Environment
duration = 240
timeStep = 1
time = np.arange(0, duration+timeStep, timeStep)

inputdata = {
    "generationPrice": 0.06,
    "fixedCosts": 140000000,
    "permittedRoR": 0.15,
    "lossRate": 0.1,
    "initialTariff": 0.15,
    "rateCorrectionFreq": 12,

    "populationGrowthRate": 0.004,
    "innovationFactor": 0.01/12,
    "imitationFactor": 0.02/12,
    "initialRegularConsumerMonthlyDemand": 500,
    "regularConsumerPriceElasticity": -0.1,
    "regularConsumerDemandChangeLimit": 0.2,
    "initialProsumerMonthlyDemand": 275,
    "prosumerPriceElasticity": -0.2,
    "prosumerDemandChangeLimit": 0.2,
    
    "BatteryEffectiveLife": 40,
    "DiscountRate": 0.012,
    "initialBatteryPrice": 600,
    'initialPVPrice': 4000,
    "minimumBatteryPrice": 100,
    "minimumPVPrice": 100,
    "normalBatteryCostReductionRate": 0.006,
    'normalPVCostReductionRate': 0.015,
    "initialProsumerNumber": 0,
    "initialRegularConsumerNumber": 4000000,
    "PVEffectiveLife": 240,
    "pvPotential":0.5,
    "PVMonthlyEnergyOutput": 140,
}


def main():
    Env = Environment(inputData=inputdata)
    for t in time:
        if t != 0:
            Env.Iterate(t)
    Env.ShowResults()


if __name__ == '__main__':
    main()
