import pandas as pd
import json
import pickle

df = pickle.load(open('full_dataset.p', 'rb'))

data_dict = {}
fatigue = list(df["Coffee Consumption"])
data_dict["Coffee Consumption"] = fatigue

Designation = list(df["Positive/Tested %"])
data_dict["Positive/Tested %"] = Designation

burn = list(df["Score"])
data_dict["Score"] = burn

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)