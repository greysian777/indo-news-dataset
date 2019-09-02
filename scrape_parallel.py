#!/usr/bin/env python3

from ehe import Paragraf
from multiprocessing import Pool
import json
from tqdm import tqdm
import time
import json
import fire
import random


def pembagi(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def main(list_of_links,sumber, nama_file, n_jobs =25):
    berita = Paragraf()
    print('getting ',len(list_of_links))

    with Pool(n_jobs) as p :
        if sumber == 'kompas':
            hasil = list(tqdm(p.imap(berita.get_kompas, list_of_links), total=len(list_of_links)))
        elif sumber == 'detik':
            hasil = list(tqdm(p.imap(berita.get_detik, list_of_links), total=len(list_of_links)))
        elif sumber == 'tempo':
            hasil = list(tqdm(p.imap(berita.get_tempo, list_of_links), total=len(list_of_links)))
        elif sumber == 'bisnis':
            hasil = list(tqdm(p.imap(berita.get_bisnis, list_of_links), total=len(list_of_links)))
        else:
            print('sumber belum ditentukan')
            raise ValueError


        p.terminate()
        p.join()
        with open(f'csv/{nama_file}___dump_parallel_hasil.json', "a+") as f:
            json.dump(hasil, f,indent=4, sort_keys=True, default=str)

def run(sumber, path_to_txt, chunks=100):
    berita = open(path_to_txt).read().splitlines()
    berita_c = list(pembagi(berita, chunks))
    for i, link in enumerate(berita_c):
        file_name=f'{i}_{sumber}'
        try:
            print(f'part {i}/{len(berita_c)}')
            time.sleep(random.randint(5,29))
            main(link, sumber=sumber ,nama_file=file_name)
        except Exception as e:
            print(str(e))
            time.sleep(random.randint(10,60))
            continue


if __name__ == "__main__":
    fire.Fire()