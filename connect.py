#!/usr/bin/env python

from pymongo import MongoClient
import json
from fire import Fire
from typing import List, Set, Dict, Tuple, Optional, NewType


# custom type hints
Client = NewType('client', MongoClient)

client = MongoClient()
# check if db exist
def check_if_db_exist(name:str) -> Client:
    if 'news' in client.list_database_names():
        return client['news']
    else:
        return client.news


# choose what json to insert
# profit

def fill_json():
    pass

def fill_single():
    pass

def main(json_file):
    with open(json_file) as f:
        file_data = json.loads(f)

if __name__ == '__main__':
    print(client.list_database_names())

