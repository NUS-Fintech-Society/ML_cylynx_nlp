import streamlit as st
from prediction import predict

import pandas as pd
import json
from tqdm import tqdm

df = pd.read_csv("data/data.csv")
df["text"] = df["title"] + " " + df["excerpt"].fillna("")

out_df = pd.DataFrame()
original_cols = df.columns

for i in tqdm(range(len(df)//500)):
    new_df = df[i*500:(i+1)*500].copy()

    text = new_df["text"].tolist()
    output = predict(text)


    new_df["ner"] = output["ner"]
    new_df["risk"] = output["risk"]
    new_df.dropna("ner",inplace =True)
    new_df = new_df.explode("ner")
    new_df["entity_name"],new_df["confidence"] = \
        new_df["ner"].apply(lambda x:x["name"], x["confidecne"])
    new_df.to_csv(f"output/output_{i}.csv",index=False)
