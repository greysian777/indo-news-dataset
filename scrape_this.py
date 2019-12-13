#!/usr/bin/env pipenv run python

from ehe import Link, Paragraf, FILE_NAME
from pertanggalan import generate_n_days_from_today, link, generate_from_date_range
import fire
import time
import os
import json
import pandas as pd

def generate_links(n_days, sumber, file_name=FILE_NAME,save_csv=True, save_json=False):
    """ generating links of sumber berita and save it to txt """
    list_of_dates = generate_n_days_from_today(n_days=n_days)
    puller = Link(list_of_dates, sumber=sumber, txt_mode=True)
    puller.run()
def generate_links_parallel(n_days, sumber, file_name=FILE_NAME,save_csv=True, save_json=False):
    def list_of_links():
        "get the list of links to be scraped"
        list_of_dates = generate_n_days_from_today(n_days=n_days)
        link_kompas = Link(list_of_dates, sumber=sumber, txt_mode=True)
        return link_kompas.get_all_link_kompas()
    links_to_get = list_of_links()
    pass

def generate_paragraph_from_txt(path_to_txt, parallel=False):
    """ generating single thread scraping paragraph from a given txt file of links """
    start = time.time()
    puller = Paragraf(txt_mode=True)
    puller.run('csv/',txt_path=path_to_txt)
    print(f'time spent: {time.time() - start}')


def generate_links_with_date_range(start, end, sumber, file_name=FILE_NAME):
    """
    made a csv of links from kompas within start until end range of dates
    """
    list_of_dates = generate_from_date_range(start, end)
    print(f'scraping {len(list_of_dates)} days')


if __name__ == "__main__":
    if not os.path.exists('csv/'):
        os.makedirs('csv/')
    fire.Fire()
