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
    database = "sqlite2.db"

    sql_create_sources_table = """ CREATE TABLE IF NOT EXISTS sources (
                                        source_id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE ,
                                        type integer
                                    ); """

    sql_create_articles_table = """ CREATE TABLE IF NOT EXISTS articles (
                                        article_id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        excerpt text,
                                        date_time text,
                                        article_url text,
                                        risk real,
                                        source text,
                                        no_entity_flag boolean,
                                        FOREIGN KEY (source)
                                            REFERENCES sources (name) 
                                    ); """

    sql_create_entities_table = """ CREATE TABLE IF NOT EXISTS entities ( 
                                        entity_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        isValid integer NOT NULL
                                    ); """

    sql_create_entity_score_table = """ CREATE TABLE IF NOT EXISTS entity_scores (
                                            entity_score_id integer PRIMARY KEY,
                                            entity_score real, 
                                            date_time text, 
                                            entity_id integer, 
                                            FOREIGN KEY (entity_id)
                                                REFERENCES entities (entity_id)
                                        ); """

    sql_create_mapping_table = """ CREATE TABLE IF NOT EXISTS mapping (
                                            mapping_id integer PRIMARY KEY,
                                            entity_id integer, 
                                            article_id integer,
                                            FOREIGN KEY (entity_id)
                                                REFERENCES entities (entity_id),
                                            FOREIGN KEY (article_id)
                                                REFERENCES articles (article_id)
                                        ); """

    conn = create_connection("sqlite2.db")

    if conn is not None:
        # create source table
        create_table(conn, sql_create_sources_table)

        # create articles table
        create_table(conn, sql_create_articles_table)

        # create entities table
        create_table(conn, sql_create_entities_table)

        # create entity score table
        create_table(conn, sql_create_entity_score_table)

        # create mapping table
        create_table(conn, sql_create_mapping_table)

        conn.close()
    else:
        print("Error! cannot create the database connection.")
