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
    # df['confidence'] = df['ner_output'].apply(lambda x: x['confidence']) TODO: Delete this

    df.to_csv('/home/ubuntu/ML_cylynx_nlp/output/original_output.csv', index=False)
    # # df = pd.read_csv('/home/ubuntu/ML_cylynx_nlp/output/original_output.csv', header=0)  # TODO: There's some problem if we read from csv
    print(df.head())

    # toArticleEntityMappingTable(df, 1, database='/home/ubuntu/ML_cylynx_nlp/db/sqlite2.db')
    # toArticleEntityMappingTable(no_ent_df, 0, database='sqlite2.db')

    df = df.explode("ner_output")
    df["entity_name"] = df["ner_output"].apply(lambda x: x["name"])

    # toEntitiesTable(df, database='/home/ubuntu/ML_cylynx_nlp/db/sqlite2.db')      # Upload df to entites table
    print(df.head())
    toEntityScoresTable(df, database='/home/ubuntu/ML_cylynx_nlp/db/sqlite2.db')  # Upload df to entity_scores table

if __name__ == "__main__":
    main()
