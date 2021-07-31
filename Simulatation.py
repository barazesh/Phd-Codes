import pysd
from pathlib import Path
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt


def Main():
    model = ReadModel()
    # SimulateBaseCase(model)
    # SimulatePeriod(model)
    # SimulatePopulation(model)


def ReadModel():
    vensimDirectory = './Simulation Files/Prosumers & defectors'
    vensimFile = 'net metering-no fixed tariff.mdl'
    filepath = Path(vensimDirectory, vensimFile)
    return pysd.read_vensim(str(filepath))


def SimulateBaseCase(model):
    outputVariableList = ['Regular Consumers', 'Prosumers', 'Defectors', 'Total Consumers', 'PV Cost', 'NPV PV', 'Battery Cost', 'Direct Defection NPV',
                          'Prosumer Average Demand', 'Regular Consumer Average Demand', 'Budget Deficit', 'Electricity Tariff', 'Monthly Income Shortfall', 'change in electricity tariff', 'Utility Energy Sale', 'Total Costs']
    model.doc()
    paramaters = {
        'population growth rate': 1.4**(1/240)-1,
        'time to adjust Prosumer Demand': 1,
        'time to adjust Regular Consumer demand': 1,
        'TIME STEP': 2**-10,
        'SAVEPER': 2**-4,
        'Tariff Correction Period': 12,
        'price elasticity of prosumers': -0.2,
        'price elasticity of regular consumers': -0.1,
        'Initial Electricity Tariff': 0.15,
        'PV Potential': 0.3,

    }
    variables = model.doc()
    units = variables.loc[variables["Real Name"].isin(outputVariableList) ,['Real Name','Unit']]
    units.loc[:,'Unit']=units.loc[:,'Unit'].apply(lambda x: str(x)[2:-1])
    units.to_csv('./Outputs/units.csv',index=False)

    result = model.run(params=paramaters, return_columns=outputVariableList)
    result.to_csv('./Outputs/base.csv')

    mpl.rc('lines',linewidth=3)  
    for v in result.columns:
        plt.plot(result[v])
        plt.grid(True,linestyle='--')
        plt.title(v)
        plt.xlabel('Time (Month)')
        plt.ylabel(units.loc[units['Real Name']==v,'Unit'].values[0])
        plt.savefig(f'./Outputs/{v}.pdf',facecolor='w',bbox_inches='tight')
        plt.clf()


def SimulatePeriod(model):
    outputVariableList = ['Regular Consumers', 'Prosumers', 'Defectors', 'Total Consumers', 'PV Cost', 'NPV PV', 'Battery Cost', 'Direct Defection NPV',
                          'Prosumer Average Demand', 'Regular Consumer Average Demand', 'Budget Deficit', 'Electricity Tariff', 'Monthly Income Shortfall', 'change in electricity tariff', 'Utility Energy Sale', 'Total Costs']

    paramaters = {
        'population growth rate': 1.4**(1/240)-1,
        'time to adjust Prosumer Demand': 1,
        'time to adjust Regular Consumer demand': 1,
        'TIME STEP': 2**-10,
        'SAVEPER': 2**-4,
        # 'Tariff Correction Period': 12
        # 'price elasticity of prosumers':0,
        # 'price elasticity of regular consumers':0
    }
    sensitivity_range = [1, 3]+list(range(6, 40, 6))

    for s in sensitivity_range:
        print(s)
        result = model.run(params={
            **paramaters, 'Tariff Correction Period': s}, return_columns=outputVariableList)
        result.to_csv(f'./Outputs/period_{s}.csv')


def SimulatePopulation(model):
    outputVariableList = ['Regular Consumers', 'Prosumers', 'Defectors', 'Total Consumers', 'PV Cost', 'NPV PV', 'Battery Cost', 'Direct Defection NPV',
                          'Prosumer Average Demand', 'Regular Consumer Average Demand', 'Budget Deficit', 'Electricity Tariff', 'Monthly Income Shortfall', 'change in electricity tariff', 'Utility Energy Sale', 'Total Costs']
    sensitivity_range = [(1+s)**(1/240)-1 for s in np.arange(0, 2, 0.1)]
    paramaters = {
        # 'population growth rate':1.4**(1/240)-1,
        'time to adjust Prosumer Demand': 1,
        'time to adjust Regular Consumer demand': 1,
        'TIME STEP': 2**-10,
        'SAVEPER': 2**-4,
        'Tariff Correction Period': 12
        # 'price elasticity of prosumers':0,
        # 'price elasticity of regular consumers':0
    }

    for s in sensitivity_range:
        print(s)
        result = model.run(params={
            **paramaters, 'population growth rate': s}, return_columns=outputVariableList)
        result.to_csv(f'./Outputs/populationGrowth_{s}.csv')


if __name__ == "__main__":
    Main()
