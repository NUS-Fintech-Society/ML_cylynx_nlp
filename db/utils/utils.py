import csv
import pandas as pd

from typing import List, Tuple, Dict

def mapping(array: List[str], mapping_csv : str = '/home/ubuntu/ML_cylynx_nlp/db/utils/mapping.csv') -> List[str]:
    """
    Takes in an array of entity names and mapping definitions and apply rule
    E.g. maps BTC, bitcoin => bitcoin

    Args:
        array (List[str]): List of entity names
        mapping_csv (str): filename where mapping definitions are defined

    Returns:
        List[str]: List of entity names after mapped according to given rule
    """
    mapping = pd.read_csv(mapping_csv)
    mapping = dict(zip(mapping.old, mapping.new))
    return list(map(lambda x: mapping[x] if x in mapping else x, array))


def blacklist(array: List[str], blacklist_csv: str = '/home/ubuntu/ML_cylynx_nlp/db/utils/blacklist.csv') -> List[Tuple[str, bool]]:
    """
    Takes in an array of entity names and definitions of blacklisted entities 
    and apply rule

    Args: 
        array (List[str]): List of entity names
        blacklist_csv (str): filename where blacklist definitions are defined

    Returns:
        List[str]: List of (entity name, isValid), where isValid is true if not blacklisted
    """
    blacklist = pd.read_csv(blacklist_csv)
    
    assert 'entity' in blacklist.columns

    blacklist = blacklist["entity"].tolist()
    return list(map(lambda x: (x, x not in blacklist), array))

def preprocessEntityNames(array: List[str]) -> List[Tuple[str, bool]] :
    '''
    Takes in a list of entity names and apply preprocessing.
    Current preprocessing includes lowercase => mapping => blacklisting

    Args: 
        array (List[str]): List of entity names

    Returns:
        List[str]: List of (entity name, isValid), where isValid is true if not blacklisted
    '''
    array = list(map(lambda x : x.lower(), array)) 
    return blacklist(mapping(array))

def preprocessEntityName(entityName: str) -> str:
    '''
    Takes in an entity name and apply preprocessing.
    Alias for single entity name preprocessing. Define preprocessing
    approach in preprocessEntityNames

    Args: 
        entityName (str)

    Returns:
        str: entityName after preprocessing
    '''
    return preprocessEntityNames([entityName])[0][0]

def preprocessTime(array: List[str]) -> List[str] :
    '''
    Takes in a list of time and apply preprocessing
    TODO: find a way to enforce time format into (YYYY-MM-DD)

    Args: 
        array (List[str]): list of time represented in strings
    
    Returns: 
        List[str]: List of preprocessed time, represented in strings (YYYY-MM-DD)
    '''
    return array

# Functions to add new blacklisted entities
# Blacklisted entities defined in blacklist.csv
def blacklist_single(entity:str) -> None:
    with open(r'blacklist.csv','a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow([entity])

def blacklist_bulk(entityList:List[str]) -> None:
    for entity in entityList:
        blacklist_single(entity)

# Function to add new mappings
# Mapping defined in mapping.csv
OldEntityName = str
NewEntityName = str
mapping_dict = Dict[OldEntityName, NewEntityName]

def map_single(old:OldEntityName, new:NewEntityName) -> None:
    with open(r'mapping.csv','a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow([old, new])

def map_bulk(dic: mapping_dict) -> None:
    for old,new in dic.items():
        map_single(old,new)