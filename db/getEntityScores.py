#!/usr/bin/env python
import sqlite3
import pandas as pd
from datetime import datetime

import logging
from typing import Union

# Placeholder for actual preprocess function
def __preprocess(entityId: str) -> str: 
    return entityId

# Placeholder for actual getScore function
def __getScore(entityScore: float) -> float: 
    return entityScore

def __getTime() -> str:
    return datetime.now().isoformat()

def __checkDatabase(database: str) -> None:
    try: 
        sqlite3.connect(database)
    except: 
        raise Exception("The given file name is not a sqlite database file")

def __deriveDataframe(map_df : pd.DataFrame) -> pd.DataFrame:
    '''
    Takes in a Dataframe with column names:
    ArticleId
    Entities
    Risk Score

    and return a DataFrame with column names: 
    EntityName
    EntityScore (Averages of Risk Score)
    '''
    ArticleIds = list(map_df['ArticleId'])
    Entities = list(map_df['Entities'])
    RiskScore = list(map_df['Risk Score'])

    tempDict = {}
    returnDict = {'EntityName': [], 'EntityScore': []}
    for idx, e in enumerate(Entities): 
        for entity in e: 
            scores = tempDict.get(entity, [])
            scores.append(RiskScore[idx])
            tempDict[entity] = scores
            if entity not in returnDict['EntityName']:
                returnDict['EntityName'].append(entity) 

    for idx, e in enumerate(returnDict['EntityName']):
        returnDict['EntityScore'].append(sum(tempDict[e]) / len(tempDict[e])) # TODO: Find a better way to do this
    print(returnDict)
    return pd.DataFrame.from_dict(returnDict)


def toDatabase(df : pd.DataFrame, database: str) -> None: 
    __checkDatabase(database)
    assert 'EntityName' in df.columns
    assert 'EntityScore' in df.columns

    con = sqlite3.connect(database)
    cur = con.cursor()
    entityNames = [__preprocess(x) for x in df['EntityName']]
    entityScores = [__getScore(x) for x in df['EntityScore']]
    
    for i, entity in enumerate(entityNames):
        cur.execute('SELECT * FROM Entity WHERE (EntityName=?)', (entity,))
        entry = cur.fetchone()

        if entry is None:
            logging.warn('Entry not found in Entity Table. EntityName: {}'.format(entity))
        else:
            logging.info('Entry found in Entity Table. Checking EntityScore Table...')
            
            entityId = entry[0]
            cur.execute('SELECT * FROM EntityScore WHERE (EntityId=?)', (entityId,))
            entry = cur.fetchone()

            if entry is None:
                cur.execute('INSERT INTO EntityScore (EntityScoreAverage, Time, EntityId) VALUES(?, ?, ?)', (entityScores[i], __getTime(), entityId))
                logging.info('New entry added to EntityScore Table: {}'.format(entityId))
            else:
                logging.info('Entry found') 
    con.commit()
    con.close()

def getEntityScore(entity: str, database: str) -> Union[None, float]:
    __checkDatabase(database)

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM Entity WHERE (EntityName=?)', (entity,))
    entry = cur.fetchone()
    if entry is None:
        logging.warn("No entity found in Entity Table")
        con.close()
        return None
    else:
        cur.execute('SELECT * FROM EntityScore WHERE (EntityId=?)', (entry[0],))
        entry = cur.fetchone()
        con.close()
        return entry[1]

if __name__=='__main__':
    d = {'EntityName': ["bitcoin", "somethingElse", "notInEntityTable"]}
    # df = pd.DataFrame(data=d)
    map_df = pd.DataFrame({"ArticleId": [19], "Entities": [["bitcoin", 'ether']], "Risk Score": [0.3]})
    df = __deriveDataframe(map_df)
    
    db = 'toyDatabaseV2.db'
    toDatabase(df, db)
    print(getEntityScore('bitcoin', db))
    print(getEntityScore('ether', db))

    # print(getEntityScore('bitcoin', db))
    # print(getEntityScore('somethingElse', db))
    # print(getEntityScore('BOB', db))
