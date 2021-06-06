import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


if __name__ == '__main__':
    database = "sqlite.db"

    sql_create_sources_table = """ CREATE TABLE IF NOT EXISTS sources (
                                        source_id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE ,
                                        type integer
                                    ); """

    #TODO add in sentiment_score to below table
    sql_create_articles_table = """ CREATE TABLE IF NOT EXISTS articles (
                                        article_id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        excerpt text,
                                        date_time text,
                                        article_url text,
                                        source text,
                                        FOREIGN KEY (source)
                                            REFERENCES sources (name) 
                                    ); """

    conn = create_connection("sqlite.db")

    if conn is not None:
        # create source table
        create_table(conn, sql_create_sources_table)

        # create articles table
        create_table(conn, sql_create_articles_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")
