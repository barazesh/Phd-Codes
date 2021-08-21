"""
Python model "net metering-no fixed tariff.py"
Translated using PySD version 0.10.0
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'Prosumer Demand Change Limit': 'prosumer_demand_change_limit',
    'Minimum Average Prosumer Demand': 'minimum_average_prosumer_demand',
    'Maximum Average Prosumer Demand': 'maximum_average_prosumer_demand',
    'Maximum Average Regular Consumer Demand': 'maximum_average_regular_consumer_demand',
    'Minimum Average Regular Consumer Demand': 'minimum_average_regular_consumer_demand',
    'Regular Consumer Demand Change Limit': 'regular_consumer_demand_change_limit',
    'change in indicated regular consumer demand': 'change_in_indicated_regular_consumer_demand',
    'installing PV by Innovation': 'installing_pv_by_innovation',
    'installing PV imitation factor': 'installing_pv_imitation_factor',
    'effect of PV ratio Limit': 'effect_of_pv_ratio_limit',
    'Direct Defection By Imitation': 'direct_defection_by_imitation',
    'Direct Defection by Innovation': 'direct_defection_by_innovation',
    'New Regular Consumer Ratio': 'new_regular_consumer_ratio',
    'PV Customers Ratio': 'pv_customers_ratio',
    'Defectors Ratio': 'defectors_ratio',
    'effect of Customers on Battery Cost': 'effect_of_customers_on_battery_cost',
    'PV visibility effect on immitation': 'pv_visibility_effect_on_immitation',
    'PV Potential': 'pv_potential',
    'Total Potential PV Customers': 'total_potential_pv_customers',
    'installing PV by imitation': 'installing_pv_by_imitation',
    'New Prosumers': 'new_prosumers',
    'Total Consumers': 'total_consumers',
    'Installing Battery By Imitation': 'installing_battery_by_imitation',
    'direct defection imitation factor': 'direct_defection_imitation_factor',
    'installing battery imitation factor': 'installing_battery_imitation_factor',
    'Regular Consumers': 'regular_consumers',
    'effect of Customers on PV Cost': 'effect_of_customers_on_pv_cost',
    'PV Cost': 'pv_cost',
    'Electricity Tariff': 'electricity_tariff',
    'Initial PV Cost': 'initial_pv_cost',
    'Battery Cost': 'battery_cost',
    'Initial Battery Cost': 'initial_battery_cost',
    'Initial Budget Deficit': 'initial_budget_deficit',
    'Budget Deficit': 'budget_deficit',
    'Initial Average Consumer Demand': 'initial_average_consumer_demand',
    'Initial Prosumer Demand': 'initial_prosumer_demand',
    'Regular Consumer Average Demand': 'regular_consumer_average_demand',
    'Prosumer Average Demand': 'prosumer_average_demand',
    'Initial Electricity Tariff': 'initial_electricity_tariff',
    'Initial Number of Consumers': 'initial_number_of_consumers',
    'Installing Battery by Innovation': 'installing_battery_by_innovation',
    'Electricity Loss': 'electricity_loss',
    'Deficit recovery period': 'deficit_recovery_period',
    'Indicated Tariff Change': 'indicated_tariff_change',
    'Energy Procurement': 'energy_procurement',
    'percent std effect of remaining time': 'percent_std_effect_of_remaining_time',
    'std of effect of remaining time': 'std_of_effect_of_remaining_time',
    'effect of remaining time on change in electricity tariff':
    'effect_of_remaining_time_on_change_in_electricity_tariff',
    'tariff correction remaining time': 'tariff_correction_remaining_time',
    'pi': 'pi',
    'change in electricity tariff': 'change_in_electricity_tariff',
    'change in Regular Consumer Demand': 'change_in_regular_consumer_demand',
    'change in Prosumer Demand': 'change_in_prosumer_demand',
    'change in indicated prosumer demand': 'change_in_indicated_prosumer_demand',
    'Average Daily Battery Eenergy': 'average_daily_battery_eenergy',
    'Battery Cost Reduction': 'battery_cost_reduction',
    'Battery Life': 'battery_life',
    'effect of Minimum Battery Cost': 'effect_of_minimum_battery_cost',
    'Direct Defection Total Cost': 'direct_defection_total_cost',
    'Direct Defector Monthly Savings': 'direct_defector_monthly_savings',
    'Direct Defector Net Present Savings': 'direct_defector_net_present_savings',
    'Discount Rate': 'discount_rate',
    'Consumer Growth': 'consumer_growth',
    'Defectors': 'defectors',
    'effect of direct defection NPV on imitation': 'effect_of_direct_defection_npv_on_imitation',
    'Direct Defection NPV': 'direct_defection_npv',
    '"No. Batteries"': 'no_batteries',
    '"No. Bettery Replacement"': 'no_bettery_replacement',
    'NPV PV Income': 'npv_pv_income',
    'Total PV Cost': 'total_pv_cost',
    'effect of direct defection NPV on innovation': 'effect_of_direct_defection_npv_on_innovation',
    'effect of installing battery NPV on imitation':
    'effect_of_installing_battery_npv_on_imitation',
    'effect of installing battery NPV on innovation':
    'effect_of_installing_battery_npv_on_innovation',
    'indicated change in Prosumer Demand': 'indicated_change_in_prosumer_demand',
    'indicated change in regular Consumer Demand': 'indicated_change_in_regular_consumer_demand',
    'Prosumers': 'prosumers',
    'Total Customers with PV': 'total_customers_with_pv',
    'Installing Battery NPV': 'installing_battery_npv',
    '"No. PVs"': 'no_pvs',
    'Total Battery Cost': 'total_battery_cost',
    'PV monthly Income': 'pv_monthly_income',
    'New Regular Consumers': 'new_regular_consumers',
    'Storage to Daily Load Factor': 'storage_to_daily_load_factor',
    'Income': 'income',
    'Reliablity Margin': 'reliablity_margin',
    'New Defectors': 'new_defectors',
    'Actual Regular Customer Demand change': 'actual_regular_customer_demand_change',
    'Actual Prosumer Demand Change': 'actual_prosumer_demand_change',
    'New Prosumer Ratio': 'new_prosumer_ratio',
    'NPV PV Ratio': 'npv_pv_ratio',
    'effect of PV NPV': 'effect_of_pv_npv',
    'NPV PV': 'npv_pv',
    'population growth rate': 'population_growth_rate',
    'New Defector Ratio': 'new_defector_ratio',
    'PV Life': 'pv_life',
    'PV monthly Generation': 'pv_monthly_generation',
    'PV size': 'pv_size',
    'Normal Battery Cost Reduction rate': 'normal_battery_cost_reduction_rate',
    'Minimum Battery Cost': 'minimum_battery_cost',
    'time to adjust Regular Consumer demand': 'time_to_adjust_regular_consumer_demand',
    'time to adjust Prosumer Demand': 'time_to_adjust_prosumer_demand',
    'Prosumers Demand': 'prosumers_demand',
    'Tariff Correction Period': 'tariff_correction_period',
    'price elasticity of prosumers': 'price_elasticity_of_prosumers',
    'price elasticity of regular consumers': 'price_elasticity_of_regular_consumers',
    'Desired Income': 'desired_income',
    'Permited Profit': 'permited_profit',
    'effect of Minimum PV Cost': 'effect_of_minimum_pv_cost',
    'PV Cost Reduction': 'pv_cost_reduction',
    'Immitation Factor': 'immitation_factor',
    'Fixed Costs': 'fixed_costs',
    'Generation Price': 'generation_price',
    'Total Costs': 'total_costs',
    'Variable Costs': 'variable_costs',
    'Normal PV Cost Reduction rate': 'normal_pv_cost_reduction_rate',
    'Minimum PV Cost': 'minimum_pv_cost',
    'Monthly Income Shortfall': 'monthly_income_shortfall',
    'Regular Consumers Demand': 'regular_consumers_demand',
    'Utility Energy Sale': 'utility_energy_sale',
    'Innovation factor': 'innovation_factor',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data['time']()


@cache('run')
def prosumer_demand_change_limit():
    """
    Real Name: b'Prosumer Demand Change Limit'
    Original Eqn: b'0.2'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.2


@cache('step')
def minimum_average_prosumer_demand():
    """
    Real Name: b'Minimum Average Prosumer Demand'
    Original Eqn: b'Initial Prosumer Demand*(1-Prosumer Demand Change Limit)'
    Units: b'kWh/(Customer*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return initial_prosumer_demand() * (1 - prosumer_demand_change_limit())


@cache('step')
def maximum_average_prosumer_demand():
    """
    Real Name: b'Maximum Average Prosumer Demand'
    Original Eqn: b'Initial Prosumer Demand*(1+Prosumer Demand Change Limit)'
    Units: b'kWh/(Customer*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return initial_prosumer_demand() * (1 + prosumer_demand_change_limit())


@cache('step')
def maximum_average_regular_consumer_demand():
    """
    Real Name: b'Maximum Average Regular Consumer Demand'
    Original Eqn: b'Initial Average Consumer Demand*(1+Regular Consumer Demand Change Limit)'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return initial_average_consumer_demand() * (1 + regular_consumer_demand_change_limit())


@cache('step')
def minimum_average_regular_consumer_demand():
    """
    Real Name: b'Minimum Average Regular Consumer Demand'
    Original Eqn: b'Initial Average Consumer Demand*(1-Regular Consumer Demand Change Limit)'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return initial_average_consumer_demand() * (1 - regular_consumer_demand_change_limit())


@cache('run')
def regular_consumer_demand_change_limit():
    """
    Real Name: b'Regular Consumer Demand Change Limit'
    Original Eqn: b'0.2'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.2


@cache('step')
def change_in_indicated_regular_consumer_demand():
    """
    Real Name: b'change in indicated regular consumer demand'
    Original Eqn: b'IF THEN ELSE( indicated change in regular Consumer Demand+Regular Consumer Average Demand\\\\ >Maximum Average Regular Consumer Demand, Maximum Average Regular Consumer Demand-Regular Consumer Average Demand , IF THEN ELSE\\\\ ( indicated change in regular Consumer Demand+Regular Consumer Average Demand<Minimum Average Regular Consumer Demand , Minimum Average Regular Consumer Demand\\\\ -Regular Consumer Average Demand , indicated change in regular Consumer Demand ) )'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b'IF THEN ELSE( indicated change in regular Consumer Demand+Regular Consumer \\n    \\t\\tAverage Demand>Maximum Average Regular Consumer Demand, Maximum Average \\n    \\t\\tRegular Consumer Demand-Regular Consumer Average Demand , IF THEN ELSE( \\n    \\t\\tindicated change in regular Consumer Demand+Regular Consumer Average \\n    \\t\\tDemand<Minimum Average Regular Consumer Demand , Minimum Average Regular \\n    \\t\\tConsumer Demand-Regular Consumer Average Demand , indicated change in \\n    \\t\\tregular Consumer Demand ) )'
    """
    return functions.if_then_else(
        indicated_change_in_regular_consumer_demand() + regular_consumer_average_demand() >
        maximum_average_regular_consumer_demand(),
        maximum_average_regular_consumer_demand() - regular_consumer_average_demand(),
        functions.if_then_else(
            indicated_change_in_regular_consumer_demand() + regular_consumer_average_demand() <
            minimum_average_regular_consumer_demand(),
            minimum_average_regular_consumer_demand() - regular_consumer_average_demand(),
            indicated_change_in_regular_consumer_demand()))


@cache('step')
def installing_pv_by_innovation():
    """
    Real Name: b'installing PV by Innovation'
    Original Eqn: b'effect of PV NPV*Innovation factor*Regular Consumers*effect of PV ratio Limit'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_pv_npv() * innovation_factor() * regular_consumers(
    ) * effect_of_pv_ratio_limit()


@cache('step')
def installing_pv_imitation_factor():
    """
    Real Name: b'installing PV imitation factor'
    Original Eqn: b'effect of PV NPV*Immitation Factor*PV Customers Ratio*PV visibility effect on immitation'
    Units: b'1/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_pv_npv() * immitation_factor() * pv_customers_ratio(
    ) * pv_visibility_effect_on_immitation()


@cache('step')
def effect_of_pv_ratio_limit():
    """
    Real Name: b'effect of PV ratio Limit'
    Original Eqn: b'1-1/(1+EXP(95-100*PV Customers Ratio))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 - 1 / (1 + np.exp(95 - 100 * pv_customers_ratio()))


@cache('step')
def direct_defection_by_imitation():
    """
    Real Name: b'Direct Defection By Imitation'
    Original Eqn: b'direct defection imitation factor*Regular Consumers*effect of PV ratio Limit'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return direct_defection_imitation_factor() * regular_consumers() * effect_of_pv_ratio_limit()


@cache('step')
def direct_defection_by_innovation():
    """
    Real Name: b'Direct Defection by Innovation'
    Original Eqn: b'Innovation factor*Regular Consumers*effect of direct defection NPV on innovation*effect of PV ratio Limit'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return innovation_factor() * regular_consumers(
    ) * effect_of_direct_defection_npv_on_innovation() * effect_of_pv_ratio_limit()


@cache('step')
def new_regular_consumer_ratio():
    """
    Real Name: b'New Regular Consumer Ratio'
    Original Eqn: b'1-New Defector Ratio-New Prosumer Ratio'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 - new_defector_ratio() - new_prosumer_ratio()


@cache('step')
def pv_customers_ratio():
    """
    Real Name: b'PV Customers Ratio'
    Original Eqn: b'Total Customers with PV/Total Potential PV Customers'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return total_customers_with_pv() / total_potential_pv_customers()


@cache('step')
def defectors_ratio():
    """
    Real Name: b'Defectors Ratio'
    Original Eqn: b'Defectors/Total Potential PV Customers'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return defectors() / total_potential_pv_customers()


@cache('step')
def effect_of_customers_on_battery_cost():
    """
    Real Name: b'effect of Customers on Battery Cost'
    Original Eqn: b'1+1/(1+EXP(5-Defectors Ratio*15))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 + 1 / (1 + np.exp(5 - defectors_ratio() * 15))


@cache('run')
def pv_visibility_effect_on_immitation():
    """
    Real Name: b'PV visibility effect on immitation'
    Original Eqn: b'3'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 3


@cache('run')
def pv_potential():
    """
    Real Name: b'PV Potential'
    Original Eqn: b'0.3'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.3


@cache('step')
def total_potential_pv_customers():
    """
    Real Name: b'Total Potential PV Customers'
    Original Eqn: b'PV Potential*Total Consumers'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return pv_potential() * total_consumers()


@cache('step')
def installing_pv_by_imitation():
    """
    Real Name: b'installing PV by imitation'
    Original Eqn: b'installing PV imitation factor*Regular Consumers*effect of PV ratio Limit'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return installing_pv_imitation_factor() * regular_consumers() * effect_of_pv_ratio_limit()


@cache('step')
def new_prosumers():
    """
    Real Name: b'New Prosumers'
    Original Eqn: b'Consumer Growth*New Prosumer Ratio*effect of PV ratio Limit'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return consumer_growth() * new_prosumer_ratio() * effect_of_pv_ratio_limit()


@cache('step')
def total_consumers():
    """
    Real Name: b'Total Consumers'
    Original Eqn: b'INTEG ( Consumer Growth, Initial Number of Consumers)'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_total_consumers()


@cache('step')
def installing_battery_by_imitation():
    """
    Real Name: b'Installing Battery By Imitation'
    Original Eqn: b'IF THEN ELSE(Prosumers>0,Prosumers*installing battery imitation factor,0)'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(prosumers() > 0,
                                  prosumers() * installing_battery_imitation_factor(), 0)


@cache('step')
def direct_defection_imitation_factor():
    """
    Real Name: b'direct defection imitation factor'
    Original Eqn: b'Immitation Factor*effect of direct defection NPV on imitation*Defectors Ratio'
    Units: b'1/(Customer*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return immitation_factor() * effect_of_direct_defection_npv_on_imitation() * defectors_ratio()


@cache('step')
def installing_battery_imitation_factor():
    """
    Real Name: b'installing battery imitation factor'
    Original Eqn: b'Defectors Ratio*effect of installing battery NPV on imitation*Immitation Factor'
    Units: b'1/(Customer*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return defectors_ratio() * effect_of_installing_battery_npv_on_imitation() * immitation_factor(
    )


@cache('step')
def regular_consumers():
    """
    Real Name: b'Regular Consumers'
    Original Eqn: b'INTEG ( New Regular Consumers-Direct Defection By Imitation-Direct Defection by Innovation-installing PV by imitation\\\\ -installing PV by Innovation, Initial Number of Consumers)'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_regular_consumers()


@cache('step')
def effect_of_customers_on_pv_cost():
    """
    Real Name: b'effect of Customers on PV Cost'
    Original Eqn: b'1+1/(1+EXP(5-PV Customers Ratio*15))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 + 1 / (1 + np.exp(5 - pv_customers_ratio() * 15))


@cache('step')
def pv_cost():
    """
    Real Name: b'PV Cost'
    Original Eqn: b'INTEG ( -PV Cost Reduction, Initial PV Cost)'
    Units: b'Dollar/kw'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_pv_cost()


@cache('step')
def electricity_tariff():
    """
    Real Name: b'Electricity Tariff'
    Original Eqn: b'INTEG ( change in electricity tariff, Initial Electricity Tariff)'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_electricity_tariff()


@cache('run')
def initial_pv_cost():
    """
    Real Name: b'Initial PV Cost'
    Original Eqn: b'4000'
    Units: b'Dollar/kw'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 4000


@cache('step')
def battery_cost():
    """
    Real Name: b'Battery Cost'
    Original Eqn: b'INTEG ( -Battery Cost Reduction, Initial Battery Cost)'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_battery_cost()


@cache('run')
def initial_battery_cost():
    """
    Real Name: b'Initial Battery Cost'
    Original Eqn: b'600'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 600


@cache('run')
def initial_budget_deficit():
    """
    Real Name: b'Initial Budget Deficit'
    Original Eqn: b'0'
    Units: b'Dollar'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0


@cache('step')
def budget_deficit():
    """
    Real Name: b'Budget Deficit'
    Original Eqn: b'INTEG ( Monthly Income Shortfall, Initial Budget Deficit)'
    Units: b'Dollar'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_budget_deficit()


@cache('run')
def initial_average_consumer_demand():
    """
    Real Name: b'Initial Average Consumer Demand'
    Original Eqn: b'500'
    Units: b'kWh/(Customer*Month)'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 500


@cache('run')
def initial_prosumer_demand():
    """
    Real Name: b'Initial Prosumer Demand'
    Original Eqn: b'200'
    Units: b'kWh/(Customer*Month)'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 200


@cache('step')
def regular_consumer_average_demand():
    """
    Real Name: b'Regular Consumer Average Demand'
    Original Eqn: b'INTEG ( change in Regular Consumer Demand, Initial Average Consumer Demand)'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_regular_consumer_average_demand()


@cache('step')
def prosumer_average_demand():
    """
    Real Name: b'Prosumer Average Demand'
    Original Eqn: b'INTEG ( change in Prosumer Demand, Initial Prosumer Demand)'
    Units: b'kWh/Month/Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_prosumer_average_demand()


@cache('run')
def initial_electricity_tariff():
    """
    Real Name: b'Initial Electricity Tariff'
    Original Eqn: b'0.15'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.15


@cache('run')
def initial_number_of_consumers():
    """
    Real Name: b'Initial Number of Consumers'
    Original Eqn: b'4e+06'
    Units: b'Customer'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 4e+06


@cache('step')
def installing_battery_by_innovation():
    """
    Real Name: b'Installing Battery by Innovation'
    Original Eqn: b'Innovation factor*Prosumers*effect of installing battery NPV on innovation'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return innovation_factor() * prosumers() * effect_of_installing_battery_npv_on_innovation()


@cache('run')
def electricity_loss():
    """
    Real Name: b'Electricity Loss'
    Original Eqn: b'10'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 10


@cache('run')
def deficit_recovery_period():
    """
    Real Name: b'Deficit recovery period'
    Original Eqn: b'6'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 6


@cache('step')
def indicated_tariff_change():
    """
    Real Name: b'Indicated Tariff Change'
    Original Eqn: b'Budget Deficit/Utility Energy Sale/Deficit recovery period'
    Units: b'Dollar/(Month*kWh)'
    Limits: (None, None)
    Type: component

    b''
    """
    return budget_deficit() / utility_energy_sale() / deficit_recovery_period()


@cache('step')
def energy_procurement():
    """
    Real Name: b'Energy Procurement'
    Original Eqn: b'Utility Energy Sale*(1+Electricity Loss/100)'
    Units: b'kWh/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return utility_energy_sale() * (1 + electricity_loss() / 100)


@cache('run')
def percent_std_effect_of_remaining_time():
    """
    Real Name: b'percent std effect of remaining time'
    Original Eqn: b'0.05'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.05


@cache('step')
def std_of_effect_of_remaining_time():
    """
    Real Name: b'std of effect of remaining time'
    Original Eqn: b'percent std effect of remaining time*Tariff Correction Period'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return percent_std_effect_of_remaining_time() * tariff_correction_period()


@cache('step')
def effect_of_remaining_time_on_change_in_electricity_tariff():
    """
    Real Name: b'effect of remaining time on change in electricity tariff'
    Original Eqn: b'1/(std of effect of remaining time*2*pi)*EXP( -0.5*(tariff correction remaining time\\\\ /std of effect of remaining time)^2 )'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b'1/(std of effect of remaining time*2*pi)*EXP( -0.5*(tariff correction \\n    \\t\\tremaining time/std of effect of remaining time)^2 )'
    """
    return 1 / (std_of_effect_of_remaining_time() * 2 * pi()) * np.exp(
        -0.5 * (tariff_correction_remaining_time() / std_of_effect_of_remaining_time())**2)


@cache('step')
def tariff_correction_remaining_time():
    """
    Real Name: b'tariff correction remaining time'
    Original Eqn: b'MIN( MODULO( Time , Tariff Correction Period ), ABS(MODULO(Time, Tariff Correction Period\\\\ )-Tariff Correction Period) )'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return np.minimum(np.mod(time(), tariff_correction_period()),
                      abs(np.mod(time(), tariff_correction_period()) - tariff_correction_period()))


@cache('run')
def pi():
    """
    Real Name: b'pi'
    Original Eqn: b'3.14159'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 3.14159


@cache('step')
def change_in_electricity_tariff():
    """
    Real Name: b'change in electricity tariff'
    Original Eqn: b'Indicated Tariff Change*effect of remaining time on change in electricity tariff'
    Units: b'Dollar/(kWh*Month)'
    Limits: (None, None)
    Type: component

    b'IF THEN ELSE( MODULO(Time, Tariff Correction Period )=0 , Limited Tariff \\n    \\t\\tChange , 0 )'
    """
    return indicated_tariff_change() * effect_of_remaining_time_on_change_in_electricity_tariff()


@cache('step')
def change_in_regular_consumer_demand():
    """
    Real Name: b'change in Regular Consumer Demand'
    Original Eqn: b'Actual Regular Customer Demand change/time to adjust Regular Consumer demand'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return actual_regular_customer_demand_change() / time_to_adjust_regular_consumer_demand()


@cache('step')
def change_in_prosumer_demand():
    """
    Real Name: b'change in Prosumer Demand'
    Original Eqn: b'Actual Prosumer Demand Change/time to adjust Prosumer Demand'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return actual_prosumer_demand_change() / time_to_adjust_prosumer_demand()


@cache('step')
def change_in_indicated_prosumer_demand():
    """
    Real Name: b'change in indicated prosumer demand'
    Original Eqn: b'IF THEN ELSE(Prosumer Average Demand+indicated change in Prosumer Demand>Maximum Average Prosumer Demand\\\\ , Maximum Average Prosumer Demand-Prosumer Average Demand , IF THEN ELSE( Prosumer Average Demand\\\\ +indicated change in Prosumer Demand<Minimum Average Prosumer Demand , Minimum Average Prosumer Demand\\\\ -Prosumer Average Demand , indicated change in Prosumer Demand ) )'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        prosumer_average_demand() + indicated_change_in_prosumer_demand() >
        maximum_average_prosumer_demand(),
        maximum_average_prosumer_demand() - prosumer_average_demand(),
        functions.if_then_else(
            prosumer_average_demand() + indicated_change_in_prosumer_demand() <
            minimum_average_prosumer_demand(),
            minimum_average_prosumer_demand() - prosumer_average_demand(),
            indicated_change_in_prosumer_demand()))


@cache('step')
def average_daily_battery_eenergy():
    """
    Real Name: b'Average Daily Battery Eenergy'
    Original Eqn: b'(Regular Consumer Average Demand/30)*Storage to Daily Load Factor'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return (regular_consumer_average_demand() / 30) * storage_to_daily_load_factor()


@cache('step')
def battery_cost_reduction():
    """
    Real Name: b'Battery Cost Reduction'
    Original Eqn: b'effect of Customers on Battery Cost*effect of Minimum Battery Cost*Normal Battery Cost Reduction rate\\\\ *Battery Cost'
    Units: b'Dollar/(kWh*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_customers_on_battery_cost() * effect_of_minimum_battery_cost(
    ) * normal_battery_cost_reduction_rate() * battery_cost()


@cache('run')
def battery_life():
    """
    Real Name: b'Battery Life'
    Original Eqn: b'40'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 40


@cache('step')
def effect_of_minimum_battery_cost():
    """
    Real Name: b'effect of Minimum Battery Cost'
    Original Eqn: b'1-1/(1+EXP(6-12*Minimum Battery Cost/Battery Cost))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 - 1 / (1 + np.exp(6 - 12 * minimum_battery_cost() / battery_cost()))


@cache('step')
def direct_defection_total_cost():
    """
    Real Name: b'Direct Defection Total Cost'
    Original Eqn: b'Total Battery Cost+Total PV Cost'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return total_battery_cost() + total_pv_cost()


@cache('step')
def direct_defector_monthly_savings():
    """
    Real Name: b'Direct Defector Monthly Savings'
    Original Eqn: b'Electricity Tariff*Regular Consumer Average Demand'
    Units: b'Dollar/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return electricity_tariff() * regular_consumer_average_demand()


@cache('step')
def direct_defector_net_present_savings():
    """
    Real Name: b'Direct Defector Net Present Savings'
    Original Eqn: b'Direct Defector Monthly Savings*(((1+Discount Rate)^(PV Life+1)-1)/Discount Rate)'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: component

    b''
    """
    return direct_defector_monthly_savings() * ((
        (1 + discount_rate())**(pv_life() + 1) - 1) / discount_rate())


@cache('run')
def discount_rate():
    """
    Real Name: b'Discount Rate'
    Original Eqn: b'0.001'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.001


@cache('step')
def consumer_growth():
    """
    Real Name: b'Consumer Growth'
    Original Eqn: b'population growth rate*Total Consumers'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return population_growth_rate() * total_consumers()


@cache('step')
def defectors():
    """
    Real Name: b'Defectors'
    Original Eqn: b'INTEG ( Direct Defection By Imitation+Direct Defection by Innovation+Installing Battery By Imitation\\\\ +Installing Battery by Innovation+New Defectors, 0)'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_defectors()


@cache('step')
def effect_of_direct_defection_npv_on_imitation():
    """
    Real Name: b'effect of direct defection NPV on imitation'
    Original Eqn: b'0.5+2/(1+EXP(2-Direct Defection NPV/5000))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b'0.5+2/(1+exp(2-x/5000))'
    """
    return 0.5 + 2 / (1 + np.exp(2 - direct_defection_npv() / 5000))


@cache('step')
def direct_defection_npv():
    """
    Real Name: b'Direct Defection NPV'
    Original Eqn: b'Direct Defector Net Present Savings-Direct Defection Total Cost'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return direct_defector_net_present_savings() - direct_defection_total_cost()


@cache('step')
def no_batteries():
    """
    Real Name: b'"No. Batteries"'
    Original Eqn: b'INTEGER(Average Daily Battery Eenergy)+1'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return int(average_daily_battery_eenergy()) + 1


@cache('step')
def no_bettery_replacement():
    """
    Real Name: b'"No. Bettery Replacement"'
    Original Eqn: b'IF THEN ELSE(MODULO(PV Life, Battery Life )=0, PV Life/Battery Life , INTEGER( PV Life\\\\ /Battery Life )+1 )'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        np.mod(pv_life(), battery_life()) == 0,
        pv_life() / battery_life(),
        int(pv_life() / battery_life()) + 1)


@cache('step')
def npv_pv_income():
    """
    Real Name: b'NPV PV Income'
    Original Eqn: b'PV monthly Income*(((1+Discount Rate)^(PV Life+1)-1)/Discount Rate)'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return pv_monthly_income() * (((1 + discount_rate())**(pv_life() + 1) - 1) / discount_rate())


@cache('step')
def total_pv_cost():
    """
    Real Name: b'Total PV Cost'
    Original Eqn: b'"No. PVs"*PV Cost'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return no_pvs() * pv_cost()


@cache('step')
def effect_of_direct_defection_npv_on_innovation():
    """
    Real Name: b'effect of direct defection NPV on innovation'
    Original Eqn: b'1+1.5/(1+EXP(2-Direct Defection NPV/2000))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 + 1.5 / (1 + np.exp(2 - direct_defection_npv() / 2000))


@cache('step')
def effect_of_installing_battery_npv_on_imitation():
    """
    Real Name: b'effect of installing battery NPV on imitation'
    Original Eqn: b'0.5+2/(1+EXP(2-Installing Battery NPV/5000))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 0.5 + 2 / (1 + np.exp(2 - installing_battery_npv() / 5000))


@cache('step')
def effect_of_installing_battery_npv_on_innovation():
    """
    Real Name: b'effect of installing battery NPV on innovation'
    Original Eqn: b'1+1.5/(1+EXP(2-Installing Battery NPV/2000))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 + 1.5 / (1 + np.exp(2 - installing_battery_npv() / 2000))


@cache('step')
def indicated_change_in_prosumer_demand():
    """
    Real Name: b'indicated change in Prosumer Demand'
    Original Eqn: b'IF THEN ELSE(Electricity Tariff=0, -price elasticity of prosumers*Prosumer Average Demand\\\\ *30 ,change in electricity tariff*price elasticity of prosumers*Prosumer Average Demand\\\\ /Electricity Tariff)'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        electricity_tariff() == 0,
        -price_elasticity_of_prosumers() * prosumer_average_demand() * 30,
        change_in_electricity_tariff() * price_elasticity_of_prosumers() *
        prosumer_average_demand() / electricity_tariff())


@cache('step')
def indicated_change_in_regular_consumer_demand():
    """
    Real Name: b'indicated change in regular Consumer Demand'
    Original Eqn: b'IF THEN ELSE(Electricity Tariff=0, -price elasticity of regular consumers*Regular Consumer Average Demand\\\\ *30, change in electricity tariff*Regular Consumer Average Demand*price elasticity of regular consumers\\\\ /Electricity Tariff)'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        electricity_tariff() == 0,
        -price_elasticity_of_regular_consumers() * regular_consumer_average_demand() * 30,
        change_in_electricity_tariff() * regular_consumer_average_demand() *
        price_elasticity_of_regular_consumers() / electricity_tariff())


@cache('step')
def prosumers():
    """
    Real Name: b'Prosumers'
    Original Eqn: b'INTEG ( installing PV by imitation+installing PV by Innovation+New Prosumers-Installing Battery By Imitation\\\\ -Installing Battery by Innovation, 0)'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_prosumers()


@cache('step')
def total_customers_with_pv():
    """
    Real Name: b'Total Customers with PV'
    Original Eqn: b'Defectors+Prosumers'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return defectors() + prosumers()


@cache('step')
def installing_battery_npv():
    """
    Real Name: b'Installing Battery NPV'
    Original Eqn: b'Direct Defection NPV-NPV PV'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return direct_defection_npv() - npv_pv()


@cache('step')
def no_pvs():
    """
    Real Name: b'"No. PVs"'
    Original Eqn: b'INTEGER(Regular Consumer Average Demand*(1+Reliablity Margin)/PV monthly Generation)\\\\ +1'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return int(regular_consumer_average_demand() *
               (1 + reliablity_margin()) / pv_monthly_generation()) + 1


@cache('step')
def total_battery_cost():
    """
    Real Name: b'Total Battery Cost'
    Original Eqn: b'Battery Cost*"No. Bettery Replacement"*"No. Batteries"'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return battery_cost() * no_bettery_replacement() * no_batteries()


@cache('step')
def pv_monthly_income():
    """
    Real Name: b'PV monthly Income'
    Original Eqn: b'Electricity Tariff*PV monthly Generation'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return electricity_tariff() * pv_monthly_generation()


@cache('step')
def new_regular_consumers():
    """
    Real Name: b'New Regular Consumers'
    Original Eqn: b'Consumer Growth*New Regular Consumer Ratio'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return consumer_growth() * new_regular_consumer_ratio()


@cache('run')
def storage_to_daily_load_factor():
    """
    Real Name: b'Storage to Daily Load Factor'
    Original Eqn: b'0.5'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.5


@cache('step')
def income():
    """
    Real Name: b'Income'
    Original Eqn: b'Electricity Tariff*Utility Energy Sale'
    Units: b'Dollar/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return electricity_tariff() * utility_energy_sale()


@cache('run')
def reliablity_margin():
    """
    Real Name: b'Reliablity Margin'
    Original Eqn: b'0.5'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.5


@cache('step')
def new_defectors():
    """
    Real Name: b'New Defectors'
    Original Eqn: b'Consumer Growth*New Defector Ratio*(effect of direct defection NPV on imitation+effect of direct defection NPV on innovation\\\\ )/2'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return consumer_growth() * new_defector_ratio() * (
        effect_of_direct_defection_npv_on_imitation() +
        effect_of_direct_defection_npv_on_innovation()) / 2


@cache('step')
def actual_regular_customer_demand_change():
    """
    Real Name: b'Actual Regular Customer Demand change'
    Original Eqn: b'INTEG ( change in indicated regular consumer demand-change in Regular Consumer Demand, 0)'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_actual_regular_customer_demand_change()


@cache('step')
def actual_prosumer_demand_change():
    """
    Real Name: b'Actual Prosumer Demand Change'
    Original Eqn: b'INTEG ( change in indicated prosumer demand-change in Prosumer Demand, 0)'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_actual_prosumer_demand_change()


@cache('step')
def new_prosumer_ratio():
    """
    Real Name: b'New Prosumer Ratio'
    Original Eqn: b'0.08*effect of PV NPV'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 0.08 * effect_of_pv_npv()


@cache('step')
def npv_pv_ratio():
    """
    Real Name: b'NPV PV Ratio'
    Original Eqn: b'NPV PV/PV Cost'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return npv_pv() / pv_cost()


@cache('step')
def effect_of_pv_npv():
    """
    Real Name: b'effect of PV NPV'
    Original Eqn: b'1+2/(1+EXP( -4*(NPV PV Ratio-2) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 + 2 / (1 + np.exp(-4 * (npv_pv_ratio() - 2)))


@cache('step')
def npv_pv():
    """
    Real Name: b'NPV PV'
    Original Eqn: b'(NPV PV Income-PV Cost)*PV size'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return (npv_pv_income() - pv_cost()) * pv_size()


@cache('run')
def population_growth_rate():
    """
    Real Name: b'population growth rate'
    Original Eqn: b'0.01/12'
    Units: b'1/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.01 / 12


@cache('run')
def new_defector_ratio():
    """
    Real Name: b'New Defector Ratio'
    Original Eqn: b'0.1'
    Units: b'Dollar'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.1


@cache('run')
def pv_life():
    """
    Real Name: b'PV Life'
    Original Eqn: b'240'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 240


@cache('run')
def pv_monthly_generation():
    """
    Real Name: b'PV monthly Generation'
    Original Eqn: b'140'
    Units: b'kWh/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 140


@cache('run')
def pv_size():
    """
    Real Name: b'PV size'
    Original Eqn: b'5'
    Units: b'kw'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 5


@cache('run')
def normal_battery_cost_reduction_rate():
    """
    Real Name: b'Normal Battery Cost Reduction rate'
    Original Eqn: b'0.006'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.006


@cache('run')
def minimum_battery_cost():
    """
    Real Name: b'Minimum Battery Cost'
    Original Eqn: b'100'
    Units: b'Dollar/kw'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 100


@cache('run')
def time_to_adjust_regular_consumer_demand():
    """
    Real Name: b'time to adjust Regular Consumer demand'
    Original Eqn: b'3'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 3


@cache('run')
def time_to_adjust_prosumer_demand():
    """
    Real Name: b'time to adjust Prosumer Demand'
    Original Eqn: b'3'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 3


@cache('step')
def prosumers_demand():
    """
    Real Name: b'Prosumers Demand'
    Original Eqn: b'Prosumer Average Demand*Prosumers'
    Units: b'kWh/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return prosumer_average_demand() * prosumers()


@cache('run')
def tariff_correction_period():
    """
    Real Name: b'Tariff Correction Period'
    Original Eqn: b'12'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 12


@cache('run')
def price_elasticity_of_prosumers():
    """
    Real Name: b'price elasticity of prosumers'
    Original Eqn: b'-0.2'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return -0.2


@cache('run')
def price_elasticity_of_regular_consumers():
    """
    Real Name: b'price elasticity of regular consumers'
    Original Eqn: b'-0.1'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return -0.1


@cache('step')
def desired_income():
    """
    Real Name: b'Desired Income'
    Original Eqn: b'Total Costs*(1+Permited Profit)'
    Units: b'Dollar/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return total_costs() * (1 + permited_profit())


@cache('run')
def permited_profit():
    """
    Real Name: b'Permited Profit'
    Original Eqn: b'0.15'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.15


@cache('step')
def effect_of_minimum_pv_cost():
    """
    Real Name: b'effect of Minimum PV Cost'
    Original Eqn: b'1-1/(1+EXP(6-12*Minimum PV Cost/PV Cost))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return 1 - 1 / (1 + np.exp(6 - 12 * minimum_pv_cost() / pv_cost()))


@cache('step')
def pv_cost_reduction():
    """
    Real Name: b'PV Cost Reduction'
    Original Eqn: b'effect of Customers on PV Cost*effect of Minimum PV Cost*Normal PV Cost Reduction rate\\\\ *PV Cost'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_customers_on_pv_cost() * effect_of_minimum_pv_cost(
    ) * normal_pv_cost_reduction_rate() * pv_cost()


@cache('run')
def immitation_factor():
    """
    Real Name: b'Immitation Factor'
    Original Eqn: b'0.02/12'
    Units: b'1/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.02 / 12


@cache('run')
def fixed_costs():
    """
    Real Name: b'Fixed Costs'
    Original Eqn: b'1.4e+08'
    Units: b'Dollar/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 1.4e+08


@cache('run')
def generation_price():
    """
    Real Name: b'Generation Price'
    Original Eqn: b'0.06'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.06


@cache('step')
def total_costs():
    """
    Real Name: b'Total Costs'
    Original Eqn: b'Fixed Costs+Variable Costs'
    Units: b'Dollar/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return fixed_costs() + variable_costs()


@cache('step')
def variable_costs():
    """
    Real Name: b'Variable Costs'
    Original Eqn: b'Energy Procurement*Generation Price'
    Units: b'Dollar/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return energy_procurement() * generation_price()


@cache('run')
def normal_pv_cost_reduction_rate():
    """
    Real Name: b'Normal PV Cost Reduction rate'
    Original Eqn: b'0.01'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.01


@cache('run')
def minimum_pv_cost():
    """
    Real Name: b'Minimum PV Cost'
    Original Eqn: b'100'
    Units: b'Dollar/kw'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 100


@cache('step')
def monthly_income_shortfall():
    """
    Real Name: b'Monthly Income Shortfall'
    Original Eqn: b'Desired Income-Income'
    Units: b'Dollar/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return desired_income() - income()


@cache('step')
def regular_consumers_demand():
    """
    Real Name: b'Regular Consumers Demand'
    Original Eqn: b'Regular Consumer Average Demand*Regular Consumers'
    Units: b'kWh/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return regular_consumer_average_demand() * regular_consumers()


@cache('step')
def utility_energy_sale():
    """
    Real Name: b'Utility Energy Sale'
    Original Eqn: b'Prosumers Demand+Regular Consumers Demand'
    Units: b'kWh/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return prosumers_demand() + regular_consumers_demand()


@cache('run')
def innovation_factor():
    """
    Real Name: b'Innovation factor'
    Original Eqn: b'0.01/12'
    Units: b'1/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.01 / 12


@cache('run')
def final_time():
    """
    Real Name: b'FINAL TIME'
    Original Eqn: b'600'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b'The final time for the simulation.'
    """
    return 600


@cache('run')
def initial_time():
    """
    Real Name: b'INITIAL TIME'
    Original Eqn: b'0'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b'The initial time for the simulation.'
    """
    return 0


@cache('step')
def saveper():
    """
    Real Name: b'SAVEPER'
    Original Eqn: b'TIME STEP'
    Units: b'Month'
    Limits: (0.0, None)
    Type: component

    b'The frequency with which output is stored.'
    """
    return time_step()


@cache('run')
def time_step():
    """
    Real Name: b'TIME STEP'
    Original Eqn: b'0.0078125'
    Units: b'Month'
    Limits: (0.0, None)
    Type: constant

    b'The time step for the simulation.'
    """
    return 0.0078125


_integ_total_consumers = functions.Integ(lambda: consumer_growth(),
                                         lambda: initial_number_of_consumers())

_integ_regular_consumers = functions.Integ(
    lambda: new_regular_consumers() - direct_defection_by_imitation() -
    direct_defection_by_innovation() - installing_pv_by_imitation() - installing_pv_by_innovation(
    ), lambda: initial_number_of_consumers())

_integ_pv_cost = functions.Integ(lambda: -pv_cost_reduction(), lambda: initial_pv_cost())

_integ_electricity_tariff = functions.Integ(lambda: change_in_electricity_tariff(),
                                            lambda: initial_electricity_tariff())

_integ_battery_cost = functions.Integ(lambda: -battery_cost_reduction(),
                                      lambda: initial_battery_cost())

_integ_budget_deficit = functions.Integ(lambda: monthly_income_shortfall(),
                                        lambda: initial_budget_deficit())

_integ_regular_consumer_average_demand = functions.Integ(
    lambda: change_in_regular_consumer_demand(), lambda: initial_average_consumer_demand())

_integ_prosumer_average_demand = functions.Integ(lambda: change_in_prosumer_demand(),
                                                 lambda: initial_prosumer_demand())

_integ_defectors = functions.Integ(
    lambda: direct_defection_by_imitation() + direct_defection_by_innovation(
    ) + installing_battery_by_imitation() + installing_battery_by_innovation() + new_defectors(),
    lambda: 0)

_integ_prosumers = functions.Integ(
    lambda: installing_pv_by_imitation() + installing_pv_by_innovation() + new_prosumers() -
    installing_battery_by_imitation() - installing_battery_by_innovation(), lambda: 0)

_integ_actual_regular_customer_demand_change = functions.Integ(
    lambda: change_in_indicated_regular_consumer_demand() - change_in_regular_consumer_demand(),
    lambda: 0)

_integ_actual_prosumer_demand_change = functions.Integ(
    lambda: change_in_indicated_prosumer_demand() - change_in_prosumer_demand(), lambda: 0)
