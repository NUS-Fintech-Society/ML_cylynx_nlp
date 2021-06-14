from setup import create_connection
from enum import Enum


class SourceType(Enum):
    WEBSITE = 1
    SOCIAL_MEDIA = 2


def populate_sources(source_names):
    conn = create_connection('sqlite.db')
    for source in source_names:
        create_source(conn, source)
    conn.close()


def create_source(conn, source_name):
    sql = ''' INSERT OR IGNORE INTO sources(name, type)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (source_name, SourceType.WEBSITE.value))
    conn.commit()


if __name__ == '__main__':
    sources = ["bitnewstoday", "coindesk",
               "cointelegraph", "cryptonews", "cryptoslate"]
    populate_sources(sources)
