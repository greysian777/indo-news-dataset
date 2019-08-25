#!/usr/bin/env pipenv run python

from ehe import Link, Paragraf, FILE_NAME 
from pertanggalan import generate_n_days_from_today, link, generate_from_date_range
import fire
import time
import os
import json
import pandas as pd  

def generate_links(n_days, sumber, file_name=FILE_NAME,save_csv=True, save_json=False):
    """
    makes a csv of links from kompas within n_days from today (date of running)
    """
    CSV_FILENAME = 'csv/'+file_name+f'_{sumber}_link.csv'
    JSON_FILENAME = 'json/'+file_name+f'_{sumber}_link.json'
    list_of_dates = generate_n_days_from_today(n_days=n_days)
    print(f'generating {n_days} days worth of news')
    puller = Link(list_of_date=list_of_dates, sumber=sumber)
    puller = puller.run() 
    if save_csv and save_json:
        puller.to_csv(CSV_FILENAME)
        puller.to_json(JSON_FILENAME)
    elif save_csv:
        puller.to_csv(CSV_FILENAME)
    elif save_json: 
        puller.to_json(JSON_FILENAME)

def generate_links_txt(n_days, sumber): 
    list_of_dates = generate_n_days_from_today(n_days=n_days)
    puller = Link(list_of_dates, sumber=sumber, txt_mode=True)
    puller.run()

def generate_paragraph_from_txt(path_to_txt, parallel=False): 
    puller = Paragraf(txt_mode=True)
    puller.run('csv/',txt_path=path_to_txt)

def generate_paragraph(): 
    pass
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
