from prediction import predict

import pandas as pd
from tqdm import tqdm

from scraping.scrape import news_scrape_general

from db.getEntities import toDatabase as toEntitiesTable
from db.getEntityScores import toDatabase as toEntityScoresTable
from db.mapping import initiate_mapping as toArticleEntityMappingTable

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(subset=["title"], inplace=True)
    df["excerpt"].fillna("", inplace=True)
    df["text"] = df["title"] + " " + df["excerpt"]
    return df

# Warning: Current code will lead to undesired behavior if re-run on the same set of articles
# Need to implement a check to not reinsert duplicate articles for this to not happen

# Code doesn't throw error, but correctness has not been checked. 
def main():
    df = news_scrape_general()
    df = preprocess_df(df)
    docs = df["text"].tolist()

    output = predict(docs)
    df["risk"] = output["risk"]
    df["ner_output"] = output["ner"]

    # ? Might want to save this df somewhere to retrain
    no_ent_df = df[df["ner_output"].apply(len) == 0]
    df = df[df["ner_output"].apply(len) > 0]

    exploded_df = df.explode("ner_output")
    exploded_df["entity_name"] = exploded_df["ner_output"].apply(lambda x: x["name"])

    toEntitiesTable(exploded_df, database='/home/ubuntu/ML_cylynx_nlp/sqlite_test.db')
    toEntityScoresTable(exploded_df, database='/home/ubuntu/ML_cylynx_nlp/sqlite_test.db')

    toArticleEntityMappingTable(df, 1, database='/home/ubuntu/ML_cylynx_nlp/sqlite_test.db')
    toArticleEntityMappingTable(no_ent_df, 0, database='/home/ubuntu/ML_cylynx_nlp/sqlite_test.db')

if __name__ == "__main__":
    main()
