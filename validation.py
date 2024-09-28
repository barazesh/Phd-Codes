# %%
import pandas as pd
import plotly.express as px
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler


# %%
def ConfigureMatplotlib():
    mpl.rc("lines", linewidth=1.5, markersize=4)
    mpl.rc("grid", linewidth=0.5, linestyle="--")
    plt.rcParams["axes.grid"] = True
    mpl.rc("font", size=7, family="Times New Roman")
    cm = 1 / 2.54
    mpl.rc("figure", figsize=(16 * cm, 10 * cm))
    custom_cycler = cycler(marker=[None, "*", "d", "o", "x"]) + cycler(
        color=[str(i) for i in np.linspace(0.2, 0.6, 5)]
    )
    mpl.rc("axes", prop_cycle=custom_cycler)


# %%
PV_projects = pd.read_csv(
    "C:/Users/baraz/Documents/Phd-Codes/Data/nem-capacity-chart.csv",
    index_col=0,
    parse_dates=True,
    usecols=["DateTime", "Prior Months' Cumulative Projects"],
).rename(columns={"Prior Months' Cumulative Projects": "Total Projects"})

# %%
output = pd.read_csv(
    "C:/Users/baraz/Documents/Phd-Codes/Outputs/baseCaseResults.csv", index_col=0
)
output.index = pd.date_range(
    start="2010-01-01", end="2040-02-01", inclusive="both", freq="1M"
)

# %%
PV_No_comparison = pd.DataFrame(
    index=pd.date_range(
        start="2010-01-01", end="2023-01-01", inclusive="left", freq="1M"
    ),
    data={
        "simulated": output.loc[output.index.year < 2023, ["Prosumers", "Defectors"]]
        .sum(1)
        .values,
        "actual": PV_projects.loc[
            (PV_projects.index.year >= 2010) & (PV_projects.index.year < 2023),
            "Total Projects",
        ].tolist(),
    },
)
PV_No_comparison['error']=100*(PV_No_comparison['actual']-PV_No_comparison['simulated'])/PV_No_comparison['actual']
px.line(PV_No_comparison)
# %%
# pv_owner['error']=100*(pv_owner['actual']-pv_owner['simulated']).abs()/pv_owner['actual']
# %%
ConfigureMatplotlib()
# %%
fig, ax1 = plt.subplots()  # Create a figure and axis

# Plot actual and simulated data on the primary y-axis
line1, = ax1.plot(PV_No_comparison.index, PV_No_comparison['actual'], label='Actual Data')
line2, = ax1.plot(PV_No_comparison.index, PV_No_comparison['simulated'], label='Simulated Data')

# Set the primary axis labels
ax1.set_xlabel("Date")
ax1.set_ylabel("Consumers")
ax1.tick_params(axis='y')

# Enable grid on the primary y-axis
ax1.grid(True)

# Create a secondary y-axis for the absolute error
ax2 = ax1.twinx()

# Plot absolute error on the secondary y-axis
line3, = ax2.plot(PV_No_comparison.index, PV_No_comparison['error'], label='Error (%)', linestyle='--')

# Set the secondary y-axis label
ax2.set_ylabel('Error (%)')
ax2.tick_params(axis='y')

# Set the error axis to range from 0 to 100 (since it's absolute)
ax2.set_ylim(-100, 100)

# Set the title
plt.title("Actual vs. Simulated number of PV owners during validation period")

# Combine legends from both axes
lines = [line1, line2, line3]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper left')

# Save the plot
plt.savefig(
    "C:/Users/baraz/Documents/Phd-Codes/Outputs/Validation_PV_consumers.pdf",
    bbox_inches="tight"
)

plt.clf()  # Clear the figure for further use

# %%
residential_tariff = pd.read_csv(
    "C:/Users/baraz/Documents/Phd-Codes/Data/SCE_financial.csv",
    index_col=0,
    usecols=["year", "residential_tariff"],
)
# %%

tariff_comparison = pd.DataFrame(
    output.groupby(output.index.year).mean()["Tariff_var"]
).rename(columns={"Tariff_var": "simulated"})
for y in tariff_comparison.index:
    if y in residential_tariff.index:
        tariff_comparison.loc[y, "actual"] = residential_tariff.loc[
            y, "residential_tariff"
        ]
tariff_comparison=tariff_comparison[tariff_comparison.index < 2023]
tariff_comparison['error']=100*(tariff_comparison['actual']-tariff_comparison['simulated'])/tariff_comparison['actual']
#%%
fig, ax1 = plt.subplots()  # Create a figure and axis

# Plot actual and simulated data on the primary y-axis
line1, = ax1.plot(tariff_comparison.index, tariff_comparison['actual'], label='Actual Data')
line2, = ax1.plot(tariff_comparison.index, tariff_comparison['simulated'], label='Simulated Data')

# Set the primary axis labels
ax1.set_xlabel("Date")
ax1.set_ylabel("Dollar/kWh")
ax1.tick_params(axis='y')
ax1.set_ylim(0, 0.25)

# Enable grid on the primary y-axis
ax1.grid(True)

# Create a secondary y-axis for the absolute error
ax2 = ax1.twinx()

# Plot absolute error on the secondary y-axis
line3, = ax2.plot(tariff_comparison.index, tariff_comparison['error'], label='Error (%)', linestyle='--')

# Set the secondary y-axis label
ax2.set_ylabel('Error (%)')
ax2.tick_params(axis='y')

# Set the error axis to range from 0 to 100 (since it's absolute)
ax2.set_ylim(-100, 100)

# Set the title
plt.title("Actual vs. Simulated residential electricity tariff during validation period")

# Combine legends from both axes
lines = [line1, line2, line3]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper left')



plt.savefig(
    f"C:/Users/baraz/Documents/Phd-Codes/Outputs/Validation_tariff.pdf",
    bbox_inches="tight",
)
plt.clf()


# %%
residential_sale = pd.read_csv(
    "C:/Users/baraz/Documents/Phd-Codes/Data/SCE_financial.csv",
    index_col=0,
    usecols=["year", "residential_sale"],
)
residential_sale_comparison = pd.DataFrame(
    output.groupby(output.index.year).sum()["Utility_Sales"]*1e-6
).rename(columns={"Utility_Sales": "simulated"})


for y in residential_sale_comparison.index:
    if y in residential_tariff.index:
        residential_sale_comparison.loc[y, "actual"] = residential_sale.loc[
            y, "residential_sale"
        ]


residential_sale_comparison=residential_sale_comparison[residential_sale_comparison.index < 2023]
residential_sale_comparison['error']=100*(residential_sale_comparison['actual']-residential_sale_comparison['simulated'])/residential_sale_comparison['actual']
#%%
fig, ax1 = plt.subplots()  # Create a figure and axis

# Plot actual and simulated data on the primary y-axis
line1, = ax1.plot(residential_sale_comparison.index, residential_sale_comparison['actual'], label='Actual Data')
line2, = ax1.plot(residential_sale_comparison.index, residential_sale_comparison['simulated'], label='Simulated Data')

# Set the primary axis labels
ax1.set_xlabel("Date")
ax1.set_ylabel("GWh")
ax1.tick_params(axis='y')
ax1.set_ylim(0, 35000)

# Enable grid on the primary y-axis
ax1.grid(True)

# Create a secondary y-axis for the absolute error
ax2 = ax1.twinx()

# Plot absolute error on the secondary y-axis
line3, = ax2.plot(residential_sale_comparison.index, residential_sale_comparison['error'], label='Error (%)', linestyle='--')

# Set the secondary y-axis label
ax2.set_ylabel('Error (%)')
ax2.tick_params(axis='y')

# Set the error axis to range from 0 to 100 (since it's absolute)
ax2.set_ylim(-100, 100)

# Set the title
plt.title("Actual vs. Simulated residential electricity tariff during validation period")

# Combine legends from both axes
lines = [line1, line2, line3]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='lower left')        

plt.savefig(
    f"C:/Users/baraz/Documents/Phd-Codes/Outputs/Validation_sale.pdf",
    bbox_inches="tight",
)
plt.clf()
