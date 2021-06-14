#!/usr/bin/env python

import sqlite3
import pandas as pd

import logging
from typing import Union

from utils import preprocessEntityName as __preprocess

def toDatabase(df : pd.DataFrame, database: str = "sqlite.db") -> None: 
    assert 'entity_name' in df.columns

    con = sqlite3.connect(database)
    cur = con.cursor()
    entityNames = [__preprocess(x) for x in df['entity_name']]
    
    for entity in entityNames:
        cur.execute('SELECT * FROM entities WHERE (name=?)', (entity,))
        entry = cur.fetchone()

        if entry is None:
            cur.execute('INSERT INTO entities (name) VALUES(?)', (entity,))
            logging.info('New entry added: {}'.format(entity))
        else:
            logging.info('Entry found')
    con.commit()
    con.close()

def getEntityIdByName(entity_name: str, database: str = "sqlite.db") -> Union[None, int]:
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM entities where (name=?)', (entity_name,))
    entry = cur.fetchone()
    con.close()

    if entry is not None: 
        return entry[0]
    else: 
        logging.warn("Entity of name {} not found in entity table".format(entity_name))
    return None

def getEntityNameById(entity_id: int, database: str = "sqlite.db") -> Union[None, str]:
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM entities WHERE (entity_id=?)', (entity_id,))
    entry = cur.fetchone()
    con.close()
    
    if entry is not None: 
        return entry[1]
    else:
        logging.warn("Entity Id {} not found in entity table".format(entity_id))
        return None

if __name__=='__main__':
    df = pd.read_csv('../output/output.csv')

    db = 'sqlite.db'
    toDatabase(df, db)
    print(getEntityIdByName('bitcoin', db))
    print(getEntityIdByName('ether', db))
    print(getEntityIdByName('somethingElse', db))

    print(getEntityNameById(14))
