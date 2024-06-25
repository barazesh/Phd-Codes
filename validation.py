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
px.line(PV_No_comparison)
# %%
# pv_owner['error']=100*(pv_owner['actual']-pv_owner['simulated']).abs()/pv_owner['actual']
# %%
ConfigureMatplotlib()
# %%
PV_No_comparison.plot()
plt.title(rf"Actual vs. Simulated number of PV owners during validation period")
plt.xlabel("date")
plt.ylabel("Consumers")
plt.savefig(
    f"C:/Users/baraz/Documents/Phd-Codes/Outputs/Validation_PV_consumers.pdf",
    bbox_inches="tight",
)
plt.clf()

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

# tariff_output.groupby(tariff_output.index.year).mean()
# %%
tariff_comparison[tariff_comparison.index < 2023].plot()
plt.title(
    rf"Actual vs. Simulated residential electricity tariff during validation period"
)
plt.xlabel("date")
plt.ylabel("Dollar/kWh")
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
# %%
residential_sale_comparison[residential_sale_comparison.index < 2023].plot()
plt.title(
    rf"Actual vs. Simulated residential electricity sales during validation period"
)
plt.xlabel("date")
plt.ylabel("GWh")
plt.savefig(
    f"C:/Users/baraz/Documents/Phd-Codes/Outputs/Validation_sale.pdf",
    bbox_inches="tight",
)
plt.clf()
