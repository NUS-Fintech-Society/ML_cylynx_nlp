import streamlit as st
from prediction import predict

import pandas as pd
import json
from tqdm import tqdm

df = pd.read_csv("data/data.csv")
df["text"] = df["title"] + " " + df["excerpt"].fillna("")
inp = df["text"].tolist()
output = []

for i in tqdm(range(len(inp)//64)):
    in_slice = inp[i*64:(i+1)*64]
    out = predict(in_slice)
    output.extend(out)
with open("output.jsonl","w+",encoding="utf-8") as f:
    json.dump(output,f)