#!/usr/bin/env python
import sqlite3
from datetime import datetime
import pandas as pd

import logging
from typing import Union

from utils import preprocessEntityName as __preprocess
from utils import preprocessTime as __preprocessTime

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
    Entities = list(map_df['entity_name'])
    RiskScore = list(map_df['risk'])

    tempDict = {}
    returnDict = {'entity_name': [], 'entity_score': [], 'date_time': []}
    for idx, entity in enumerate(Entities):
        date_time = map_df['date_time'][idx].split(' ')[0]
        scores = tempDict.get((entity, date_time), [])

        scores.append(RiskScore[idx])
        tempDict[(entity, date_time)] = scores

    for idx, (entity_name, date_time) in enumerate(tempDict.keys()):
        entity_score = sum(tempDict[(entity_name, date_time)]) / len(tempDict[(entity_name, date_time)])
        returnDict['entity_name'].append(entity_name)
        returnDict['entity_score'].append(entity_score)
        returnDict['date_time'].append(date_time)

    return pd.DataFrame.from_dict(returnDict)


def toDatabase(df : pd.DataFrame, database: str = "sqlite.db") -> None: 
    assert 'entity_name' in df.columns
    assert 'entity_score' in df.columns
    assert 'date_time' in df.columns

    con = sqlite3.connect(database)
    cur = con.cursor()
    entityNames = [__preprocess(x) for x in df['entity_name']]
    entityScores = df['entity_score']
    queryTime = df['date_time']
    
    for i, entity in enumerate(entityNames):
        cur.execute('SELECT * FROM entities WHERE (name=?)', (entity,))
        entry = cur.fetchone()

        if entry is None:
            logging.warn('Entry not found in Entity Table. EntityName: {}'.format(entity))
        else:
            logging.info('Entry found in Entity Table. Checking EntityScore Table...')
            
            entityId = entry[0]
            cur.execute('SELECT * FROM entity_scores WHERE (entity_id=?) AND (date_time=?)', (entityId, queryTime[i]))
            entry = cur.fetchone()

            if entry is None:
                cur.execute('INSERT INTO entity_scores (entity_score, date_time, entity_id) VALUES(?, ?, ?)', (entityScores[i], queryTime[i], entityId))
                logging.info('New entry added to EntityScore Table: {}'.format(entityId))
            else:
                logging.info('Entry found') 
    con.commit()
    con.close()

def getEntityScore(entity: str, database : str = "sqlite.db") -> Union[None, list]:
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM entities WHERE (name=?)', (entity,))
    entry = cur.fetchone()
    if entry is None:
        logging.warn("No such entity found in Entity Table")
        con.close()
        return None
    else:
        cur.execute('SELECT * FROM entity_scores WHERE (entity_id=?)', (entry[0],))
        entry = cur.fetchall()
        con.close()
        return [(x[1], x[2]) for x in entry] if entry is not None else None

def getEntityScoreAtTime(entity: str, time: str, database: str = "sqlite.db") -> Union[None, float]:
    time = __preprocessTime(time)
    results = getEntityScore(entity, database)
    if results is None:
        return None
    else:
        result = list(filter(lambda x: x[1] == time, results))
        if len(result) == 1:
            return result[0][0]
        else:
            logging.warn("Entity {} found but no score for given time".format(entity))
            return None

if __name__=='__main__':
    map_df = pd.read_csv("../output/output.csv")
    df = __deriveDataframe(map_df)

    db = 'sqlite.db'
    toDatabase(df, db)
    
    print("Entity: bitcoin. Score: ", getEntityScore('bitcoin', db))
    print("Entity: ether. Score: ", getEntityScore('ether', db))
    print("Entity: somethingElse. Score: ", getEntityScore('somethingElse', db))
    print("Entity: BOB. Score: ", getEntityScore('BOB', db))
