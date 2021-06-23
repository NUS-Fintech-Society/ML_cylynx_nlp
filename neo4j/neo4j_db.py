from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
from py2neo.data import Relationship
import pandas as pd

# https://py2neo.org/2021.1/bulk/index.html


df_cols = ["article_id","title","excerpt","date_time","article_url",
           "risk","source"]

def create_articles(g, df: pd.DataFrame):
    data = df.to_dict("records")
    create_nodes(g.auto(),data,labels={"Article"})

def create_entities(g,df: pd.DataFrame):

    data = df.to_dict("records")
    print(data)
    create_nodes(g.auto(),data,labels={"Entity"})

def match_article_entity(g,df:pd.DataFrame):
    """
    3 Columns: entity_id, entity_name, article_id 
    """
    data =[]
    for row in df.itertuples():
        entry = ((row.entity_id),{"test":1},row.article_id)
        data.append(entry)
    print([len(i) for i in data])
    create_relationships(
        g.auto(),data,rel_type="MENTIONED",start_node_key=("Entity","entity_id"),
        end_node_key=("Article","article_id"))
    print("done")





if __name__ == "__main__":

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))
    graph.run("MATCH (e:Entity)-[r]-(n:Article) DELETE r")
    graph.run("MATCH (r:Entity) MATCH (n:Article) DELETE n,r")


    article_df = pd.read_csv("test_article.csv")
    entity_df = pd.read_csv("test_entities.csv")
    
    create_articles(graph, article_df)
    create_entities(graph, entity_df)
    match_df = pd.read_csv("test_match.csv")
    match_article_entity(graph,match_df)
    a = graph.nodes.match("Article",article_id= 1).first()
    b = graph.nodes.match("Entity",entity_id=1).first()
    print(a,b)

    rel = Relationship(b,"MENTIONED_BY",a)
    # graph.create(rel)