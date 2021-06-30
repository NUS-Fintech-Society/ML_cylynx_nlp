import csv
from typing import List

def blacklist_single(entity:str):
    with open(r'blacklist.csv','a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow([entity])

def blacklist_bulk(entityList:List[str]):
    for entity in entityList:
        blacklist_single(entity)


def map_single(old:str,new:str):
    with open(r'mapping.csv','a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow([old, new])

# Dictionary where key is old value, value is new value
def map_bulk(dic):
    for old,new in dic.items():
        map_single(old,new)

def clean_data(array):
    blacklist = pd.read_csv("blacklist.csv")["entity"].tolist()
    mapping = pd.read_csv("mapping.csv")
    mapping = dict(zip(mapping.old,mapping.new))
    return list(map(lambda x:mapping[x] if x in mapping else x,
        filter(lambda x:x not in blacklist, array)))

# TODO: Maybe find better names for these
def preprocess(array):
    mapping = pd.read_csv('mapping.csv')
    mapping = dict(zip(mapping.old, mapping.new))
    return list(map(lambda x: mapping[x] if x in mapping else x, array))

def blacklist(array):
    blacklist = pd.read_csv("blacklist.csv")["entity"].tolist()
    return list(map(lambda x: (x, x not in blacklist), array))

def clean_data2(array):
    return blacklist(preprocess(array))
