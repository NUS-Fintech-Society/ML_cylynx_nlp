from .articles import create_article
from .getEntities import getEntityIdByName

import pandas as pd
import sqlite3

import json
import logging

def read_data() -> pd.DataFrame():
    df = pd.read_csv('/home/ubuntu/ML_cylynx_nlp/output/output.csv')
    return df


def initiate_mapping(df: pd.DataFrame, entities_present: bool, database: str = 'sqlite.db') -> None:
    con = sqlite3.connect(database)
    cur = con.cursor()

    for idx in range(len(df)):
        row = df.iloc[idx]
        article = (row['title'], row['excerpt'], row['date_time'],
                   row['article_url'], row['risk'], row['source'], 1 if entities_present else 0)
        article_id = create_article(con, cur, article) # Inserts article. No article uniqueness check done here

        ner_list = json.loads(row['ner_output'].replace("\'", "\""))

        for entity in ner_list: 
            assert entity['type'] == 'Entity'
            entity_name = entity['name']
            entity_confidence = entity['confidence']
            entity_id = getEntityIdByName(entity_name, database)

            if entity_id is not None:
                mapData = (entity_id, article_id, entity_confidence)
                code = "INSERT INTO mapping (entity_id, article_id) VALUES(?, ?)"

                cur = con.cursor()
                cur.execute(code, mapData)
                con.commit()
                logging.info('Mapping Entry inserted')
            else:
                logging.warn("Mapping Entry not inserted")
    con.close()


if __name__ == '__main__':
    df = read_data()
    print(df.head())
    # db = 'sqlite.db'
    # initiate_mapping(db, df)
