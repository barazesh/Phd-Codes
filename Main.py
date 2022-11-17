import numpy as np
from PV import PV
from Environment import Environment
duration = 240
timeStep = 1
time = np.arange(0, duration+timeStep, timeStep)

inputdata = {
    "initialTariff": 0.15,
    'initialPVPrice': 18000,
    'normalPVCostReductionRate': 0.01,
    "initialProsumerNumber": 0,
    "initialProsumerMonthlyDemand": 275,
    "prosumerPriceElasticity": -0.2,
    "prosumerDemandChangeLimit": 0.2,
    "initialRegularConsumerNumber": 4000000,
    "initialRegularConsumerMonthlyDemand": 500,
    "regularConsumerPriceElasticity": -0.1,
    "regularConsumerDemandChangeLimit": 0.2,
    "minimumPVPrice": 100,
    "initialBatteryPrice": 600,
    "normalBatteryCostReductionRate": 0.006,
    "minimumBatteryPrice": 100,
    "generationPrice": 0.06,
    "fixedCosts": 140000000,
    "permittedRoR": 0.1,
    "lossRate": 0.1,
    "rateCorrectionFreq": 36,
    "PVEffectiveLife": 240,
    "BatteryEffectiveLife": 40,
    "PVMonthlyEnergyOutput": 140,
    "DiscountRate": 0.012,
    "imitationFactor": 0.02/12,
    "innovationFactor": 0.01/12,
}


def main():
    Env = Environment(inputData=inputdata)
    for t in time:
        if t != 0:
            Env.Iterate(t)
    Env.ShowResults()


if __name__ == '__main__':
    main()
