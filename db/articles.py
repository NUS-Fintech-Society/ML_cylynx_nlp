import pandas as pd
from setup import create_connection


def create_article(conn, article):
    sql = ''' INSERT INTO articles(title, excerpt, date_time, article_url, risk, source)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, article)
    conn.commit()
    return cur.lastrowid
