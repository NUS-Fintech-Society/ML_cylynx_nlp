from articles import create_article
import pandas as pd
import sqlite3
import json
import logging
from setup import create_connection
from sqlite3 import Error


def __checkDatabase(database: str) -> None:
    try:
        sqlite3.connect(database)
    except:
        raise Exception("The given file name is not a sqlite database file")

def read_data() -> pd.DataFrame():
    df0 = pd.read_csv("../output/output_0.csv")
    df1 = pd.read_csv("../output/output_1.csv")
    df2 = pd.read_csv("../output/output_2.csv")
    df3 = pd.read_csv("../output/output_3.csv")
    df4 = pd.read_csv("../output/output_4.csv")
    df5 = pd.read_csv("../output/output_5.csv")
    df6 = pd.read_csv("../output/output_6.csv")
    df7 = pd.read_csv("../output/output_7.csv")
    df8 = pd.read_csv("../output/output_8.csv")

    df = pd.concat([df0, df1, df2, df3, df4, df5,
                df6, df7, df8], ignore_index=True)
    return df


def initiate_mapping(database: str, df: pd.DataFrame()) -> None:
    __checkDatabase(database)

    con = sqlite3.connect(database)
    cur = con.cursor()

    for i in range(len(df)):  # for each article
        row = df.iloc[i]
        article = (row['title'], row['excerpt'], row['date_time'],
                   row['article_url'], row['risk'], row['source'])
        article_id = create_article(con, article)

        ner_list = json.loads(row['ner'].replace("\'", "\""))

        for each in ner_list:  # for each entity

            # Retrieve entity id
            entity_name = each['name']
            cur.execute(
                'SELECT entity_id FROM entities WHERE (name=?)', (entity_name,))
            entity_id = cur.fetchone()

            if entity_id is None:
                logging.info('Entity: {} does not exist'.format(entity_name))

            else:
                logging.info('Entity found')
                mapData = (entity_id, article_id)

                code = ''' INSERT INTO mapping (entity_id, article_id)
              VALUES(?, ?) '''
                cur = con.cursor()
                cur.execute(code, mapData)
                con.commit()
                logging.info('Mapping Entry inserted')

    con.close()


if __name__ == '__main__':
    df = read_data()
    db = 'sqlite.db'
    initiate_mapping(db, df)
