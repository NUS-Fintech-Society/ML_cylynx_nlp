import pandas as pd
from setup import create_connection

df = pd.read_csv("../data/data.csv")
# TODO add in sentiment_score to below df and articles table
df = df[['title', 'excerpt', 'date_time', 'article_url', 'source']]
conn = create_connection("sqlite.db")
df.to_sql('articles', conn, if_exists="append", index=False)
conn.close()
