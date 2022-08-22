"""
Python model 'net metering-no fixed tariff.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import integer, modulo, if_then_else
from pysd.py_backend.statefuls import Integ

__pysd_version__ = "2.2.4"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "Prosumer Demand Change Limit": "prosumer_demand_change_limit",
    "Minimum Average Prosumer Demand": "minimum_average_prosumer_demand",
    "Maximum Average Prosumer Demand": "maximum_average_prosumer_demand",
    "Maximum Average Regular Consumer Demand": "maximum_average_regular_consumer_demand",
    "Minimum Average Regular Consumer Demand": "minimum_average_regular_consumer_demand",
    "Regular Consumer Demand Change Limit": "regular_consumer_demand_change_limit",
    "change in indicated regular consumer demand": "change_in_indicated_regular_consumer_demand",
    "installing PV by Innovation": "installing_pv_by_innovation",
    "installing PV imitation factor": "installing_pv_imitation_factor",
    "effect of PV ratio Limit": "effect_of_pv_ratio_limit",
    "Direct Defection By Imitation": "direct_defection_by_imitation",
    "Direct Defection by Innovation": "direct_defection_by_innovation",
    "New Regular Consumer Ratio": "new_regular_consumer_ratio",
    "PV Customers Ratio": "pv_customers_ratio",
    "Defectors Ratio": "defectors_ratio",
    "effect of Customers on Battery Cost": "effect_of_customers_on_battery_cost",
    "PV visibility effect on immitation": "pv_visibility_effect_on_immitation",
    "PV Potential": "pv_potential",
    "Total Potential PV Customers": "total_potential_pv_customers",
    "installing PV by imitation": "installing_pv_by_imitation",
    "New Prosumers": "new_prosumers",
    "Total Consumers": "total_consumers",
    "Installing Battery By Imitation": "installing_battery_by_imitation",
    "direct defection imitation factor": "direct_defection_imitation_factor",
    "installing battery imitation factor": "installing_battery_imitation_factor",
    "Regular Consumers": "regular_consumers",
    "effect of Customers on PV Cost": "effect_of_customers_on_pv_cost",
    "PV Cost": "pv_cost",
    "Electricity Tariff": "electricity_tariff",
    "Initial PV Cost": "initial_pv_cost",
    "Battery Cost": "battery_cost",
    "Initial Battery Cost": "initial_battery_cost",
    "Initial Budget Deficit": "initial_budget_deficit",
    "Budget Deficit": "budget_deficit",
    "Initial Average Consumer Demand": "initial_average_consumer_demand",
    "Initial Prosumer Demand": "initial_prosumer_demand",
    "Regular Consumer Average Demand": "regular_consumer_average_demand",
    "Prosumer Average Demand": "prosumer_average_demand",
    "Initial Electricity Tariff": "initial_electricity_tariff",
    "Initial Number of Consumers": "initial_number_of_consumers",
    "Installing Battery by Innovation": "installing_battery_by_innovation",
    "Electricity Loss": "electricity_loss",
    "Deficit recovery period": "deficit_recovery_period",
    "Indicated Tariff Change": "indicated_tariff_change",
    "Energy Procurement": "energy_procurement",
    "percent std effect of remaining time": "percent_std_effect_of_remaining_time",
    "std of effect of remaining time": "std_of_effect_of_remaining_time",
    "effect of remaining time on change in electricity tariff": "effect_of_remaining_time_on_change_in_electricity_tariff",
    "tariff correction remaining time": "tariff_correction_remaining_time",
    "pi": "pi",
    "change in electricity tariff": "change_in_electricity_tariff",
    "change in Regular Consumer Demand": "change_in_regular_consumer_demand",
    "change in Prosumer Demand": "change_in_prosumer_demand",
    "change in indicated prosumer demand": "change_in_indicated_prosumer_demand",
    "Average Daily Battery Eenergy": "average_daily_battery_eenergy",
    "Battery Cost Reduction": "battery_cost_reduction",
    "Battery Life": "battery_life",
    "effect of Minimum Battery Cost": "effect_of_minimum_battery_cost",
    "Direct Defection Total Cost": "direct_defection_total_cost",
    "Direct Defector Monthly Savings": "direct_defector_monthly_savings",
    "Direct Defector Net Present Savings": "direct_defector_net_present_savings",
    "Discount Rate": "discount_rate",
    "Consumer Growth": "consumer_growth",
    "Defectors": "defectors",
    "effect of direct defection NPV on imitation": "effect_of_direct_defection_npv_on_imitation",
    "Direct Defection NPV": "direct_defection_npv",
    '"No. Batteries"': "no_batteries",
    '"No. Bettery Replacement"': "no_bettery_replacement",
    "NPV PV Income": "npv_pv_income",
    "Total PV Cost": "total_pv_cost",
    "effect of direct defection NPV on innovation": "effect_of_direct_defection_npv_on_innovation",
    "effect of installing battery NPV on imitation": "effect_of_installing_battery_npv_on_imitation",
    "effect of installing battery NPV on innovation": "effect_of_installing_battery_npv_on_innovation",
    "indicated change in Prosumer Demand": "indicated_change_in_prosumer_demand",
    "indicated change in regular Consumer Demand": "indicated_change_in_regular_consumer_demand",
    "Prosumers": "prosumers",
    "Total Customers with PV": "total_customers_with_pv",
    "Installing Battery NPV": "installing_battery_npv",
    '"No. PVs"': "no_pvs",
    "Total Battery Cost": "total_battery_cost",
    "PV monthly Income": "pv_monthly_income",
    "New Regular Consumers": "new_regular_consumers",
    "Storage to Daily Load Factor": "storage_to_daily_load_factor",
    "Income": "income",
    "Reliablity Margin": "reliablity_margin",
    "New Defectors": "new_defectors",
    "Actual Regular Customer Demand change": "actual_regular_customer_demand_change",
    "Actual Prosumer Demand Change": "actual_prosumer_demand_change",
    "New Prosumer Ratio": "new_prosumer_ratio",
    "NPV PV Ratio": "npv_pv_ratio",
    "effect of PV NPV": "effect_of_pv_npv",
    "NPV PV": "npv_pv",
    "population growth rate": "population_growth_rate",
    "New Defector Ratio": "new_defector_ratio",
    "PV Life": "pv_life",
    "PV monthly Generation": "pv_monthly_generation",
    "PV size": "pv_size",
    "Normal Battery Cost Reduction rate": "normal_battery_cost_reduction_rate",
    "Minimum Battery Cost": "minimum_battery_cost",
    "time to adjust Regular Consumer demand": "time_to_adjust_regular_consumer_demand",
    "time to adjust Prosumer Demand": "time_to_adjust_prosumer_demand",
    "Prosumers Demand": "prosumers_demand",
    "Tariff Correction Period": "tariff_correction_period",
    "price elasticity of prosumers": "price_elasticity_of_prosumers",
    "price elasticity of regular consumers": "price_elasticity_of_regular_consumers",
    "Desired Income": "desired_income",
    "Permited Profit": "permited_profit",
    "effect of Minimum PV Cost": "effect_of_minimum_pv_cost",
    "PV Cost Reduction": "pv_cost_reduction",
    "Immitation Factor": "immitation_factor",
    "Fixed Costs": "fixed_costs",
    "Generation Price": "generation_price",
    "Total Costs": "total_costs",
    "Variable Costs": "variable_costs",
    "Normal PV Cost Reduction rate": "normal_pv_cost_reduction_rate",
    "Minimum PV Cost": "minimum_pv_cost",
    "Monthly Income Shortfall": "monthly_income_shortfall",
    "Regular Consumers Demand": "regular_consumers_demand",
    "Utility Energy Sale": "utility_energy_sale",
    "Innovation factor": "innovation_factor",
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

_dependencies = {
    "prosumer_demand_change_limit": {},
    "minimum_average_prosumer_demand": {
        "initial_prosumer_demand": 1,
        "prosumer_demand_change_limit": 1,
    },
    "maximum_average_prosumer_demand": {
        "initial_prosumer_demand": 1,
        "prosumer_demand_change_limit": 1,
    },
    "maximum_average_regular_consumer_demand": {
        "initial_average_consumer_demand": 1,
        "regular_consumer_demand_change_limit": 1,
    },
    "minimum_average_regular_consumer_demand": {
        "initial_average_consumer_demand": 1,
        "regular_consumer_demand_change_limit": 1,
    },
    "regular_consumer_demand_change_limit": {},
    "change_in_indicated_regular_consumer_demand": {
        "indicated_change_in_regular_consumer_demand": 3,
        "regular_consumer_average_demand": 4,
        "maximum_average_regular_consumer_demand": 2,
        "minimum_average_regular_consumer_demand": 2,
    },
    "installing_pv_by_innovation": {
        "effect_of_pv_npv": 1,
        "innovation_factor": 1,
        "regular_consumers": 1,
        "effect_of_pv_ratio_limit": 1,
    },
    "installing_pv_imitation_factor": {
        "effect_of_pv_npv": 1,
        "immitation_factor": 1,
        "pv_customers_ratio": 1,
        "pv_visibility_effect_on_immitation": 1,
    },
    "effect_of_pv_ratio_limit": {"pv_customers_ratio": 1},
    "direct_defection_by_imitation": {
        "direct_defection_imitation_factor": 1,
        "regular_consumers": 1,
        "effect_of_pv_ratio_limit": 1,
    },
    "direct_defection_by_innovation": {
        "innovation_factor": 1,
        "regular_consumers": 1,
        "effect_of_direct_defection_npv_on_innovation": 1,
        "effect_of_pv_ratio_limit": 1,
    },
    "new_regular_consumer_ratio": {"new_defector_ratio": 1, "new_prosumer_ratio": 1},
    "pv_customers_ratio": {
        "total_customers_with_pv": 1,
        "total_potential_pv_customers": 1,
    },
    "defectors_ratio": {"defectors": 1, "total_potential_pv_customers": 1},
    "effect_of_customers_on_battery_cost": {"defectors_ratio": 1},
    "pv_visibility_effect_on_immitation": {},
    "pv_potential": {},
    "total_potential_pv_customers": {"pv_potential": 1, "total_consumers": 1},
    "installing_pv_by_imitation": {
        "installing_pv_imitation_factor": 1,
        "regular_consumers": 1,
        "effect_of_pv_ratio_limit": 1,
    },
    "new_prosumers": {
        "consumer_growth": 1,
        "new_prosumer_ratio": 1,
        "effect_of_pv_ratio_limit": 1,
    },
    "total_consumers": {"_integ_total_consumers": 1},
    "installing_battery_by_imitation": {
        "prosumers": 2,
        "installing_battery_imitation_factor": 1,
    },
    "direct_defection_imitation_factor": {
        "immitation_factor": 1,
        "effect_of_direct_defection_npv_on_imitation": 1,
        "defectors_ratio": 1,
    },
    "installing_battery_imitation_factor": {
        "defectors_ratio": 1,
        "effect_of_installing_battery_npv_on_imitation": 1,
        "immitation_factor": 1,
    },
    "regular_consumers": {"_integ_regular_consumers": 1},
    "effect_of_customers_on_pv_cost": {"pv_customers_ratio": 1},
    "pv_cost": {"_integ_pv_cost": 1},
    "electricity_tariff": {"_integ_electricity_tariff": 1},
    "initial_pv_cost": {},
    "battery_cost": {"_integ_battery_cost": 1},
    "initial_battery_cost": {},
    "initial_budget_deficit": {},
    "budget_deficit": {"_integ_budget_deficit": 1},
    "initial_average_consumer_demand": {},
    "initial_prosumer_demand": {},
    "regular_consumer_average_demand": {"_integ_regular_consumer_average_demand": 1},
    "prosumer_average_demand": {"_integ_prosumer_average_demand": 1},
    "initial_electricity_tariff": {},
    "initial_number_of_consumers": {},
    "installing_battery_by_innovation": {
        "innovation_factor": 1,
        "prosumers": 1,
        "effect_of_installing_battery_npv_on_innovation": 1,
    },
    "electricity_loss": {},
    "deficit_recovery_period": {},
    "indicated_tariff_change": {
        "budget_deficit": 1,
        "utility_energy_sale": 1,
        "deficit_recovery_period": 1,
    },
    "energy_procurement": {"utility_energy_sale": 1, "electricity_loss": 1},
    "percent_std_effect_of_remaining_time": {},
    "std_of_effect_of_remaining_time": {
        "percent_std_effect_of_remaining_time": 1,
        "tariff_correction_period": 1,
    },
    "effect_of_remaining_time_on_change_in_electricity_tariff": {
        "std_of_effect_of_remaining_time": 2,
        "pi": 1,
        "tariff_correction_remaining_time": 1,
    },
    "tariff_correction_remaining_time": {"time": 2, "tariff_correction_period": 3},
    "pi": {},
    "change_in_electricity_tariff": {
        "indicated_tariff_change": 1,
        "effect_of_remaining_time_on_change_in_electricity_tariff": 1,
    },
    "change_in_regular_consumer_demand": {
        "actual_regular_customer_demand_change": 1,
        "time_to_adjust_regular_consumer_demand": 1,
    },
    "change_in_prosumer_demand": {
        "actual_prosumer_demand_change": 1,
        "time_to_adjust_prosumer_demand": 1,
    },
    "change_in_indicated_prosumer_demand": {
        "prosumer_average_demand": 4,
        "indicated_change_in_prosumer_demand": 3,
        "maximum_average_prosumer_demand": 2,
        "minimum_average_prosumer_demand": 2,
    },
    "average_daily_battery_eenergy": {
        "regular_consumer_average_demand": 1,
        "storage_to_daily_load_factor": 1,
    },
    "battery_cost_reduction": {
        "effect_of_customers_on_battery_cost": 1,
        "effect_of_minimum_battery_cost": 1,
        "normal_battery_cost_reduction_rate": 1,
        "battery_cost": 1,
    },
    "battery_life": {},
    "effect_of_minimum_battery_cost": {"minimum_battery_cost": 1, "battery_cost": 1},
    "direct_defection_total_cost": {"total_battery_cost": 1, "total_pv_cost": 1},
    "direct_defector_monthly_savings": {
        "electricity_tariff": 1,
        "regular_consumer_average_demand": 1,
    },
    "direct_defector_net_present_savings": {
        "direct_defector_monthly_savings": 1,
        "discount_rate": 2,
        "pv_life": 1,
    },
    "discount_rate": {},
    "consumer_growth": {"population_growth_rate": 1, "total_consumers": 1},
    "defectors": {"_integ_defectors": 1},
    "effect_of_direct_defection_npv_on_imitation": {"direct_defection_npv": 1},
    "direct_defection_npv": {
        "direct_defector_net_present_savings": 1,
        "direct_defection_total_cost": 1,
    },
    "no_batteries": {"average_daily_battery_eenergy": 1},
    "no_bettery_replacement": {"pv_life": 3, "battery_life": 3},
    "npv_pv_income": {"pv_monthly_income": 1, "discount_rate": 2, "pv_life": 1},
    "total_pv_cost": {"no_pvs": 1, "pv_cost": 1},
    "effect_of_direct_defection_npv_on_innovation": {"direct_defection_npv": 1},
    "effect_of_installing_battery_npv_on_imitation": {"installing_battery_npv": 1},
    "effect_of_installing_battery_npv_on_innovation": {"installing_battery_npv": 1},
    "indicated_change_in_prosumer_demand": {
        "electricity_tariff": 2,
        "price_elasticity_of_prosumers": 2,
        "prosumer_average_demand": 2,
        "change_in_electricity_tariff": 1,
    },
    "indicated_change_in_regular_consumer_demand": {
        "electricity_tariff": 2,
        "price_elasticity_of_regular_consumers": 2,
        "regular_consumer_average_demand": 2,
        "change_in_electricity_tariff": 1,
    },
    "prosumers": {"_integ_prosumers": 1},
    "total_customers_with_pv": {"defectors": 1, "prosumers": 1},
    "installing_battery_npv": {"direct_defection_npv": 1, "npv_pv": 1},
    "no_pvs": {
        "regular_consumer_average_demand": 1,
        "reliablity_margin": 1,
        "pv_monthly_generation": 1,
    },
    "total_battery_cost": {
        "battery_cost": 1,
        "no_bettery_replacement": 1,
        "no_batteries": 1,
    },
    "pv_monthly_income": {"electricity_tariff": 1, "pv_monthly_generation": 1},
    "new_regular_consumers": {"consumer_growth": 1, "new_regular_consumer_ratio": 1},
    "storage_to_daily_load_factor": {},
    "income": {"electricity_tariff": 1, "utility_energy_sale": 1},
    "reliablity_margin": {},
    "new_defectors": {
        "consumer_growth": 1,
        "new_defector_ratio": 1,
        "effect_of_direct_defection_npv_on_imitation": 1,
        "effect_of_direct_defection_npv_on_innovation": 1,
    },
    "actual_regular_customer_demand_change": {
        "_integ_actual_regular_customer_demand_change": 1
    },
    "actual_prosumer_demand_change": {"_integ_actual_prosumer_demand_change": 1},
    "new_prosumer_ratio": {"effect_of_pv_npv": 1},
    "npv_pv_ratio": {"npv_pv": 1, "pv_cost": 1},
    "effect_of_pv_npv": {"npv_pv_ratio": 1},
    "npv_pv": {"npv_pv_income": 1, "pv_cost": 1, "pv_size": 1},
    "population_growth_rate": {},
    "new_defector_ratio": {},
    "pv_life": {},
    "pv_monthly_generation": {},
    "pv_size": {},
    "normal_battery_cost_reduction_rate": {},
    "minimum_battery_cost": {},
    "time_to_adjust_regular_consumer_demand": {},
    "time_to_adjust_prosumer_demand": {},
    "prosumers_demand": {"prosumer_average_demand": 1, "prosumers": 1},
    "tariff_correction_period": {},
    "price_elasticity_of_prosumers": {},
    "price_elasticity_of_regular_consumers": {},
    "desired_income": {"total_costs": 1, "permited_profit": 1},
    "permited_profit": {},
    "effect_of_minimum_pv_cost": {"minimum_pv_cost": 1, "pv_cost": 1},
    "pv_cost_reduction": {
        "effect_of_customers_on_pv_cost": 1,
        "effect_of_minimum_pv_cost": 1,
        "normal_pv_cost_reduction_rate": 1,
        "pv_cost": 1,
    },
    "immitation_factor": {},
    "fixed_costs": {},
    "generation_price": {},
    "total_costs": {"fixed_costs": 1, "variable_costs": 1},
    "variable_costs": {"energy_procurement": 1, "generation_price": 1},
    "normal_pv_cost_reduction_rate": {},
    "minimum_pv_cost": {},
    "monthly_income_shortfall": {"desired_income": 1, "income": 1},
    "regular_consumers_demand": {
        "regular_consumer_average_demand": 1,
        "regular_consumers": 1,
    },
    "utility_energy_sale": {"prosumers_demand": 1, "regular_consumers_demand": 1},
    "innovation_factor": {},
    "final_time": {},
    "initial_time": {},
    "saveper": {"time_step": 1},
    "time_step": {},
    "_integ_total_consumers": {
        "initial": {"initial_number_of_consumers": 1},
        "step": {"consumer_growth": 1},
    },
    "_integ_regular_consumers": {
        "initial": {"initial_number_of_consumers": 1},
        "step": {
            "new_regular_consumers": 1,
            "direct_defection_by_imitation": 1,
            "direct_defection_by_innovation": 1,
            "installing_pv_by_imitation": 1,
            "installing_pv_by_innovation": 1,
        },
    },
    "_integ_pv_cost": {
        "initial": {"initial_pv_cost": 1},
        "step": {"pv_cost_reduction": 1},
    },
    "_integ_electricity_tariff": {
        "initial": {"initial_electricity_tariff": 1},
        "step": {"change_in_electricity_tariff": 1},
    },
    "_integ_battery_cost": {
        "initial": {"initial_battery_cost": 1},
        "step": {"battery_cost_reduction": 1},
    },
    "_integ_budget_deficit": {
        "initial": {"initial_budget_deficit": 1},
        "step": {"monthly_income_shortfall": 1},
    },
    "_integ_regular_consumer_average_demand": {
        "initial": {"initial_average_consumer_demand": 1},
        "step": {"change_in_regular_consumer_demand": 1},
    },
    "_integ_prosumer_average_demand": {
        "initial": {"initial_prosumer_demand": 1},
        "step": {"change_in_prosumer_demand": 1},
    },
    "_integ_defectors": {
        "initial": {},
        "step": {
            "direct_defection_by_imitation": 1,
            "direct_defection_by_innovation": 1,
            "installing_battery_by_imitation": 1,
            "installing_battery_by_innovation": 1,
            "new_defectors": 1,
        },
    },
    "_integ_prosumers": {
        "initial": {},
        "step": {
            "installing_pv_by_imitation": 1,
            "installing_pv_by_innovation": 1,
            "new_prosumers": 1,
            "installing_battery_by_imitation": 1,
            "installing_battery_by_innovation": 1,
        },
    },
    "_integ_actual_regular_customer_demand_change": {
        "initial": {},
        "step": {
            "change_in_indicated_regular_consumer_demand": 1,
            "change_in_regular_consumer_demand": 1,
        },
    },
    "_integ_actual_prosumer_demand_change": {
        "initial": {},
        "step": {
            "change_in_indicated_prosumer_demand": 1,
            "change_in_prosumer_demand": 1,
        },
    },
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 600,
    "time_step": lambda: 0.0078125,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 600
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return __data["time"].final_time()


def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return __data["time"].initial_time()


def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Month
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return __data["time"].saveper()


def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 0.0078125
    Units: Month
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return __data["time"].time_step()


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################


def prosumer_demand_change_limit():
    """
    Real Name: Prosumer Demand Change Limit
    Original Eqn: 0.2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.2


def minimum_average_prosumer_demand():
    """
    Real Name: Minimum Average Prosumer Demand
    Original Eqn: Initial Prosumer Demand*(1-Prosumer Demand Change Limit)
    Units: kWh/(Customer*Month)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_prosumer_demand() * (1 - prosumer_demand_change_limit())


def maximum_average_prosumer_demand():
    """
    Real Name: Maximum Average Prosumer Demand
    Original Eqn: Initial Prosumer Demand*(1+Prosumer Demand Change Limit)
    Units: kWh/(Customer*Month)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_prosumer_demand() * (1 + prosumer_demand_change_limit())


def maximum_average_regular_consumer_demand():
    """
    Real Name: Maximum Average Regular Consumer Demand
    Original Eqn: Initial Average Consumer Demand*(1+Regular Consumer Demand Change Limit)
    Units: kWh/(Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_average_consumer_demand() * (
        1 + regular_consumer_demand_change_limit()
    )


def minimum_average_regular_consumer_demand():
    """
    Real Name: Minimum Average Regular Consumer Demand
    Original Eqn: Initial Average Consumer Demand*(1-Regular Consumer Demand Change Limit)
    Units: kWh/(Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return initial_average_consumer_demand() * (
        1 - regular_consumer_demand_change_limit()
    )


def regular_consumer_demand_change_limit():
    """
    Real Name: Regular Consumer Demand Change Limit
    Original Eqn: 0.2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.2


def change_in_indicated_regular_consumer_demand():
    """
    Real Name: change in indicated regular consumer demand
    Original Eqn: IF THEN ELSE( indicated change in regular Consumer Demand+Regular Consumer Average Demand>Maximum Average Regular Consumer Demand, Maximum Average Regular Consumer Demand-Regular Consumer Average Demand , IF THEN ELSE( indicated change in regular Consumer Demand+Regular Consumer Average Demand<Minimum Average Regular Consumer Demand , Minimum Average Regular Consumer Demand-Regular Consumer Average Demand , indicated change in regular Consumer Demand ) )
    Units: kWh/(Month*Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None

    IF THEN ELSE( indicated change in regular Consumer Demand+Regular Consumer
        Average Demand>Maximum Average Regular Consumer Demand, Maximum Average
        Regular Consumer Demand-Regular Consumer Average Demand , IF THEN ELSE(
        indicated change in regular Consumer Demand+Regular Consumer Average
        Demand<Minimum Average Regular Consumer Demand , Minimum Average Regular
        Consumer Demand-Regular Consumer Average Demand , indicated change in
        regular Consumer Demand ) )
    """
    return if_then_else(
        indicated_change_in_regular_consumer_demand()
        + regular_consumer_average_demand()
        > maximum_average_regular_consumer_demand(),
        lambda: maximum_average_regular_consumer_demand()
        - regular_consumer_average_demand(),
        lambda: if_then_else(
            indicated_change_in_regular_consumer_demand()
            + regular_consumer_average_demand()
            < minimum_average_regular_consumer_demand(),
            lambda: minimum_average_regular_consumer_demand()
            - regular_consumer_average_demand(),
            lambda: indicated_change_in_regular_consumer_demand(),
        ),
    )


def installing_pv_by_innovation():
    """
    Real Name: installing PV by Innovation
    Original Eqn: effect of PV NPV*Innovation factor*Regular Consumers*effect of PV ratio Limit
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        effect_of_pv_npv()
        * innovation_factor()
        * regular_consumers()
        * effect_of_pv_ratio_limit()
    )


def installing_pv_imitation_factor():
    """
    Real Name: installing PV imitation factor
    Original Eqn: effect of PV NPV*Immitation Factor*PV Customers Ratio*PV visibility effect on immitation
    Units: 1/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        effect_of_pv_npv()
        * immitation_factor()
        * pv_customers_ratio()
        * pv_visibility_effect_on_immitation()
    )


def effect_of_pv_ratio_limit():
    """
    Real Name: effect of PV ratio Limit
    Original Eqn: 1-1/(1+EXP(95-100*PV Customers Ratio))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - 1 / (1 + np.exp(95 - 100 * pv_customers_ratio()))


def direct_defection_by_imitation():
    """
    Real Name: Direct Defection By Imitation
    Original Eqn: direct defection imitation factor*Regular Consumers*effect of PV ratio Limit
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        direct_defection_imitation_factor()
        * regular_consumers()
        * effect_of_pv_ratio_limit()
    )


def direct_defection_by_innovation():
    """
    Real Name: Direct Defection by Innovation
    Original Eqn: Innovation factor*Regular Consumers*effect of direct defection NPV on innovation*effect of PV ratio Limit
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        innovation_factor()
        * regular_consumers()
        * effect_of_direct_defection_npv_on_innovation()
        * effect_of_pv_ratio_limit()
    )


def new_regular_consumer_ratio():
    """
    Real Name: New Regular Consumer Ratio
    Original Eqn: 1-New Defector Ratio-New Prosumer Ratio
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - new_defector_ratio() - new_prosumer_ratio()


def pv_customers_ratio():
    """
    Real Name: PV Customers Ratio
    Original Eqn: Total Customers with PV/Total Potential PV Customers
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_customers_with_pv() / total_potential_pv_customers()


def defectors_ratio():
    """
    Real Name: Defectors Ratio
    Original Eqn: Defectors/Total Potential PV Customers
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return defectors() / total_potential_pv_customers()


def effect_of_customers_on_battery_cost():
    """
    Real Name: effect of Customers on Battery Cost
    Original Eqn: 1+1/(1+EXP(5-Defectors Ratio*15))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 + 1 / (1 + np.exp(5 - defectors_ratio() * 15))


def pv_visibility_effect_on_immitation():
    """
    Real Name: PV visibility effect on immitation
    Original Eqn: 3
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 3


def pv_potential():
    """
    Real Name: PV Potential
    Original Eqn: 0.3
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.3


def total_potential_pv_customers():
    """
    Real Name: Total Potential PV Customers
    Original Eqn: PV Potential*Total Consumers
    Units: Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pv_potential() * total_consumers()


def installing_pv_by_imitation():
    """
    Real Name: installing PV by imitation
    Original Eqn: installing PV imitation factor*Regular Consumers*effect of PV ratio Limit
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        installing_pv_imitation_factor()
        * regular_consumers()
        * effect_of_pv_ratio_limit()
    )


def new_prosumers():
    """
    Real Name: New Prosumers
    Original Eqn: Consumer Growth*New Prosumer Ratio*effect of PV ratio Limit
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return consumer_growth() * new_prosumer_ratio() * effect_of_pv_ratio_limit()


def total_consumers():
    """
    Real Name: Total Consumers
    Original Eqn: INTEG ( Consumer Growth, Initial Number of Consumers)
    Units: Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_total_consumers()


def installing_battery_by_imitation():
    """
    Real Name: Installing Battery By Imitation
    Original Eqn: IF THEN ELSE(Prosumers>0,Prosumers*installing battery imitation factor,0)
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        prosumers() > 0,
        lambda: prosumers() * installing_battery_imitation_factor(),
        lambda: 0,
    )


def direct_defection_imitation_factor():
    """
    Real Name: direct defection imitation factor
    Original Eqn: Immitation Factor*effect of direct defection NPV on imitation*Defectors Ratio
    Units: 1/(Customer*Month)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        immitation_factor()
        * effect_of_direct_defection_npv_on_imitation()
        * defectors_ratio()
    )


def installing_battery_imitation_factor():
    """
    Real Name: installing battery imitation factor
    Original Eqn: Defectors Ratio*effect of installing battery NPV on imitation*Immitation Factor
    Units: 1/(Customer*Month)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        defectors_ratio()
        * effect_of_installing_battery_npv_on_imitation()
        * immitation_factor()
    )


def regular_consumers():
    """
    Real Name: Regular Consumers
    Original Eqn: INTEG ( New Regular Consumers-Direct Defection By Imitation-Direct Defection by Innovation-installing PV by imitation-installing PV by Innovation, Initial Number of Consumers)
    Units: Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_regular_consumers()


def effect_of_customers_on_pv_cost():
    """
    Real Name: effect of Customers on PV Cost
    Original Eqn: 1+1/(1+EXP(5-PV Customers Ratio*15))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 + 1 / (1 + np.exp(5 - pv_customers_ratio() * 15))


def pv_cost():
    """
    Real Name: PV Cost
    Original Eqn: INTEG ( -PV Cost Reduction, Initial PV Cost)
    Units: Dollar/kw
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_pv_cost()


def electricity_tariff():
    """
    Real Name: Electricity Tariff
    Original Eqn: INTEG ( change in electricity tariff, Initial Electricity Tariff)
    Units: Dollar/kWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_electricity_tariff()


def initial_pv_cost():
    """
    Real Name: Initial PV Cost
    Original Eqn: 4000
    Units: Dollar/kw
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 4000


def battery_cost():
    """
    Real Name: Battery Cost
    Original Eqn: INTEG ( -Battery Cost Reduction, Initial Battery Cost)
    Units: Dollar/kWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_battery_cost()


def initial_battery_cost():
    """
    Real Name: Initial Battery Cost
    Original Eqn: 600
    Units: Dollar/kWh
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 600


def initial_budget_deficit():
    """
    Real Name: Initial Budget Deficit
    Original Eqn: 0
    Units: Dollar
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0


def budget_deficit():
    """
    Real Name: Budget Deficit
    Original Eqn: INTEG ( Monthly Income Shortfall, Initial Budget Deficit)
    Units: Dollar
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_budget_deficit()


def initial_average_consumer_demand():
    """
    Real Name: Initial Average Consumer Demand
    Original Eqn: 500
    Units: kWh/(Customer*Month)
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 500


def initial_prosumer_demand():
    """
    Real Name: Initial Prosumer Demand
    Original Eqn: 250
    Units: kWh/(Customer*Month)
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 250


def regular_consumer_average_demand():
    """
    Real Name: Regular Consumer Average Demand
    Original Eqn: INTEG ( change in Regular Consumer Demand, Initial Average Consumer Demand)
    Units: kWh/(Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_regular_consumer_average_demand()


def prosumer_average_demand():
    """
    Real Name: Prosumer Average Demand
    Original Eqn: INTEG ( change in Prosumer Demand, Initial Prosumer Demand)
    Units: kWh/Month/Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_prosumer_average_demand()


def initial_electricity_tariff():
    """
    Real Name: Initial Electricity Tariff
    Original Eqn: 0.15
    Units: Dollar/kWh
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.15


def initial_number_of_consumers():
    """
    Real Name: Initial Number of Consumers
    Original Eqn: 4e+06
    Units: Customer
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 4e06


def installing_battery_by_innovation():
    """
    Real Name: Installing Battery by Innovation
    Original Eqn: Innovation factor*Prosumers*effect of installing battery NPV on innovation
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        innovation_factor()
        * prosumers()
        * effect_of_installing_battery_npv_on_innovation()
    )


def electricity_loss():
    """
    Real Name: Electricity Loss
    Original Eqn: 10
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 10


def deficit_recovery_period():
    """
    Real Name: Deficit recovery period
    Original Eqn: 6
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 6


def indicated_tariff_change():
    """
    Real Name: Indicated Tariff Change
    Original Eqn: Budget Deficit/Utility Energy Sale/Deficit recovery period
    Units: Dollar/(Month*kWh)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return budget_deficit() / utility_energy_sale() / deficit_recovery_period()


def energy_procurement():
    """
    Real Name: Energy Procurement
    Original Eqn: Utility Energy Sale*(1+Electricity Loss/100)
    Units: kWh/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return utility_energy_sale() * (1 + electricity_loss() / 100)


def percent_std_effect_of_remaining_time():
    """
    Real Name: percent std effect of remaining time
    Original Eqn: 0.05
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.05


def std_of_effect_of_remaining_time():
    """
    Real Name: std of effect of remaining time
    Original Eqn: percent std effect of remaining time*Tariff Correction Period
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return percent_std_effect_of_remaining_time() * tariff_correction_period()


def effect_of_remaining_time_on_change_in_electricity_tariff():
    """
    Real Name: effect of remaining time on change in electricity tariff
    Original Eqn: 1/(std of effect of remaining time*2*pi)*EXP( -0.5*(tariff correction remaining time/std of effect of remaining time)^2 )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    1/(std of effect of remaining time*2*pi)*EXP( -0.5*(tariff correction
        remaining time/std of effect of remaining time)^2 )
    """
    return (
        1
        / (std_of_effect_of_remaining_time() * 2 * pi())
        * np.exp(
            -0.5
            * (tariff_correction_remaining_time() / std_of_effect_of_remaining_time())
            ** 2
        )
    )


def tariff_correction_remaining_time():
    """
    Real Name: tariff correction remaining time
    Original Eqn: MIN( MODULO( Time , Tariff Correction Period ), ABS(MODULO(Time, Tariff Correction Period)-Tariff Correction Period) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.minimum(
        modulo(time(), tariff_correction_period()),
        np.abs(modulo(time(), tariff_correction_period()) - tariff_correction_period()),
    )


def pi():
    """
    Real Name: pi
    Original Eqn: 3.14159
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 3.14159


def change_in_electricity_tariff():
    """
    Real Name: change in electricity tariff
    Original Eqn: Indicated Tariff Change*effect of remaining time on change in electricity tariff
    Units: Dollar/(kWh*Month)
    Limits: (None, None)
    Type: component
    Subs: None

    IF THEN ELSE( MODULO(Time, Tariff Correction Period )=0 , Limited Tariff
        Change , 0 )
    """
    return (
        indicated_tariff_change()
        * effect_of_remaining_time_on_change_in_electricity_tariff()
    )


def change_in_regular_consumer_demand():
    """
    Real Name: change in Regular Consumer Demand
    Original Eqn: Actual Regular Customer Demand change/time to adjust Regular Consumer demand
    Units: kWh/(Month*Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        actual_regular_customer_demand_change()
        / time_to_adjust_regular_consumer_demand()
    )


def change_in_prosumer_demand():
    """
    Real Name: change in Prosumer Demand
    Original Eqn: Actual Prosumer Demand Change/time to adjust Prosumer Demand
    Units: kWh/(Month*Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return actual_prosumer_demand_change() / time_to_adjust_prosumer_demand()


def change_in_indicated_prosumer_demand():
    """
    Real Name: change in indicated prosumer demand
    Original Eqn: IF THEN ELSE(Prosumer Average Demand+indicated change in Prosumer Demand>Maximum Average Prosumer Demand, Maximum Average Prosumer Demand-Prosumer Average Demand , IF THEN ELSE( Prosumer Average Demand+indicated change in Prosumer Demand<Minimum Average Prosumer Demand , Minimum Average Prosumer Demand-Prosumer Average Demand , indicated change in Prosumer Demand ) )
    Units: kWh/(Month*Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        prosumer_average_demand() + indicated_change_in_prosumer_demand()
        > maximum_average_prosumer_demand(),
        lambda: maximum_average_prosumer_demand() - prosumer_average_demand(),
        lambda: if_then_else(
            prosumer_average_demand() + indicated_change_in_prosumer_demand()
            < minimum_average_prosumer_demand(),
            lambda: minimum_average_prosumer_demand() - prosumer_average_demand(),
            lambda: indicated_change_in_prosumer_demand(),
        ),
    )


def average_daily_battery_eenergy():
    """
    Real Name: Average Daily Battery Eenergy
    Original Eqn: (Regular Consumer Average Demand/30)*Storage to Daily Load Factor
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (regular_consumer_average_demand() / 30) * storage_to_daily_load_factor()


def battery_cost_reduction():
    """
    Real Name: Battery Cost Reduction
    Original Eqn: effect of Customers on Battery Cost*effect of Minimum Battery Cost*Normal Battery Cost Reduction rate*Battery Cost
    Units: Dollar/(kWh*Month)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        effect_of_customers_on_battery_cost()
        * effect_of_minimum_battery_cost()
        * normal_battery_cost_reduction_rate()
        * battery_cost()
    )


def battery_life():
    """
    Real Name: Battery Life
    Original Eqn: 40
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 40


def effect_of_minimum_battery_cost():
    """
    Real Name: effect of Minimum Battery Cost
    Original Eqn: 1-1/(1+EXP(6-12*Minimum Battery Cost/Battery Cost))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - 1 / (1 + np.exp(6 - 12 * minimum_battery_cost() / battery_cost()))


def direct_defection_total_cost():
    """
    Real Name: Direct Defection Total Cost
    Original Eqn: Total Battery Cost+Total PV Cost
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_battery_cost() + total_pv_cost()


def direct_defector_monthly_savings():
    """
    Real Name: Direct Defector Monthly Savings
    Original Eqn: Electricity Tariff*Regular Consumer Average Demand
    Units: Dollar/(Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return electricity_tariff() * regular_consumer_average_demand()


def direct_defector_net_present_savings():
    """
    Real Name: Direct Defector Net Present Savings
    Original Eqn: Direct Defector Monthly Savings*(((1+Discount Rate)^(PV Life+1)-1)/Discount Rate)
    Units: Dollar/kWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return direct_defector_monthly_savings() * (
        ((1 + discount_rate()) ** (pv_life() + 1) - 1) / discount_rate()
    )


def discount_rate():
    """
    Real Name: Discount Rate
    Original Eqn: 0.001
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.001


def consumer_growth():
    """
    Real Name: Consumer Growth
    Original Eqn: population growth rate*Total Consumers
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return population_growth_rate() * total_consumers()


def defectors():
    """
    Real Name: Defectors
    Original Eqn: INTEG ( Direct Defection By Imitation+Direct Defection by Innovation+Installing Battery By Imitation+Installing Battery by Innovation+New Defectors, 0)
    Units: Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_defectors()


def effect_of_direct_defection_npv_on_imitation():
    """
    Real Name: effect of direct defection NPV on imitation
    Original Eqn: 0.5+2/(1+EXP(2-Direct Defection NPV/5000))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    0.5+2/(1+exp(2-x/5000))
    """
    return 0.5 + 2 / (1 + np.exp(2 - direct_defection_npv() / 5000))


def direct_defection_npv():
    """
    Real Name: Direct Defection NPV
    Original Eqn: Direct Defector Net Present Savings-Direct Defection Total Cost
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return direct_defector_net_present_savings() - direct_defection_total_cost()


def no_batteries():
    """
    Real Name: "No. Batteries"
    Original Eqn: INTEGER(Average Daily Battery Eenergy)+1
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return integer(average_daily_battery_eenergy()) + 1


def no_bettery_replacement():
    """
    Real Name: "No. Bettery Replacement"
    Original Eqn: IF THEN ELSE(MODULO(PV Life, Battery Life )=0, PV Life/Battery Life , INTEGER( PV Life/Battery Life )+1 )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        modulo(pv_life(), battery_life()) == 0,
        lambda: pv_life() / battery_life(),
        lambda: integer(pv_life() / battery_life()) + 1,
    )


def npv_pv_income():
    """
    Real Name: NPV PV Income
    Original Eqn: PV monthly Income*(((1+Discount Rate)^(PV Life+1)-1)/Discount Rate)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pv_monthly_income() * (
        ((1 + discount_rate()) ** (pv_life() + 1) - 1) / discount_rate()
    )


def total_pv_cost():
    """
    Real Name: Total PV Cost
    Original Eqn: "No. PVs"*PV Cost
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return no_pvs() * pv_cost()


def effect_of_direct_defection_npv_on_innovation():
    """
    Real Name: effect of direct defection NPV on innovation
    Original Eqn: 1+1.5/(1+EXP(2-Direct Defection NPV/2000))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 + 1.5 / (1 + np.exp(2 - direct_defection_npv() / 2000))


def effect_of_installing_battery_npv_on_imitation():
    """
    Real Name: effect of installing battery NPV on imitation
    Original Eqn: 0.5+2/(1+EXP(2-Installing Battery NPV/5000))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 0.5 + 2 / (1 + np.exp(2 - installing_battery_npv() / 5000))


def effect_of_installing_battery_npv_on_innovation():
    """
    Real Name: effect of installing battery NPV on innovation
    Original Eqn: 1+1.5/(1+EXP(2-Installing Battery NPV/2000))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 + 1.5 / (1 + np.exp(2 - installing_battery_npv() / 2000))


def indicated_change_in_prosumer_demand():
    """
    Real Name: indicated change in Prosumer Demand
    Original Eqn: IF THEN ELSE(Electricity Tariff=0, -price elasticity of prosumers*Prosumer Average Demand*30 ,change in electricity tariff*price elasticity of prosumers*Prosumer Average Demand/Electricity Tariff)
    Units: kWh/(Month*Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        electricity_tariff() == 0,
        lambda: -price_elasticity_of_prosumers() * prosumer_average_demand() * 30,
        lambda: change_in_electricity_tariff()
        * price_elasticity_of_prosumers()
        * prosumer_average_demand()
        / electricity_tariff(),
    )


def indicated_change_in_regular_consumer_demand():
    """
    Real Name: indicated change in regular Consumer Demand
    Original Eqn: IF THEN ELSE(Electricity Tariff=0, -price elasticity of regular consumers*Regular Consumer Average Demand*30, change in electricity tariff*Regular Consumer Average Demand*price elasticity of regular consumers/Electricity Tariff)
    Units: kWh/(Month*Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        electricity_tariff() == 0,
        lambda: -price_elasticity_of_regular_consumers()
        * regular_consumer_average_demand()
        * 30,
        lambda: change_in_electricity_tariff()
        * regular_consumer_average_demand()
        * price_elasticity_of_regular_consumers()
        / electricity_tariff(),
    )


def prosumers():
    """
    Real Name: Prosumers
    Original Eqn: INTEG ( installing PV by imitation+installing PV by Innovation+New Prosumers-Installing Battery By Imitation-Installing Battery by Innovation, 0)
    Units: Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_prosumers()


def total_customers_with_pv():
    """
    Real Name: Total Customers with PV
    Original Eqn: Defectors+Prosumers
    Units: Customer
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return defectors() + prosumers()


def installing_battery_npv():
    """
    Real Name: Installing Battery NPV
    Original Eqn: Direct Defection NPV-NPV PV
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return direct_defection_npv() - npv_pv()


def no_pvs():
    """
    Real Name: "No. PVs"
    Original Eqn: INTEGER(Regular Consumer Average Demand*(1+Reliablity Margin)/PV monthly Generation)+1
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        integer(
            regular_consumer_average_demand()
            * (1 + reliablity_margin())
            / pv_monthly_generation()
        )
        + 1
    )


def total_battery_cost():
    """
    Real Name: Total Battery Cost
    Original Eqn: Battery Cost*"No. Bettery Replacement"*"No. Batteries"
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return battery_cost() * no_bettery_replacement() * no_batteries()


def pv_monthly_income():
    """
    Real Name: PV monthly Income
    Original Eqn: Electricity Tariff*PV monthly Generation
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return electricity_tariff() * pv_monthly_generation()


def new_regular_consumers():
    """
    Real Name: New Regular Consumers
    Original Eqn: Consumer Growth*New Regular Consumer Ratio
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return consumer_growth() * new_regular_consumer_ratio()


def storage_to_daily_load_factor():
    """
    Real Name: Storage to Daily Load Factor
    Original Eqn: 0.5
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.5


def income():
    """
    Real Name: Income
    Original Eqn: Electricity Tariff*Utility Energy Sale
    Units: Dollar/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return electricity_tariff() * utility_energy_sale()


def reliablity_margin():
    """
    Real Name: Reliablity Margin
    Original Eqn: 0.5
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.5


def new_defectors():
    """
    Real Name: New Defectors
    Original Eqn: Consumer Growth*New Defector Ratio*(effect of direct defection NPV on imitation+effect of direct defection NPV on innovation)/2
    Units: Customer/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        consumer_growth()
        * new_defector_ratio()
        * (
            effect_of_direct_defection_npv_on_imitation()
            + effect_of_direct_defection_npv_on_innovation()
        )
        / 2
    )


def actual_regular_customer_demand_change():
    """
    Real Name: Actual Regular Customer Demand change
    Original Eqn: INTEG ( change in indicated regular consumer demand-change in Regular Consumer Demand, 0)
    Units: kWh/(Month*Customer)
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_actual_regular_customer_demand_change()


def actual_prosumer_demand_change():
    """
    Real Name: Actual Prosumer Demand Change
    Original Eqn: INTEG ( change in indicated prosumer demand-change in Prosumer Demand, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_actual_prosumer_demand_change()


def new_prosumer_ratio():
    """
    Real Name: New Prosumer Ratio
    Original Eqn: 0.08*effect of PV NPV
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 0.08 * effect_of_pv_npv()


def npv_pv_ratio():
    """
    Real Name: NPV PV Ratio
    Original Eqn: NPV PV/PV Cost
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return npv_pv() / pv_cost()


def effect_of_pv_npv():
    """
    Real Name: effect of PV NPV
    Original Eqn: 1+2/(1+EXP( -4*(NPV PV Ratio-2) ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 + 2 / (1 + np.exp(-4 * (npv_pv_ratio() - 2)))


def npv_pv():
    """
    Real Name: NPV PV
    Original Eqn: (NPV PV Income-PV Cost)*PV size
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (npv_pv_income() - pv_cost()) * pv_size()


def population_growth_rate():
    """
    Real Name: population growth rate
    Original Eqn: 0.01/12
    Units: 1/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.01 / 12


def new_defector_ratio():
    """
    Real Name: New Defector Ratio
    Original Eqn: 0.1
    Units: Dollar
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.1


def pv_life():
    """
    Real Name: PV Life
    Original Eqn: 240
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 240


def pv_monthly_generation():
    """
    Real Name: PV monthly Generation
    Original Eqn: 140
    Units: kWh/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 140


def pv_size():
    """
    Real Name: PV size
    Original Eqn: 5
    Units: kw
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 5


def normal_battery_cost_reduction_rate():
    """
    Real Name: Normal Battery Cost Reduction rate
    Original Eqn: 0.006
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.006


def minimum_battery_cost():
    """
    Real Name: Minimum Battery Cost
    Original Eqn: 100
    Units: Dollar/kw
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 100


def time_to_adjust_regular_consumer_demand():
    """
    Real Name: time to adjust Regular Consumer demand
    Original Eqn: 3
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 3


def time_to_adjust_prosumer_demand():
    """
    Real Name: time to adjust Prosumer Demand
    Original Eqn: 3
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 3


def prosumers_demand():
    """
    Real Name: Prosumers Demand
    Original Eqn: Prosumer Average Demand*Prosumers
    Units: kWh/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return prosumer_average_demand() * prosumers()


def tariff_correction_period():
    """
    Real Name: Tariff Correction Period
    Original Eqn: 12
    Units: Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 12


def price_elasticity_of_prosumers():
    """
    Real Name: price elasticity of prosumers
    Original Eqn: -0.2
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return -0.2


def price_elasticity_of_regular_consumers():
    """
    Real Name: price elasticity of regular consumers
    Original Eqn: -0.1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return -0.1


def desired_income():
    """
    Real Name: Desired Income
    Original Eqn: Total Costs*(1+Permited Profit)
    Units: Dollar/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_costs() * (1 + permited_profit())


def permited_profit():
    """
    Real Name: Permited Profit
    Original Eqn: 0.15
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.15


def effect_of_minimum_pv_cost():
    """
    Real Name: effect of Minimum PV Cost
    Original Eqn: 1-1/(1+EXP(6-12*Minimum PV Cost/PV Cost))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - 1 / (1 + np.exp(6 - 12 * minimum_pv_cost() / pv_cost()))


def pv_cost_reduction():
    """
    Real Name: PV Cost Reduction
    Original Eqn: effect of Customers on PV Cost*effect of Minimum PV Cost*Normal PV Cost Reduction rate*PV Cost
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        effect_of_customers_on_pv_cost()
        * effect_of_minimum_pv_cost()
        * normal_pv_cost_reduction_rate()
        * pv_cost()
    )


def immitation_factor():
    """
    Real Name: Immitation Factor
    Original Eqn: 0.02/12
    Units: 1/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.02 / 12


def fixed_costs():
    """
    Real Name: Fixed Costs
    Original Eqn: 1.4e+08
    Units: Dollar/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1.4e08


def generation_price():
    """
    Real Name: Generation Price
    Original Eqn: 0.06
    Units: Dollar/kWh
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.06


def total_costs():
    """
    Real Name: Total Costs
    Original Eqn: Fixed Costs+Variable Costs
    Units: Dollar/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fixed_costs() + variable_costs()


def variable_costs():
    """
    Real Name: Variable Costs
    Original Eqn: Energy Procurement*Generation Price
    Units: Dollar/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return energy_procurement() * generation_price()


def normal_pv_cost_reduction_rate():
    """
    Real Name: Normal PV Cost Reduction rate
    Original Eqn: 0.01
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.01


def minimum_pv_cost():
    """
    Real Name: Minimum PV Cost
    Original Eqn: 100
    Units: Dollar/kw
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 100


def monthly_income_shortfall():
    """
    Real Name: Monthly Income Shortfall
    Original Eqn: Desired Income-Income
    Units: Dollar/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return desired_income() - income()


def regular_consumers_demand():
    """
    Real Name: Regular Consumers Demand
    Original Eqn: Regular Consumer Average Demand*Regular Consumers
    Units: kWh/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return regular_consumer_average_demand() * regular_consumers()


def utility_energy_sale():
    """
    Real Name: Utility Energy Sale
    Original Eqn: Prosumers Demand+Regular Consumers Demand
    Units: kWh/Month
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return prosumers_demand() + regular_consumers_demand()


def innovation_factor():
    """
    Real Name: Innovation factor
    Original Eqn: 0.01/12
    Units: 1/Month
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0.01 / 12


_integ_total_consumers = Integ(
    lambda: consumer_growth(),
    lambda: initial_number_of_consumers(),
    "_integ_total_consumers",
)


_integ_regular_consumers = Integ(
    lambda: new_regular_consumers()
    - direct_defection_by_imitation()
    - direct_defection_by_innovation()
    - installing_pv_by_imitation()
    - installing_pv_by_innovation(),
    lambda: initial_number_of_consumers(),
    "_integ_regular_consumers",
)


_integ_pv_cost = Integ(
    lambda: -pv_cost_reduction(), lambda: initial_pv_cost(), "_integ_pv_cost"
)


_integ_electricity_tariff = Integ(
    lambda: change_in_electricity_tariff(),
    lambda: initial_electricity_tariff(),
    "_integ_electricity_tariff",
)


_integ_battery_cost = Integ(
    lambda: -battery_cost_reduction(),
    lambda: initial_battery_cost(),
    "_integ_battery_cost",
)


_integ_budget_deficit = Integ(
    lambda: monthly_income_shortfall(),
    lambda: initial_budget_deficit(),
    "_integ_budget_deficit",
)


_integ_regular_consumer_average_demand = Integ(
    lambda: change_in_regular_consumer_demand(),
    lambda: initial_average_consumer_demand(),
    "_integ_regular_consumer_average_demand",
)


_integ_prosumer_average_demand = Integ(
    lambda: change_in_prosumer_demand(),
    lambda: initial_prosumer_demand(),
    "_integ_prosumer_average_demand",
)


_integ_defectors = Integ(
    lambda: direct_defection_by_imitation()
    + direct_defection_by_innovation()
    + installing_battery_by_imitation()
    + installing_battery_by_innovation()
    + new_defectors(),
    lambda: 0,
    "_integ_defectors",
)


_integ_prosumers = Integ(
    lambda: installing_pv_by_imitation()
    + installing_pv_by_innovation()
    + new_prosumers()
    - installing_battery_by_imitation()
    - installing_battery_by_innovation(),
    lambda: 0,
    "_integ_prosumers",
)


_integ_actual_regular_customer_demand_change = Integ(
    lambda: change_in_indicated_regular_consumer_demand()
    - change_in_regular_consumer_demand(),
    lambda: 0,
    "_integ_actual_regular_customer_demand_change",
)


_integ_actual_prosumer_demand_change = Integ(
    lambda: change_in_indicated_prosumer_demand() - change_in_prosumer_demand(),
    lambda: 0,
    "_integ_actual_prosumer_demand_change",
)
