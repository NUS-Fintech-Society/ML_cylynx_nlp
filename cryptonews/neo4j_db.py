from py2neo import Graph
from py2neo.bulk import merge_nodes, merge_relationships
from py2neo.data import Relationship
import pandas as pd



def connect_graph(): #? Maybe use a decorator?
    return Graph("bolt://localhost:7687", auth=("neo4j", "1234"))

def clear_graph():
    g = connect_graph()
    g.run("MATCH (e:Entity)-[r]-(n:Article) DELETE r")
    g.run("MATCH (r:Entity) MATCH (n:Article) DELETE n,r")

def create_articles(df: pd.DataFrame):
    g= connect_graph()
    data = df.to_dict("records")
    merge_nodes(g.auto(),data,merge_key=("Article","article_id"),labels={"Article"})

def create_entities(df: pd.DataFrame):
    """
    2 Columns: entity_id, name 
    """
    g= connect_graph()
    data = df.to_dict("records")
    merge_nodes(g.auto(),data,merge_key=("Entity","entity_id"),labels={"Entity"})

def match_article_entity(df:pd.DataFrame):
    """
    2 Columns: entity_id, article_id 
    """
    g= connect_graph()
    data =[]
    for row in df.itertuples():
        entry = (row.article_id,dict(),row.entity_id)
        data.append(entry)
    merge_relationships(
        g.auto(),data,merge_key=("MENTIONED"), start_node_key=("Article","article_id"),
        end_node_key=("Entity","entity_id"))

def update_valid_entities(entity_ids):
    """
    Set valid: true for entity nodes that fulfil a certain criteria
    """
    g = connect_graph()
    for idx in entity_ids:
        node = g.nodes.match("Entity",entity_id=idx).first()
        if node:
            node["valid"] = True
            g.push(node)

def merge_nodes(id1,id2):
    """
    If 2 nodes point to the same entity, use this function to combine them
    """
    pass
# if __name__ == "__main__":

#     graph = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))


#     article_df = pd.read_csv("test_article.csv")
#     entity_df = pd.read_csv("test_entities.csv")
    
#     create_articles(article_df)
#     create_entities( entity_df)
#     match_df = pd.read_csv("test_match.csv")
#     match_article_entity(match_df)
#     a = graph.nodes.match("Article",article_id= 1).first()
#     b = graph.nodes.match("Entity",entity_id=1).first()

#     rel = Relationship(b,"MENTIONED_BY",a)
#     graph.create(rel)