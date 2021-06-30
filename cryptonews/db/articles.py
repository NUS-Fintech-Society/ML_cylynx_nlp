import pandas as pd
import sqlite3
from .setup import create_connection

def create_article(con, cur, article):
    cur.execute('SELECT * FROM articles WHERE (title=? AND excerpt=? AND date_time=? AND article_url=? AND risk=? AND source=? AND no_entity_flag=?)', article)
    existing_articles = cur.fetchone()

    if existing_articles is None:
        sql = ''' INSERT INTO articles(title, excerpt, date_time, article_url, risk, source, no_entity_flag)
                VALUES(?, ?, ?, ?, ?, ?, ?) '''
        # cur = conn.cursor()
        cur.execute(sql, article)
        con.commit()
        return cur.lastrowid
    else:
        return None

def getArticlesFromIds(ids,database:str ="sqlite.db") -> pd.DataFrame:
    ids = tuple(ids)
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT * FROM articles WHERE " \
        "article_id IN {}".format(ids)
    df = pd.read_sql_query(query,con)
    return df

