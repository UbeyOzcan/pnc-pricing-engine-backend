from src.DataFactory import DataFactory
import json
import numpy as np

DF = DataFactory()

df = DF.getData()

cols = df.columns.to_list()
cols = [x for x in cols if x not in ['IDpol', 'Exposure', 'ClaimNb', 'ClaimAmount']]
df = df[cols]
unique = {}
for i in cols:
    unique[i] = list(df[i].unique())

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

with open('unique.json', 'w') as f:
    json.dump(unique, f, cls=NpEncoder)