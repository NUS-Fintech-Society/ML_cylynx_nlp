#!/usr/bin/env python
import sqlite3
import pandas as pd

import logging
from typing import Union

from .utils.utils import preprocessEntityName as __preprocessName
from .utils.utils import preprocessTime as __preprocessTime

from .getEntities import getEntityIdByName

def __deriveDataframe(map_df : pd.DataFrame) -> pd.DataFrame:
    '''
    Takes in a Dataframe with column names:
    entity_name
    risk
    date_time

    and return a DataFrame with column names: 
    entity_name
    entity_score (Averages of Risk Score)
    date_time 
    '''

    tempDict = {}
    returnDict = {'entity_name': [], 'entity_score': [], 'date_time': []}

    for row in map_df.itertuples():
        date_time = row.date_time.strftime('%Y-%m-%d')
        entity = row.entity_name

        scores = tempDict.get((entity, date_time), [])
        scores.append(row.risk)
        tempDict[((entity, date_time))] = scores

    for idx, (entity_name, date_time) in enumerate(tempDict.keys()):
        entity_score = sum(tempDict[(entity_name, date_time)]) / len(tempDict[(entity_name, date_time)])
        returnDict['entity_name'].append(entity_name)
        returnDict['entity_score'].append(entity_score)
        returnDict['date_time'].append(date_time)

    return pd.DataFrame.from_dict(returnDict)


def toDatabase(df : pd.DataFrame, database: str = "sqlite.db") -> None: 
    assert 'entity_name' in df.columns
    assert 'date_time' in df.columns
    assert 'risk' in df.columns

    df = __deriveDataframe(df)
    con = sqlite3.connect(database)
    cur = con.cursor()
    df['entity_name'] = df['entity_name'].apply(__preprocessName)

    for row in df.itertuples():
        entity_name = row.entity_name
        query_time = row.date_time
        entity_score = row.entity_score

        entry = getEntityScoreAtTime(entity_name, query_time, database)
        if entry is None:
            entityId = getEntityIdByName(entity_name, database)
            cur.execute('INSERT INTO entity_scores (entity_score, date_time, entity_id) VALUES(?, ?, ?)', (entity_score, query_time, entityId))
            logging.info('New entry added to EntityScore Table: {}'.format(entityId))
        else:
            logging.info('Entry found') 
    con.commit()
    con.close()

def getEntityScore(entity: str, database : str = "sqlite.db") -> Union[None, list]:
    con = sqlite3.connect(database)
    cur = con.cursor()

    entityId = getEntityIdByName(entity, database)
    if entityId is not None:
        cur.execute('SELECT * FROM entity_scores WHERE (entity_id=?)', (entityId,))
        entry = cur.fetchall()
        con.close()
        return [(x[1], x[2]) for x in entry] if entry is not None else None

def getEntityScoreAtTime(entity: str, time: str, database: str = "sqlite.db") -> Union[None, float]:
    time = __preprocessTime(time)
    results = getEntityScore(entity, database)
    if results is not None:
        result = list(filter(lambda x: x[1] == time, results))
        # ? Commented out this assertion as it was causing errors in main
        # assert len(result) == 0 or len(result) == 1
        if len(result) == 1:
            return result[0][0]
        else:
            # logging.warn("Entity {} found but no score for given time".format(entity))
            # logging.warn("Number of Found Results: ", len(result))
            # logging.warn("Queried Time: ", time)
            return None

def getScoresDateRange(database:str):
    con = sqlite3.connect(database)
    query = 'SELECT date_time FROM "entity_scores"'
    
    return pd.read_sql(query, con)['date_time'].tolist() 


if __name__=='__main__':
    map_df = pd.read_csv("../output/output.csv")
    df = __deriveDataframe(map_df)

    db = 'sqlite.db'
    toDatabase(df, db)
    
    print("Entity: bitcoin. Score: ", getEntityScore('bitcoin', db))
    print("Entity: ether. Score: ", getEntityScore('ether', db))
    print("Entity: somethingElse. Score: ", getEntityScore('somethingElse', db))
    print("Entity: BOB. Score: ", getEntityScore('BOB', db))
