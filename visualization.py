# %%
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import numpy as np

# %%
mpl.rc('lines',linewidth=1.5,markersize=4)  
mpl.rc('grid',linewidth=0.5,linestyle='--')
plt.rcParams["axes.grid"] = True
mpl.rc('font',size=7,family='Times New Roman')
cm = 1/2.54
mpl.rc('figure',figsize=(16*cm,10*cm))
markerinterval=12
custom_cycler=(cycler(marker=[None,'*','d','o','x'])+cycler(color=[str(i) for i in np.linspace(0.2,0.6,5)]))
mpl.rc('axes',prop_cycle=custom_cycler)

#%%#

import openpyxl as xl
wb = xl.load_workbook("./Outputs/sensitivity_period.xlsx")
print(wb.sheetnames)
#%%

data= pd.read_excel("./Outputs/sensitivity_period.xlsx", sheet_name='Tariff',index_col=0)
data.plot(markevery=markerinterval)
plt.title(f'Electricity Tariff')
plt.legend(loc='upper left')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar/kWh') 
plt.savefig('./Outputs/period_tariff.pdf', bbox_inches='tight')


#%%

data= pd.read_excel("./Outputs/sensitivity_period.xlsx", sheet_name='Utility_Deficit',index_col=0)
data.plot(markevery=markerinterval)
plt.title('Total Utility Budget Deficit')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar')
plt.savefig('./Outputs/period_deficit.pdf', bbox_inches='tight')


#%%
data= 100*pd.read_excel("./Outputs/sensitivity_period.xlsx", sheet_name='Utility_Deficit_Fraction',index_col=0)
data.plot(markevery=markerinterval)
plt.title('Utility Budget Deficit as a fraction of Sales')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('%')
plt.savefig('./Outputs/period_deficit_fraction.pdf', bbox_inches='tight')

#%%
data= pd.read_excel("./Outputs/sensitivity_period.xlsx", sheet_name='Utility_Sales',index_col=0)
data_agg=data.rolling(12,step=12).sum()
data_agg.loc[0]=data.loc[0]*12
data_agg.plot()
plt.title('Total Utility Energy Sale')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar')
plt.savefig('./Outputs/period_sale.pdf', bbox_inches='tight')

#%%
data = pd.read_csv("./Outputs/baseCaseResults.csv", index_col=0)


plt.plot(data['Tariff'])
plt.title(f'Electricity Tariff')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar/kWh') 
plt.savefig('./Outputs/base_tariff.pdf', bbox_inches='tight')


(100*data[['Regular_Consumers','Prosumers','Defectors']].divide(data['Total_Housholds'],axis=0)).plot(markevery=markerinterval)
plt.title('Fraction of consumers adopting each concept')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.legend(loc='center')
plt.xlabel('Time (Month)')
plt.ylabel('%')
plt.savefig('./Outputs/base_Customers.pdf', bbox_inches='tight')
plt.clf()

# plt.plot(data[['Regular_Consumers','Prosumers','Defectors']],markevery=markerinterval)
data[['Regular_Consumers','Prosumers','Defectors']].plot(markevery=markerinterval)
plt.title('Total number of consumers adopting each concept')
plt.xlim([0, 240])
plt.legend(loc='center')
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Consumers')
plt.savefig('./Outputs/base_CustomersNo.pdf', bbox_inches='tight')
plt.clf()

plt.plot(data.rolling(12,on='Utility_Sales',step=12)['Utility_Sales'].sum())
plt.title('Total Utility Energy Sale')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar')
plt.savefig('./Outputs/base_sale.pdf', bbox_inches='tight')
plt.clf()

plt.plot(data['Utility_Deficit'])
plt.title('Total Utility Budget Deficit')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar')
plt.savefig('./Outputs/base_deficit.pdf', bbox_inches='tight')
plt.clf()

plt.plot(100*data['Utility_Deficit_Fraction'])
plt.title('Utility Budget Deficit as a fraction of Sales')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('%')
plt.savefig('./Outputs/base_deficit_fraction.pdf', bbox_inches='tight')
plt.clf()

#%%
for c in data.columns:
    plt.plot(data[c])
    plt.title(c)
    plt.xlim([0, 240])
    plt.xticks([r for r in range(0,241,12)])
    plt.xlabel('Time (Month)')
    plt.ylabel('Dollar/kWh') 
    # plt.savefig(f"./{c.replace(' ','_')}.pdf", bbox_inches='tight')
    plt.clf()




