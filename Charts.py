from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import numpy as np


def Main():
    DesignCharts()
    important_vars = ['Electricity Tariff', 'Budget Deficit',
                      'Utility Energy Sale', 'Total Costs']
    directoryPath = Path.cwd().joinpath('Outputs')

    units = GetUnits(directoryPath)

    sensitivity_var = 'populationGrowth'
    chart_vars = [(1+s)**(1/240)-1 for s in np.arange(0, 1.1, 0.2)]

    # sensitivity_var = 'period'
    # chart_vars = [1, 6, 12, 24, 36]

    result = GetValues(sensitivity_var, important_vars,
                       chart_vars, directoryPath)

    CreateCharts(directoryPath, result, units, sensitivity_var)


def CreateCharts(directoryPath, data, units, sensitivity_var):
    markerinterval = 12*2**4
    for v in data.keys():
        data[v].plot(markevery=markerinterval)
        plt.grid(True)
        plt.legend()
        if v == 'Budget Deficit':
            plt.title('Revenue Deficit')
        else:
            plt.title(v)

        plt.xlabel('Time (Month)')
        plt.xticks(range(0, 250, 24))
        u = '%'
        if v in units.index:
            u = units[v]
        plt.ylabel(u)
        # plt.show()
        plt.savefig(directoryPath.joinpath(
            f'{sensitivity_var}_{v}.pdf'), bbox_inches='tight')
        plt.clf()


def GetUnits(directoryPath):
    units = pd.read_csv(directoryPath.joinpath(
        'units.csv'), squeeze=True, index_col=0)
    return units


def DesignCharts():
    mpl.rc('lines', linewidth=1.5, markersize=4)
    mpl.rc('grid', linewidth=0.5, linestyle='--')
    mpl.rc('font', size=7, family='Times New Roman')
    cm = 1/2.54
    mpl.rc('figure', figsize=(9*cm, 6*cm))
    custom_cycler = (cycler(marker=[None, '*', 'd', 'o', 'x', 'v', 'D', 's']) +
                     cycler(color=[str(i) for i in np.linspace(0.1, 0.7, 8)]))
    mpl.rc('axes', prop_cycle=custom_cycler)


def GetValues(sensitivity_var, important_vars, selectedValues, directoryPath):
    select_result = {v: pd.DataFrame() for v in important_vars}
    for s in directoryPath.glob(f'{sensitivity_var}_*.csv'):
        sv = float(s.stem.split('_')[1])
        if sv in selectedValues:
            result = pd.read_csv(s, squeeze=True, index_col=0, dtype='float64')
            for v in important_vars:
                select_result[v][sv] = result[v]

    for v in important_vars:
        if sensitivity_var == 'populationGrowth':
            select_result[v].rename(
                columns=ConvertMonthly2AnnualRate, inplace=True)
        select_result[v].sort_index(axis=1, inplace=True)
    select_result['Deficit Fraction'] = 100 * \
        select_result['Budget Deficit']/select_result['Total Costs']
    return select_result


def ConvertMonthly2AnnualRate(rate):
    return round(100*((1+rate)**(12)-1), 3)


if __name__ == '__main__':
    Main()
