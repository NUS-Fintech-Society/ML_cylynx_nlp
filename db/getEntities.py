#!/usr/bin/env python

import sqlite3
import pandas as pd

import logging
from typing import Union

from .utils.utils import preprocessEntityNames as __preprocessNames
from .utils.utils import preprocessEntityName as __preprocessName

def toDatabase(df : pd.DataFrame, database: str = "sqlite.db") -> None: 
    assert 'entity_name' in df.columns # TODO: see if this is still the column name

    con = sqlite3.connect(database)
    cur = con.cursor()
    entities = __preprocessNames(df['entity_name'].tolist())

    entityNames = [x[0] for x in entities]
    entityValid = [x[1] for x in entities] # True if valid
    
    for i, entity in enumerate(entityNames):
        cur.execute('SELECT * FROM entities WHERE (name=?)', (entity,))
        entry = cur.fetchone()

        if entry is None:
            cur.execute('INSERT INTO entities (name, isValid) VALUES(?, ?)', (entity, entityValid[i]))
            logging.info('New entry added: {}'.format(entity))
        else:
            logging.info('Entry found')
    con.commit()
    con.close()

def getEntityIdByName(entity_name: str, database: str = "sqlite.db") -> Union[None, int]:
    con = sqlite3.connect(database)
    cur = con.cursor()

    entity_name = __preprocessName(entity_name)
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

    db = 'sqlite3.db'
    toDatabase(df, db)
    print(getEntityIdByName('bitcoin', db))
    print(getEntityIdByName('ether', db))
    print(getEntityIdByName('somethingElse', db))

    print(getEntityNameById(14))
