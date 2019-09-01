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


def main(list_of_links,name, n_jobs =25): 
    berita = Paragraf()
    print('getting ',len(list_of_links))

    with Pool(n_jobs) as p :
        hasil = list(tqdm(p.imap(berita.get_bisnis, list_of_links), total=len(list_of_links)))
        p.terminate()
        p.join()
        with open(f'csv/{name}___dump_bisnis_parallel_hasil.json', "a+") as f: 
            json.dump(hasil, f,indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    kompas = open('json/bisnis_links.txt').read().splitlines()
    kl = list(pembagi(kompas, 100))
    for j in kl: 
        print(len(j))
    for i,link in enumerate(kl): 
        try:
            print('sudah pakai print')
            print(f'part {i}/{len(kl)}')
            time.sleep(random.randint(5,29))
            main(link, i)
        except:
            continue
