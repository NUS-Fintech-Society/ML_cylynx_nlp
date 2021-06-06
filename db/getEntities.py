#!/usr/bin/env python

import sqlite3
import pandas as pd

import logging
from typing import Union

# Placeholder for actual preprocess function
def __preprocess(entityName: str) -> str: 
    return entityName

def __checkDatabase(database: str) -> None:
    try: 
        sqlite3.connect(database)
    except: 
        raise Exception("The given file name is not a sqlite database file")

def toDatabase(df : pd.DataFrame, database: str) -> None: 
    __checkDatabase(database)
    assert 'EntityName' in df.columns

    con = sqlite3.connect(database)
    cur = con.cursor()
    entityNames = [__preprocess(x) for x in df['EntityName']]
    
    for entity in entityNames:
        cur.execute('SELECT * FROM Entity WHERE (EntityName=?)', (entity,))
        entry = cur.fetchone()

        if entry is None:
            cur.execute('INSERT INTO Entity (EntityName, EntityProbability) VALUES(?, ?)', (entity, 0))
            logging.info('New entry added: {}'.format('entity'))
        else:
            logging.info('Entry found')
    con.commit()
    con.close()

def getEntity(entity: str, database: str) -> Union[None, float]:
    __checkDatabase(database)

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM Entity WHERE (EntityName=?)', (entity,))
    entry = cur.fetchone()
    con.close()
    return entry

if __name__=='__main__':
    d = {'EntityName': ["btc", "ether", "bitcoin", "somethingElse"]}
    df = pd.DataFrame(data=d)

    db = 'toyDatabaseV2.db'
    toDatabase(df, db)
    print(getEntity('bitcoin', db))
    print(getEntity('somethingElse', db))
    print(getEntity('BOB', db))
