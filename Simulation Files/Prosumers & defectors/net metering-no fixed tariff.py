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
    'Average Daily Battery Eenergy': 'average_daily_battery_eenergy',
    'Battery Cost': 'battery_cost',
    'Battery Cost Reduction': 'battery_cost_reduction',
    'Battery Life': 'battery_life',
    'effect of Minimum Battery Cost': 'effect_of_minimum_battery_cost',
    'change in electricity tariff': 'change_in_electricity_tariff',
    'Direct Defection Total Cost': 'direct_defection_total_cost',
    'Direct Defector Monthly Savings': 'direct_defector_monthly_savings',
    'Direct Defector Net Present Savings': 'direct_defector_net_present_savings',
    'Discount Rate': 'discount_rate',
    'Consumer Growth': 'consumer_growth',
    'Defectors': 'defectors',
    'effect of direct defection NPV on imitation': 'effect_of_direct_defection_npv_on_imitation',
    'Direct Defection By Imitation': 'direct_defection_by_imitation',
    'Direct Defection by Innovation': 'direct_defection_by_innovation',
    'direct defection imitation factor': 'direct_defection_imitation_factor',
    'direct defection imitation percent': 'direct_defection_imitation_percent',
    'direct defection innovation factor': 'direct_defection_innovation_factor',
    'Direct Defection NPV': 'direct_defection_npv',
    '"No. Batteries"': 'no_batteries',
    '"No. Bettery Replacement"': 'no_bettery_replacement',
    'Installing Battery By Imitation': 'installing_battery_by_imitation',
    'Installing Battery by Innovation': 'installing_battery_by_innovation',
    'effect of Customers on Battery Cost': 'effect_of_customers_on_battery_cost',
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
    'Electricity Tariff': 'electricity_tariff',
    'PV monthly Income': 'pv_monthly_income',
    'New Regular Consumers': 'new_regular_consumers',
    'Storage to Daily Load Factor': 'storage_to_daily_load_factor',
    'Regular Consumers': 'regular_consumers',
    'Income': 'income',
    'New Prosumers': 'new_prosumers',
    'Reliablity Margin': 'reliablity_margin',
    'installing battery imitation percent': 'installing_battery_imitation_percent',
    'Total Consumers': 'total_consumers',
    'New Defectors': 'new_defectors',
    'change in Regular Consumer Demand': 'change_in_regular_consumer_demand',
    'Indicated Regular Customer Demand': 'indicated_regular_customer_demand',
    'change in indicated regular consumer demand': 'change_in_indicated_regular_consumer_demand',
    'Regular Consumer Average Demand': 'regular_consumer_average_demand',
    'Indicated Prosumer Demand': 'indicated_prosumer_demand',
    'Prosumer Average Demand': 'prosumer_average_demand',
    'change in indicated prosumer demand': 'change_in_indicated_prosumer_demand',
    'change in Prosumer Demand': 'change_in_prosumer_demand',
    'New Prosumer Ratio': 'new_prosumer_ratio',
    'installing PV imitation factor': 'installing_pv_imitation_factor',
    'NPV PV Ratio': 'npv_pv_ratio',
    'installing PV by Innovation': 'installing_pv_by_innovation',
    'effect of PV NPV': 'effect_of_pv_npv',
    'NPV PV': 'npv_pv',
    'population growth rate': 'population_growth_rate',
    'New Regular Consumer Ratio': 'new_regular_consumer_ratio',
    'New Defector Ratio': 'new_defector_ratio',
    'PV Life': 'pv_life',
    'PV monthly Generation': 'pv_monthly_generation',
    'PV size': 'pv_size',
    'installing PV imitation percent': 'installing_pv_imitation_percent',
    'effect of Customers on PV Cost': 'effect_of_customers_on_pv_cost',
    'Normal Battery Cost Reduction rate': 'normal_battery_cost_reduction_rate',
    'Minimum Battery Cost': 'minimum_battery_cost',
    'time to adjust Regular Consumer demand': 'time_to_adjust_regular_consumer_demand',
    'time to adjust Prosumer Demand': 'time_to_adjust_prosumer_demand',
    'effect of Prosumer Minimum Demand': 'effect_of_prosumer_minimum_demand',
    'effect of Maximum Regular Consumer Demand': 'effect_of_maximum_regular_consumer_demand',
    'Prosumers Demand': 'prosumers_demand',
    'effect of Minimum Regular Consumer Demand': 'effect_of_minimum_regular_consumer_demand',
    'Maximum Average Prosumer Demand': 'maximum_average_prosumer_demand',
    'Maximum Average Regular Consumer Demand': 'maximum_average_regular_consumer_demand',
    'Minimum Average Prosumer Demand': 'minimum_average_prosumer_demand',
    'Minimum Average Regular Consumer Demand': 'minimum_average_regular_consumer_demand',
    'Indicated Tariff Change': 'indicated_tariff_change',
    'Tariff Correction Period': 'tariff_correction_period',
    'effect of Prosumer Maximum Demand': 'effect_of_prosumer_maximum_demand',
    'price eleasticity of prosumers': 'price_eleasticity_of_prosumers',
    'price eleasticity of regular consumers': 'price_eleasticity_of_regular_consumers',
    'Budget Deficit': 'budget_deficit',
    'Desired Income': 'desired_income',
    'Permited Profit': 'permited_profit',
    'effect of Minimum PV Cost': 'effect_of_minimum_pv_cost',
    'Energy Procurement': 'energy_procurement',
    'PV Cost Reduction': 'pv_cost_reduction',
    'final yearly percent': 'final_yearly_percent',
    'Fixed Costs': 'fixed_costs',
    'Generation Price': 'generation_price',
    'Total Costs': 'total_costs',
    'installing battery imitation factor': 'installing_battery_imitation_factor',
    'Variable Costs': 'variable_costs',
    'PV Cost': 'pv_cost',
    'Normal PV Cost Reduction rate': 'normal_pv_cost_reduction_rate',
    'Minimum PV Cost': 'minimum_pv_cost',
    'Monthly Income Shortfall': 'monthly_income_shortfall',
    'Regular Consumers Demand': 'regular_consumers_demand',
    'Utility Energy Sale': 'utility_energy_sale',
    'installing PV by imitation': 'installing_pv_by_imitation',
    'installing battery innovation factor': 'installing_battery_innovation_factor',
    'installing PV innovation factor': 'installing_pv_innovation_factor',
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
def battery_cost():
    """
    Real Name: b'Battery Cost'
    Original Eqn: b'INTEG ( -Battery Cost Reduction, 600)'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_battery_cost()


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
    Original Eqn: b'WITH LOOKUP ( Minimum Battery Cost/Battery Cost, ([(0,0)-(1,1)],(0,1),(0.25,0.95),(0.4,0.8),(0.5,0.5),(0.6,0.2),(0.75,0.05),(1,0) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(minimum_battery_cost() / battery_cost(),
                            [0, 0.25, 0.4, 0.5, 0.6, 0.75, 1], [1, 0.95, 0.8, 0.5, 0.2, 0.05, 0])


@cache('step')
def change_in_electricity_tariff():
    """
    Real Name: b'change in electricity tariff'
    Original Eqn: b'IF THEN ELSE( MODULO(Time, Tariff Correction Period )=0 , Indicated Tariff Change , \\\\ 0 )'
    Units: b'Dollar/(kWh*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        np.mod(time(), tariff_correction_period()) == 0, indicated_tariff_change(), 0)


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
    Original Eqn: b'-Direct Defector Monthly Savings*((1-(1+Discount Rate)^(PV Life+1))/Discount Rate)'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: component

    b''
    """
    return -direct_defector_monthly_savings() * (
        (1 - (1 + discount_rate())**(pv_life() + 1)) / discount_rate())


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
    Original Eqn: b'WITH LOOKUP ( Direct Defection NPV, ([(0,0)-(40000,20)],(0,1),(5000,1.5),(20000,2),(40000,2.5) ))'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(direct_defection_npv(), [0, 5000, 20000, 40000], [1, 1.5, 2, 2.5])


@cache('step')
def direct_defection_by_imitation():
    """
    Real Name: b'Direct Defection By Imitation'
    Original Eqn: b'IF THEN ELSE(Regular Consumers>0,direct defection imitation percent*Regular Consumers\\\\ ,0)'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(regular_consumers() > 0,
                                  direct_defection_imitation_percent() * regular_consumers(), 0)


@cache('step')
def direct_defection_by_innovation():
    """
    Real Name: b'Direct Defection by Innovation'
    Original Eqn: b'IF THEN ELSE(Regular Consumers>0,direct defection innovation factor*Regular Consumers\\\\ *effect of direct defection NPV on innovation,0)'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        regular_consumers() > 0,
        direct_defection_innovation_factor() * regular_consumers() *
        effect_of_direct_defection_npv_on_innovation(), 0)


@cache('step')
def direct_defection_imitation_factor():
    """
    Real Name: b'direct defection imitation factor'
    Original Eqn: b'final yearly percent/12/1e+06'
    Units: b'1/(Customer*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return final_yearly_percent() / 12 / 1e+06


@cache('step')
def direct_defection_imitation_percent():
    """
    Real Name: b'direct defection imitation percent'
    Original Eqn: b'Defectors*direct defection imitation factor*effect of direct defection NPV on imitation'
    Units: b'1/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return defectors() * direct_defection_imitation_factor(
    ) * effect_of_direct_defection_npv_on_imitation()


@cache('run')
def direct_defection_innovation_factor():
    """
    Real Name: b'direct defection innovation factor'
    Original Eqn: b'0.001/12'
    Units: b'1/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.001 / 12


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
def installing_battery_by_imitation():
    """
    Real Name: b'Installing Battery By Imitation'
    Original Eqn: b'IF THEN ELSE(Prosumers>0,Prosumers*installing battery imitation percent,0)'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(prosumers() > 0,
                                  prosumers() * installing_battery_imitation_percent(), 0)


@cache('step')
def installing_battery_by_innovation():
    """
    Real Name: b'Installing Battery by Innovation'
    Original Eqn: b'installing battery innovation factor*Prosumers*effect of installing battery NPV on innovation'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return installing_battery_innovation_factor() * prosumers(
    ) * effect_of_installing_battery_npv_on_innovation()


@cache('step')
def effect_of_customers_on_battery_cost():
    """
    Real Name: b'effect of Customers on Battery Cost'
    Original Eqn: b'WITH LOOKUP ( Defectors, ([(0,1)-(1e+06,2)],(100000,1),(278287,1.07895),(400612,1.16667),(486239,1.39035),(596330\\\\ ,1.66667),(776758,1.77632),(1e+06 ,1.8) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(defectors(), [100000, 278287, 400612, 486239, 596330, 776758, 1e+06],
                            [1, 1.07895, 1.16667, 1.39035, 1.66667, 1.77632, 1.8])


@cache('step')
def npv_pv_income():
    """
    Real Name: b'NPV PV Income'
    Original Eqn: b'-PV monthly Income*((1-(1+Discount Rate)^(PV Life+1))/Discount Rate)'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return -pv_monthly_income() * ((1 - (1 + discount_rate())**(pv_life() + 1)) / discount_rate())


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
    Original Eqn: b'WITH LOOKUP ( Direct Defection NPV, ([(-5000,0)-(20000,20)],(-5000,1),(0,1.5),(5000,2),(20000,2.5) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(direct_defection_npv(), [-5000, 0, 5000, 20000], [1, 1.5, 2, 2.5])


@cache('step')
def effect_of_installing_battery_npv_on_imitation():
    """
    Real Name: b'effect of installing battery NPV on imitation'
    Original Eqn: b'WITH LOOKUP ( Installing Battery NPV, ([(0,0)-(40000,20)],(0,1),(5000,1.5),(20000,2),(40000,2.5) ))'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(installing_battery_npv(), [0, 5000, 20000, 40000], [1, 1.5, 2, 2.5])


@cache('step')
def effect_of_installing_battery_npv_on_innovation():
    """
    Real Name: b'effect of installing battery NPV on innovation'
    Original Eqn: b'WITH LOOKUP ( Installing Battery NPV, ([(-5000,0)-(20000,20)],(-5000,1),(0,1.5),(5000,2),(20000,2.5) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(installing_battery_npv(), [-5000, 0, 5000, 20000], [1, 1.5, 2, 2.5])


@cache('step')
def indicated_change_in_prosumer_demand():
    """
    Real Name: b'indicated change in Prosumer Demand'
    Original Eqn: b'change in electricity tariff*price eleasticity of prosumers*Prosumer Average Demand/\\\\ Electricity Tariff'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return change_in_electricity_tariff() * price_eleasticity_of_prosumers(
    ) * prosumer_average_demand() / electricity_tariff()


@cache('step')
def indicated_change_in_regular_consumer_demand():
    """
    Real Name: b'indicated change in regular Consumer Demand'
    Original Eqn: b'change in electricity tariff*Regular Consumer Average Demand*price eleasticity of regular consumers\\\\ /Electricity Tariff'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return change_in_electricity_tariff() * regular_consumer_average_demand(
    ) * price_eleasticity_of_regular_consumers() / electricity_tariff()


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
def electricity_tariff():
    """
    Real Name: b'Electricity Tariff'
    Original Eqn: b'INTEG ( change in electricity tariff, 0.15)'
    Units: b'Dollar/kWh'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_electricity_tariff()


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
def regular_consumers():
    """
    Real Name: b'Regular Consumers'
    Original Eqn: b'INTEG ( New Regular Consumers-Direct Defection By Imitation-Direct Defection by Innovation-installing PV by imitation\\\\ -installing PV by Innovation, 4e+06)'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_regular_consumers()


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


@cache('step')
def new_prosumers():
    """
    Real Name: b'New Prosumers'
    Original Eqn: b'Consumer Growth*New Prosumer Ratio'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return consumer_growth() * new_prosumer_ratio()


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
def installing_battery_imitation_percent():
    """
    Real Name: b'installing battery imitation percent'
    Original Eqn: b'Defectors*installing battery imitation factor*effect of installing battery NPV on imitation'
    Units: b'1/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return defectors() * installing_battery_imitation_factor(
    ) * effect_of_installing_battery_npv_on_imitation()


@cache('step')
def total_consumers():
    """
    Real Name: b'Total Consumers'
    Original Eqn: b'INTEG ( Consumer Growth, 4e+06)'
    Units: b'Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_total_consumers()


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
def change_in_regular_consumer_demand():
    """
    Real Name: b'change in Regular Consumer Demand'
    Original Eqn: b'effect of Maximum Regular Consumer Demand*effect of Minimum Regular Consumer Demand*\\\\ Indicated Regular Customer Demand/time to adjust Regular Consumer demand'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_maximum_regular_consumer_demand() * effect_of_minimum_regular_consumer_demand(
    ) * indicated_regular_customer_demand() / time_to_adjust_regular_consumer_demand()


@cache('step')
def indicated_regular_customer_demand():
    """
    Real Name: b'Indicated Regular Customer Demand'
    Original Eqn: b'INTEG ( change in indicated regular consumer demand-change in Regular Consumer Demand, 0)'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_indicated_regular_customer_demand()


@cache('step')
def change_in_indicated_regular_consumer_demand():
    """
    Real Name: b'change in indicated regular consumer demand'
    Original Eqn: b'indicated change in regular Consumer Demand'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return indicated_change_in_regular_consumer_demand()


@cache('step')
def regular_consumer_average_demand():
    """
    Real Name: b'Regular Consumer Average Demand'
    Original Eqn: b'INTEG ( change in Regular Consumer Demand, 500)'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_regular_consumer_average_demand()


@cache('step')
def indicated_prosumer_demand():
    """
    Real Name: b'Indicated Prosumer Demand'
    Original Eqn: b'INTEG ( change in indicated prosumer demand-change in Prosumer Demand, 0)'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_indicated_prosumer_demand()


@cache('step')
def prosumer_average_demand():
    """
    Real Name: b'Prosumer Average Demand'
    Original Eqn: b'INTEG ( change in Prosumer Demand, 150)'
    Units: b'kWh/Month/Customer'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_prosumer_average_demand()


@cache('step')
def change_in_indicated_prosumer_demand():
    """
    Real Name: b'change in indicated prosumer demand'
    Original Eqn: b'indicated change in Prosumer Demand'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return indicated_change_in_prosumer_demand()


@cache('step')
def change_in_prosumer_demand():
    """
    Real Name: b'change in Prosumer Demand'
    Original Eqn: b'effect of Prosumer Maximum Demand*effect of Prosumer Minimum Demand*Indicated Prosumer Demand\\\\ /time to adjust Prosumer Demand'
    Units: b'kWh/(Month*Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_prosumer_maximum_demand() * effect_of_prosumer_minimum_demand(
    ) * indicated_prosumer_demand() / time_to_adjust_prosumer_demand()


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
def installing_pv_imitation_factor():
    """
    Real Name: b'installing PV imitation factor'
    Original Eqn: b'effect of PV NPV*final yearly percent/12/1e+06'
    Units: b'1/(Month*Customer)'
    Limits: (None, None)
    Type: component

    b''
    """
    return effect_of_pv_npv() * final_yearly_percent() / 12 / 1e+06


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
def installing_pv_by_innovation():
    """
    Real Name: b'installing PV by Innovation'
    Original Eqn: b'IF THEN ELSE( Regular Consumers > 0, effect of PV NPV*installing PV innovation factor\\\\ *Regular Consumers , 0 )'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(
        regular_consumers() > 0,
        effect_of_pv_npv() * installing_pv_innovation_factor() * regular_consumers(), 0)


@cache('step')
def effect_of_pv_npv():
    """
    Real Name: b'effect of PV NPV'
    Original Eqn: b'WITH LOOKUP ( NPV PV Ratio, ([(0,0)-(4,3)],(0,1),(0.905199,1.06579),(1.61468,1.44737),(2,2),(2.36086,2.64474),(\\\\ 2.92355,2.90789),(4,3) ))'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(npv_pv_ratio(), [0, 0.905199, 1.61468, 2, 2.36086, 2.92355, 4],
                            [1, 1.06579, 1.44737, 2, 2.64474, 2.90789, 3])


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
    Original Eqn: b'0.03/12'
    Units: b'1/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.03 / 12


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


@cache('step')
def installing_pv_imitation_percent():
    """
    Real Name: b'installing PV imitation percent'
    Original Eqn: b'installing PV imitation factor*Total Customers with PV'
    Units: b'1/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return installing_pv_imitation_factor() * total_customers_with_pv()


@cache('step')
def effect_of_customers_on_pv_cost():
    """
    Real Name: b'effect of Customers on PV Cost'
    Original Eqn: b'WITH LOOKUP ( Total Customers with PV, ([(0,1)-(1e+06,2)],(100000,1),(278287,1.07895),(400612,1.16667),(486239,1.39035),(596330\\\\ ,1.66667),(776758,1.77632),(1e+06 ,1.8) ))'
    Units: b''
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(total_customers_with_pv(),
                            [100000, 278287, 400612, 486239, 596330, 776758, 1e+06],
                            [1, 1.07895, 1.16667, 1.39035, 1.66667, 1.77632, 1.8])


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
def effect_of_prosumer_minimum_demand():
    """
    Real Name: b'effect of Prosumer Minimum Demand'
    Original Eqn: b'WITH LOOKUP ( Minimum Average Prosumer Demand/Prosumer Average Demand, ([(0,0)-(1,1)],(0,1),(0.8,1),(1,0) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(minimum_average_prosumer_demand() / prosumer_average_demand(),
                            [0, 0.8, 1], [1, 1, 0])


@cache('step')
def effect_of_maximum_regular_consumer_demand():
    """
    Real Name: b'effect of Maximum Regular Consumer Demand'
    Original Eqn: b'WITH LOOKUP ( Regular Consumer Average Demand/Maximum Average Regular Consumer Demand, ([(0,0)-(1,1)],(0,1),(0.8,1),(1,0) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(
        regular_consumer_average_demand() / maximum_average_regular_consumer_demand(), [0, 0.8, 1],
        [1, 1, 0])


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


@cache('step')
def effect_of_minimum_regular_consumer_demand():
    """
    Real Name: b'effect of Minimum Regular Consumer Demand'
    Original Eqn: b'WITH LOOKUP ( Minimum Average Regular Consumer Demand/Regular Consumer Average Demand, ([(0,0)-(1,1)],(0,1),(0.8,1),(1,0) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(
        minimum_average_regular_consumer_demand() / regular_consumer_average_demand(), [0, 0.8, 1],
        [1, 1, 0])


@cache('run')
def maximum_average_prosumer_demand():
    """
    Real Name: b'Maximum Average Prosumer Demand'
    Original Eqn: b'180'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 180


@cache('run')
def maximum_average_regular_consumer_demand():
    """
    Real Name: b'Maximum Average Regular Consumer Demand'
    Original Eqn: b'600'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 600


@cache('run')
def minimum_average_prosumer_demand():
    """
    Real Name: b'Minimum Average Prosumer Demand'
    Original Eqn: b'120'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 120


@cache('run')
def minimum_average_regular_consumer_demand():
    """
    Real Name: b'Minimum Average Regular Consumer Demand'
    Original Eqn: b'400'
    Units: b'kWh/(Month*Customer)'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 400


@cache('step')
def indicated_tariff_change():
    """
    Real Name: b'Indicated Tariff Change'
    Original Eqn: b'Budget Deficit/Utility Energy Sale/Tariff Correction Period'
    Units: b'Dollar/(Month*kWh)'
    Limits: (None, None)
    Type: component

    b''
    """
    return budget_deficit() / utility_energy_sale() / tariff_correction_period()


@cache('run')
def tariff_correction_period():
    """
    Real Name: b'Tariff Correction Period'
    Original Eqn: b'24'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 24


@cache('step')
def effect_of_prosumer_maximum_demand():
    """
    Real Name: b'effect of Prosumer Maximum Demand'
    Original Eqn: b'WITH LOOKUP ( Prosumer Average Demand/Maximum Average Prosumer Demand, ([(0,0)-(1,1)],(0,1),(0.8,1),(1,0) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(prosumer_average_demand() / maximum_average_prosumer_demand(),
                            [0, 0.8, 1], [1, 1, 0])


@cache('run')
def price_eleasticity_of_prosumers():
    """
    Real Name: b'price eleasticity of prosumers'
    Original Eqn: b'-0.2'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return -0.2


@cache('run')
def price_eleasticity_of_regular_consumers():
    """
    Real Name: b'price eleasticity of regular consumers'
    Original Eqn: b'-0.1'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: constant

    b''
    """
    return -0.1


@cache('step')
def budget_deficit():
    """
    Real Name: b'Budget Deficit'
    Original Eqn: b'INTEG ( Monthly Income Shortfall, 0)'
    Units: b'Dollar'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_budget_deficit()


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
    Original Eqn: b'WITH LOOKUP ( Minimum PV Cost/PV Cost, ([(0,0)-(1,1)],(0,1),(0.25,0.95),(0.4,0.8),(0.5,0.5),(0.6,0.2),(0.75,0.05),(1,0) ))'
    Units: b'Dmnl'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.lookup(minimum_pv_cost() / pv_cost(), [0, 0.25, 0.4, 0.5, 0.6, 0.75, 1],
                            [1, 0.95, 0.8, 0.5, 0.2, 0.05, 0])


@cache('step')
def energy_procurement():
    """
    Real Name: b'Energy Procurement'
    Original Eqn: b'Utility Energy Sale'
    Units: b'kWh/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return utility_energy_sale()


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
def final_yearly_percent():
    """
    Real Name: b'final yearly percent'
    Original Eqn: b'0.005'
    Units: b''
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.005


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
def installing_battery_imitation_factor():
    """
    Real Name: b'installing battery imitation factor'
    Original Eqn: b'final yearly percent/(12*1e+06*5)'
    Units: b'1/(Customer*Month)'
    Limits: (None, None)
    Type: component

    b''
    """
    return final_yearly_percent() / (12 * 1e+06 * 5)


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


@cache('step')
def pv_cost():
    """
    Real Name: b'PV Cost'
    Original Eqn: b'INTEG ( -PV Cost Reduction, 4000)'
    Units: b'Dollar/kw'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_pv_cost()


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


@cache('step')
def installing_pv_by_imitation():
    """
    Real Name: b'installing PV by imitation'
    Original Eqn: b'IF THEN ELSE(Regular Consumers>0,installing PV imitation percent*Regular Consumers,0\\\\ )'
    Units: b'Customer/Month'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(regular_consumers() > 0,
                                  installing_pv_imitation_percent() * regular_consumers(), 0)


@cache('run')
def installing_battery_innovation_factor():
    """
    Real Name: b'installing battery innovation factor'
    Original Eqn: b'0.01/12'
    Units: b'1/Month'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.01 / 12


@cache('run')
def installing_pv_innovation_factor():
    """
    Real Name: b'installing PV innovation factor'
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
    Original Eqn: b'240'
    Units: b'Month'
    Limits: (None, None)
    Type: constant

    b'The final time for the simulation.'
    """
    return 240


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
    Original Eqn: b'1'
    Units: b'Month'
    Limits: (0.0, None)
    Type: constant

    b'The time step for the simulation.'
    """
    return 1


_integ_battery_cost = functions.Integ(lambda: -battery_cost_reduction(), lambda: 600)

_integ_defectors = functions.Integ(
    lambda: direct_defection_by_imitation() + direct_defection_by_innovation(
    ) + installing_battery_by_imitation() + installing_battery_by_innovation() + new_defectors(),
    lambda: 0)

_integ_prosumers = functions.Integ(
    lambda: installing_pv_by_imitation() + installing_pv_by_innovation() + new_prosumers() -
    installing_battery_by_imitation() - installing_battery_by_innovation(), lambda: 0)

_integ_electricity_tariff = functions.Integ(lambda: change_in_electricity_tariff(), lambda: 0.15)

_integ_regular_consumers = functions.Integ(
    lambda: new_regular_consumers() - direct_defection_by_imitation() -
    direct_defection_by_innovation() - installing_pv_by_imitation() - installing_pv_by_innovation(
    ), lambda: 4e+06)

_integ_total_consumers = functions.Integ(lambda: consumer_growth(), lambda: 4e+06)

_integ_indicated_regular_customer_demand = functions.Integ(
    lambda: change_in_indicated_regular_consumer_demand() - change_in_regular_consumer_demand(),
    lambda: 0)

_integ_regular_consumer_average_demand = functions.Integ(
    lambda: change_in_regular_consumer_demand(), lambda: 500)

_integ_indicated_prosumer_demand = functions.Integ(
    lambda: change_in_indicated_prosumer_demand() - change_in_prosumer_demand(), lambda: 0)

_integ_prosumer_average_demand = functions.Integ(lambda: change_in_prosumer_demand(), lambda: 150)

_integ_budget_deficit = functions.Integ(lambda: monthly_income_shortfall(), lambda: 0)

_integ_pv_cost = functions.Integ(lambda: -pv_cost_reduction(), lambda: 4000)
