#!/usr/bin/env python

from pymongo import MongoClient
import json
from fire import Fire
from typing import List, Set, Dict, Tuple, Optional, NewType




class db_berita:
    def __init__(self, client, sumber, path_to_news_json,*args, **kwargs):
        self.client = MongoClient()
        self.sumber = sumber
        self.db = client['news'].sumber
        self.path_to_news_json = path_to_news_json

    def get_json(self):
        with open(self.path_to_news_json) as f:
            data = json.load(f)
        return data

    def insert_berita(self):
        result = self.db.insert_many(self.get_json(self.path_to_news_json))
        for o_id in result.inserted_ids:
            print(f'added new {self.sumber}, berita id is {o_id}')


if __name__ == '__main__':
    pass
