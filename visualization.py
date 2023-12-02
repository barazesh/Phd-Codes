#%%
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

# import openpyxl as xl
import numpy as np
import plotly.express as px
#%%

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


def PlotSensitivity(parameter: str):
    ConfigureMatplotlib()
    markerinterval = 12
    dataPath = f"./Outputs/sensitivity_{parameter}.xlsx"
    data = pd.read_excel(dataPath, sheet_name="Tariff_var", index_col=0)
    data.plot(markevery=markerinterval)
    plt.title(f"Electricity Tariff (Volumetric)")
    plt.legend(loc="upper left")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Dollar/kWh")
    plt.savefig(f"./Outputs/{parameter}_tariff_var.pdf", bbox_inches="tight")
    plt.clf()
 
    data = pd.read_excel(dataPath, sheet_name="Tariff_fix", index_col=0)
    data.plot(markevery=markerinterval)
    plt.title(f"Fixed Electricity Tariff")
    plt.legend(loc="upper left")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Dollar/Month")
    plt.savefig(f"./Outputs/{parameter}_tariff_fix.pdf", bbox_inches="tight")
    plt.clf()

    data = pd.read_excel(dataPath, sheet_name="Utility_Deficit", index_col=0)
    data.plot(markevery=markerinterval)
    plt.title("Total Utility Budget Deficit")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Dollar")
    plt.savefig(f"./Outputs/{parameter}_deficit.pdf", bbox_inches="tight")
    plt.clf()

    data = 100 * pd.read_excel(
        dataPath, sheet_name="Utility_Deficit_Fraction", index_col=0
    )
    data.plot(markevery=markerinterval)
    plt.title("Utility Budget Deficit as a fraction of monthly revenue")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("%")
    plt.savefig(f"./Outputs/{parameter}_deficit_fraction.pdf", bbox_inches="tight")
    plt.clf()

    data = pd.read_excel(dataPath, sheet_name="Utility_Sales", index_col=0)
    data_agg = data.rolling(12, step=12).sum()
    data_agg.loc[0, :] = data.loc[0, :] * 12
    data_agg.plot()
    plt.title("Total Utility Energy Sale")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("kWh")
    plt.savefig(f"./Outputs/{parameter}_sale.pdf", bbox_inches="tight")
    plt.clf()

    for c in ["Regular_Consumers", "Prosumers", "Defectors"]:
        data = pd.read_excel(dataPath, sheet_name=c, index_col=0)
        data.plot(markevery=markerinterval)
        plt.title(f"Number of {c}")
        plt.xlim([0, 360])
        plt.xticks([r for r in range(0, 361, 24)])
        plt.xlabel("Time (Month)")
        plt.ylabel("Consumers")
        plt.savefig(f"./Outputs/{parameter}_{c}.pdf", bbox_inches="tight")
        plt.clf()

    for c in ["Regular2ProsumerIRR","Regular2DefectorIRR","Prosumer2DefectorIRR"]:
        data = pd.read_excel(dataPath, sheet_name=c, index_col=0)
        data.plot(markevery=markerinterval)
        temp=c[:-3].split('2')
        plt.title(f"Internal Rate of Return for the transition from {temp[0]} to {temp[1]}")
        plt.xlim([0, 360])
        plt.xticks([r for r in range(0, 361, 24)])
        plt.xlabel("Time (Month)")
        plt.ylabel("%")
        plt.savefig(f"./Outputs/{parameter}_{c}.pdf", bbox_inches="tight")
        plt.clf()


def PlotBaseCase():
    data = pd.read_csv("./Outputs/baseCaseResults.csv", index_col=0)
    ConfigureMatplotlib()
    markerinterval = 12

    plt.plot(data["Tariff_var"])
    plt.title("Electricity Tariff - Variable part")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Dollar/kWh")
    plt.savefig("./Outputs/base_tariff_var.pdf", bbox_inches="tight")
    plt.clf()

    plt.plot(data["Tariff_fix"])
    plt.title("Electricity Tariff - fixed part")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Dollar/Month")
    plt.savefig("./Outputs/base_tariff_fix.pdf", bbox_inches="tight")
    plt.clf()

    (
        100
        * data[["Regular_Consumers", "Prosumers", "Defectors"]].divide(
            data["Total_Housholds"], axis=0
        )
    ).plot(markevery=markerinterval)
    plt.title("Fraction of consumers adopting each concept")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.legend(loc="center")
    plt.xlabel("Time (Month)")
    plt.ylabel("%")
    plt.savefig("./Outputs/base_Customers.pdf", bbox_inches="tight")
    plt.clf()

    # plt.plot(data[['Regular_Consumers','Prosumers','Defectors']],markevery=markerinterval)
    data[["Regular_Consumers", "Prosumers", "Defectors"]].plot(markevery=markerinterval)
    plt.title("Total number of consumers adopting each concept")
    plt.xlim([0, 360])
    plt.legend(loc="center")
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Consumers")
    plt.savefig("./Outputs/base_CustomersNo.pdf", bbox_inches="tight")
    plt.clf()

    data[["Regular2ProsumerIRR","Regular2DefectorIRR","Prosumer2DefectorIRR"]].plot(markevery=markerinterval)
    plt.title("Internal Rate of Return for each transition")
    plt.xlim([0, 360])
    plt.legend(loc="center")
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("%")
    plt.savefig("./Outputs/base_IRR.pdf", bbox_inches="tight")
    plt.clf()

    plt.plot(data.rolling(12, on="Utility_Sales", step=12)["Utility_Sales"].sum())
    plt.title("Total Utility Energy Sale")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("kWh")
    plt.savefig("./Outputs/base_sale.pdf", bbox_inches="tight")
    plt.clf()

    plt.plot(data["Utility_Deficit"])
    plt.title("Total Utility Budget Deficit")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("Dollar")
    plt.savefig("./Outputs/base_deficit.pdf", bbox_inches="tight")
    plt.clf()

    plt.plot(100 * data["Utility_Deficit_Fraction"])
    plt.title("Utility Budget Deficit as a fraction of Sales")
    plt.xlim([0, 360])
    plt.xticks([r for r in range(0, 361, 24)])
    plt.xlabel("Time (Month)")
    plt.ylabel("%")
    plt.savefig("./Outputs/base_deficit_fraction.pdf", bbox_inches="tight")
    plt.clf()

#%%
# parameter="fixed2VariableRatio"
# dataPath = f"C:/Users/baraz/Documents/Phd-Codes/Outputs/sensitivity_{parameter}.xlsx"
# data_file=pd.ExcelFile(dataPath)
#%%
# results={}
# for sheet in data_file.sheet_names:
#     results[sheet]= pd.read_excel(data_file, sheet_name=sheet, index_col=0)
#     print(sheet)

# #%%
# px.line(results['Prosumers_Demand_Change'])
# # %%
# parameter="fixed2VariableRatio"
# dataPath = f"C:/Users/baraz/Documents/Phd-Codes/Outputs/sensitivity_{parameter}_0elas.xlsx"
# data_file=pd.ExcelFile(dataPath)
# #%%
# results={}
# for sheet in data_file.sheet_names:
#     results[sheet]= pd.read_excel(data_file, sheet_name=sheet, index_col=0)

# #%%
# px.line(results['Utility_Sales'])
# # %%
