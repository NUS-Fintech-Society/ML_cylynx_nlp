import pandas as pd

def jaccard_matrix():
    pass

def clean_df(df):
    df.dropna("title",inplace = True)
    df["excerpt"] = df["excerpt"].fillna("")

    pass
