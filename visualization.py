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
markerinterval=12*2**4
custom_cycler=(cycler(marker=[None,'*','d','o','x'])+cycler(color=[str(i) for i in np.linspace(0.2,0.6,5)]))
mpl.rc('axes',prop_cycle=custom_cycler)
#%%
data = pd.read_csv("./Outputs/baseCaseResults.csv", index_col=0)


#%%

plt.plot(data['Tariff'])
plt.title(f'Electricity Tariff')
plt.xlim([0, 240])
plt.xticks([r for r in range(0,241,24)])
plt.xlabel('Time (Month)')
plt.ylabel('Dollar/kWh') 
plt.savefig('.Outputs/base_tariff.pdf', bbox_inches='tight')


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




