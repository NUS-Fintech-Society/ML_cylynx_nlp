from prediction import predict

import pandas as pd
import json
from tqdm import tqdm

from scraping.scrape import news_scrape_general

from db.getEntities import toDatabase as toEntitiesTable
from db.getEntityScores import toDatabase as toEntityScoresTable

def preprocess_df(df:pd.DataFrame)->pd.DataFrame:
    df.dropna(subset = ["title"],inplace = True)
    df["excerpt"].fillna("",inplace = True)
    df["text"]  = df["title"] + " " + df["excerpt"]
    return df

def main():
    df = news_scrape_general()
    df = preprocess_df(df)
    docs = df["text"].tolist()
    
    output = predict(docs)
    df["risk"] = output["risk"]
    
    df["ner_output"] = output["ner"]
    # ? Might want to save this df somewhere to retrain  
    #TODO: Call Article Function
    no_ent_df = df[df["ner_output"].apply(len)==0]
    
    
    df = df[df["ner_output"].apply(len)>0] 
    
    df = df.explode("ner_output")
    df["entity_name"] = df["ner_output"].apply(lambda x:x["name"])
    df["confidence"] = df["ner_output"].apply(lambda x:x["confidence"])
    
    
    toEntitiesTable(df) #Upload df to entites table
    toEntityScoresTable(df) # Upload df to entity_scores table


if __name__ == "__main__":
    main()
