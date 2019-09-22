#!/usr/bin/env python

from pymongo import MongoClient
import json
from fire import Fire

client = MongoClient('localhost',2707)
db = client['news']
collection_currency = db['currency']

# check if db exist
# choose what json to insert
# profit


def main(json_file):
    with open(json_file) as f:
        file_data = json.loads(f)

if __name__ == '__main__':
    Fire(main)

