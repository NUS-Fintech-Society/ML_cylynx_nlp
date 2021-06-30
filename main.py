from prediction import predict

import pandas as pd
from tqdm import tqdm

from scraping.scrape import news_scrape_general

from db.getEntities import toDatabase as toEntitiesTable
from db.getEntityScores import toDatabase as toEntityScoresTable
from db.mapping import initiate_mapping as toArticleEntityMappingTable

from db.articles import getArticlesFromIds
from db.mapping import getMappingFromArticleIds
from db.getEntities import getEntityIdsNames, getValidEntityIdsNames

from neo4j_db import create_articles, create_entities, match_article_entity
import IPython

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

    article_ids = toArticleEntityMappingTable(df, 1, database='/home/ubuntu/ML_cylynx_nlp/sqlite_test.db')
    toArticleEntityMappingTable(no_ent_df, 0, database='/home/ubuntu/ML_cylynx_nlp/sqlite_test.db')
    article_ids = [i for i in article_ids if i != None]
    
    # Scripts for Neo4J components
    article_df = getArticlesFromIds(article_ids, "./sqlite_test.db")
    mapping_df = getMappingFromArticleIds(article_ids, "./sqlite_test.db")
    entity_ids = mapping_df["entity_id"].tolist()
    
    entity_ids_from_run = list(set(entity_ids))
    valid_entity_df = getValidEntityIdsNames("./sqlite_test.db")
    valid_ids = valid_entity_df["entity_id"].tolist()

    valid_ids = [idx for idx in valid_ids if idx in entity_ids_from_run]

    entity_df = getEntityIdsNames(valid_ids,"./sqlite_test.db")
    # This is a merge operation so if the entity is present, it will not do anything

    create_entities(entity_df)
    create_articles(article_df)
    match_article_entity(mapping_df)

if __name__ == "__main__":
    main()
