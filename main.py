from cryptonews.prediction import predict

import pandas as pd
from tqdm import tqdm

from cryptonews.scraping.scrape import news_scrape_general
from cryptonews.db.getEntities import toDatabase as toEntitiesTable
from cryptonews.db.getEntityScores import toDatabase as toEntityScoresTable
from cryptonews.db.mapping import initiate_mapping as toArticleEntityMappingTable

from cryptonews.db.articles import getArticlesFromIds
from cryptonews.db.mapping import getMappingFromArticleIds
from cryptonews.db.getEntities import getEntityIdsNames, getValidEntityIdsNames

from cryptonews.neo4j_db import create_articles, create_entities, \
    match_article_entity, update_valid_entities
from datetime import datetime, timedelta
import IPython
import argparse

from cryptonews.config import config
from loguru import logger

DB_PATH = config.db_path

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(subset=["title"], inplace=True)
    df["excerpt"].fillna("", inplace=True)
    df["text"] = df["title"] + " " + df["excerpt"]
    return df

def process(sd:datetime, ed:datetime):

    logger.info(f"Running for {sd} to {ed}")
    df = news_scrape_general(sd, ed)
    logger.info(f"{len(df)} documents scraped")

    df = preprocess_df(df)
    docs = df["text"].tolist()

    output = predict(docs)
    df["risk"] = output["risk"]
    df["ner_output"] = output["ner"]

    no_ent_df = df[df["ner_output"].apply(len) == 0]
    df = df[df["ner_output"].apply(len) > 0]

    exploded_df = df.explode("ner_output")
    exploded_df["entity_name"] = exploded_df["ner_output"].apply(
        lambda x: x["name"])

    toEntitiesTable(exploded_df, database=DB_PATH)
    toEntityScoresTable(exploded_df, database=DB_PATH)

    article_ids = toArticleEntityMappingTable(
        df, 1, database=DB_PATH)
    toArticleEntityMappingTable(no_ent_df, 0, database= DB_PATH)
    article_ids = [i for i in article_ids if i != None]

    # Scripts for Neo4J components
    article_df = getArticlesFromIds(article_ids, DB_PATH)
    mapping_df = getMappingFromArticleIds(article_ids, DB_PATH)
    entity_ids = mapping_df["entity_id"].tolist()

    entity_ids = list(set(entity_ids))

    # This is a merge operation so if the entity is present, it will not do anything
    entity_df = getEntityIdsNames(entity_ids, DB_PATH)
    logger.info("Adding data to Neo4J")
    create_entities(entity_df)
    create_articles(article_df)
    match_article_entity(mapping_df)


def main(start_date=None, end_date=None, no_days=None):

    if end_date and not start_date:
        raise ValueError("Start Date has to be defined if End Date is defined ")

    if not end_date:
        end_date = datetime.today()
      
    if not start_date:
        start_date = end_date - timedelta(days=1)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    #Batching
    if no_days:
        start_dates = pd.date_range(freq=f"{no_days}D",
                                    start=start_date, end=end_date)
        end_dates = start_dates + timedelta(days=no_days)
        date_pairs = zip(start_dates, end_dates)

        for sd, ed in date_pairs:
            process(sd,ed)
    else:
        process(start_date,end_date)
    
    logger.info("Updating Entity Nodes with Valid Flag")
    valid_entity_df = getValidEntityIdsNames(DB_PATH)
    valid_ids = valid_entity_df["entity_id"].tolist()
    update_valid_entities(valid_ids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Daily Script for Inference")
    parser.add_argument(
        "--start_date",
        help="[Optional] Start Date to run the script from in YYYY-MM-DD. "
        "Defaults to 1 day before current day"
    )
    parser.add_argument(
        "--end_date",
        help="[Optional] End Date to run the script from in YYYY-MM-DD. "
        "Defaults to current day"
    )
    parser.add_argument(
        "--days",
        help="[Optional] For performing inference on larger time intervals set "
        "this value to the number of days per batch. Defaults to None"
    )
    args = parser.parse_args()
    main(args.start_date, args.end_date, args.days)
