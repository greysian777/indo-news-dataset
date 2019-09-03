#!/usr/bin/env python3

from ehe import Paragraf
from multiprocessing import Pool
from tqdm import tqdm
import numpy as np
import os
import time
import json
from glob import glob
import fire
import random


def pembagi(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def main(list_of_links, sumber, nama_file, n_jobs=25):
    if not os.path.exists(f'csv/{sumber}'):
        os.makedirs(f'csv/{sumber}')

    list_of_links = np.asarray(list_of_links)
    berita = Paragraf()
    print('getting ', len(list_of_links))
    with Pool(n_jobs) as p:
        if sumber == 'kompas':
            hasil = list(
                tqdm(p.imap(berita.get_kompas, list_of_links), total=len(list_of_links)))
        elif sumber == 'detik':
            hasil = list(
                tqdm(p.imap(berita.get_detik, list_of_links), total=len(list_of_links)))
        elif sumber == 'tempo':
            hasil = list(
                tqdm(p.imap(berita.get_tempo, list_of_links), total=len(list_of_links)))
        elif sumber == 'bisnis':
            hasil = list(
                tqdm(p.imap(berita.get_bisnis, list_of_links), total=len(list_of_links)))
        else:
            print('sumber belum ditentukan')
            raise ValueError

        p.terminate()
        p.join()
        with open(f'csv/{sumber}/{nama_file}___dump_parallel_hasil.json', "a+") as f:
            json.dump(hasil, f, indent=4, sort_keys=True, default=str)


def run(sumber, path_to_txt, chunks=100):
    """ sumber: berita, path_to_txt: txt file with link per line, chunks: saving every n_th chunk
        will dump to .json with part number, then aggregate after finished
    """
    berita_c = np.asarray(
        list(pembagi(open(path_to_txt).read().splitlines(), chunks)))
    for i, link in enumerate(berita_c):
        file_name = f'{i}_{sumber}'
        try:
            print(f'part {i}/{len(berita_c)}')
            time.sleep(random.randint(5, 29))
            main(link, sumber=sumber, nama_file=file_name)
        except Exception as e:
            print(str(e))
            time.sleep(random.randint(10, 60))
            continue
    print('finished\n\n\n\n')
    print('now aggregating json files')
    json_aggregator(sumber)


def json_aggregator(sumber):
    json_path = f'csv/{sumber}/*__*.json'
    berita_json = glob(json_path)

    berita = []
    for file in berita_json:
        try:
            with open(file) as f:
                berita.append(json.load(f))
        except Exception as e:
            print(str(e))
            pass

    # check if path available
    if not os.path.exists(f'hasil/{sumber}'):
        os.makedirs(f'hasil/{sumber}')
    berita = [sub for i in berita for sub in i]
    with open(f'hasil/{sumber}.json', 'w+') as f:
        json.dump(berita, f, indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    fire.Fire(run)