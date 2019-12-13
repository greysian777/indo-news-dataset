#!/usr/bin/env pipenv run python

from ehe import Link, Paragraf, FILE_NAME
from pertanggalan import generate_n_days_from_today, link, generate_from_date_range
import fire
import time
import os
import json
import pandas as pd


def generate_links(n_days, sumber, file_name=FILE_NAME, save_csv=True, save_json=False):
    """ generating links of sumber berita and save it to txt """
    list_of_dates = generate_n_days_from_today(n_days=n_days)
    puller = Link(list_of_dates, sumber=sumber, txt_mode=True)
    puller.run()


def generate_links_parallel(n_days, sumber, file_name=FILE_NAME, save_csv=True, save_json=False, n_jobs=25):
    from scrape_parallel import pembagi
    os.makedirs('links/tmp',exist_ok=True)


    list_of_dates = generate_n_days_from_today(n_days=n_days)
    link_kompas = Link(list_of_dates, sumber=sumber, txt_mode=True)
    links_to_get = link_kompas.get_all_link_kompas()
    links_to_get_chunked = list(pembagi(links_to_get,1000))

    # decouple this guy
    from multiprocessing import Pool
    from tqdm import tqdm
    for i, link in enumerate(links_to_get_chunked):
        with Pool(n_jobs) as p:
            hasil = list(
                tqdm(p.imap(link_kompas.run_one_link_kompas, link), total=len(link)))
        with open(f'links/tmp/{i}__dump_links.txt', 'a+') as f:
            for h  in hasil:
                for i in h:
                    f.writelines(i+'\n')

def generate_paragraph_from_txt(path_to_txt, parallel=False):
    """ generating single thread scraping paragraph from a given txt file of links """
    start = time.time()
    puller = Paragraf(txt_mode=True)
    puller.run('csv/', txt_path=path_to_txt)
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
