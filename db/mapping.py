from prediction import predict
import pandas as pd
import sqlite3
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


con = sqlite3.connect("sqlite.db")
cur = con.cursor()
articles = pd.read_sql_query("SELECT * from articles", con)

map_df = pd.DataFrame()
ArticleIds = []
Entities = []
Risks = []

# for i in range(len(articles)):
for i in range(1):
    article_id = articles['article_id'].iloc[i]
    title = articles['title'].iloc[i]
    excerpt = articles['excerpt'].iloc[i]
    title += ' '
    title += excerpt

    output_dict = predict(title)
    # output_dict looks like this
    # {"ner": [{"name": "Bitcoin", "type": ..., "confidence": ...},
    #          {"name": "Bank of India", "type": ..., "confidence": ...}, ...],
    #  "risk": some % value}

    ArticleIds.append(article_id)
    Entities.append(output_dict['ner'])
    Risks.append(output_dict['risk'])

map_df = pd.DataFrame({"ArticleId": ArticleIds,
                      "Entities": Entities,
                      "Risk Score": Risks})

map_df.to_sql('mapping', con, if_exists="append", index=False)
con.close()
