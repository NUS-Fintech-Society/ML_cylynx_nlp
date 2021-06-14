from db.setup import create_connection
import pandas as pd

#Might Require date checking
#TODO: Preload article data as well so that we can easily fetch what headlines
def fetch_data():
    conn = create_connection("db/sqlite.db")
    #Find Entities which have more than 10 occurences
    query = """ SELECT * FROM "entity_scores" s 
    INNER JOIN "entities" e ON e.entity_id = s.entity_id
    GROUP BY s.entity_id
    HAVING COUNT(s.entity_id) > 10 
    """
    df = pd.read_sql(query,conn)
    id_map = {row["entity_id"][0]:row["name"] for _,row in df.iterrows()}
    ids = tuple(df["entity_id"].iloc[:,0].tolist())
    query = "SELECT * FROM entity_scores WHERE " \
        "entity_id IN {}".format(ids)
    data_df = pd.read_sql(query,conn)
    
    data_df["name"] = data_df["entity_id"].map(id_map)
    return data_df
