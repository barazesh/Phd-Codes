import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from pathlib import Path


sectors = ["all", "residential", "commercial",
           "industrial", "transportation", "other"]
data_path = Path('./Data')

data = {}
for f in data_path.glob('*.csv'):
    temp_total = pd.read_csv(str(f))
    states_length = temp_total.shape[0]
    data[f.stem]={}
    for sec in sectors:
        begin = sectors.index(sec)+2
        x = range(begin, states_length, 7)
        temp = temp_total.iloc[x]
        states = [i[0].strip() for i in temp["description"].str.split(":")]
        temp.loc[:,"state"] = states
        temp.drop(axis=1, columns=temp.columns[range(0, 3)], inplace=True)
        temp.set_index("state", inplace=True)
        for c in temp.columns:
            temp.loc[:,c] = pd.to_numeric(temp.loc[:,c], errors="coerce")
        data[f.stem][sec] = temp.transpose()

print(data[list(data)[1]]['all'])
