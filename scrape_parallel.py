#!/usr/bin/env python3

from multiprocessing import Pool
from colorama import Back, Fore, init
from tqdm import tqdm
import numpy as np
import os
import time
import json
from glob import glob
import fire
import random
from ehe import Paragraf

# colorama autoreset
init(autoreset=True)


def pembagi(l, n):
    """ slicer list, l --> berapa element dalam n part """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def main(list_of_links, sumber, nama_file, n_jobs=25):
    if not os.path.exists(f'hasil/{sumber}'):
        os.makedirs(f'hasil/{sumber}')
    list_of_links = [l for l in list_of_links if 'money' not in l]
    list_of_links = np.asarray([l for l in list_of_links if 'lifestyle' not in l])
    berita = Paragraf()
    print(f'{Fore.CYAN}getting ', len(list_of_links))
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
            print(f'{Back.RED}sumber belum ditentukan')
            raise ValueError

        p.terminate()
        p.join()
        with open(f'hasil/{sumber}/{nama_file}___dump_parallel_hasil.json', "a+") as f:
            json.dump(hasil, f, indent=4, sort_keys=True, default=str)


def run(sumber:str, path_to_txt:str, chunks:int=100):
    """ sumber: berita, path_to_txt: txt file with link per line, chunks: saving every n_th chunk
        will dump to .json with part number, then aggregate after finished
    """
    berita_c = np.asarray(
        list(pembagi(open(path_to_txt).read().splitlines(), chunks)))
    for i, link in enumerate(berita_c):
        file_name = f'{i}_{sumber}'
        print(f'part {i}/{len(berita_c)}')
        time.sleep(random.randint(5, 29))
        main(link, sumber=sumber, nama_file=file_name)
        time.sleep(random.randint(10, 60))
    print(f'{Fore.GREEN}finished\n\n\n\n')
    print(f'{Fore.CYAN}now aggregating json files')
    json_aggregator(sumber)


def json_aggregator(sumber:str):
    """
    aggregate a list of json files inside a directory
     """
    json_path = f'hasil/{sumber}/*__*.json'
    berita_json = glob(json_path)

    berita = []
    for file in berita_json:
        try:
            with open(file) as f:
                berita.append(json.load(f))
        except Exception as e:
            print(f"{Fore.RED}{str(e)}")
            pass

    if not os.path.exists(f'hasil/{sumber}'):
        os.makedirs(f'hasil/{sumber}')
    berita = [sub for i in berita for sub in i]
    with open(f'hasil/{sumber}.json', 'w+') as f:
        json.dump(berita, f, indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    fire.Fire(run)
