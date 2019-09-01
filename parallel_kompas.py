#!/usr/bin/env python3

from ehe import Paragraf
from multiprocessing import Pool
import json 
from tqdm import tqdm
import time 
import json
import fire


def pembagi(l, n): 
    for i in range(0, len(l), n): 
        yield l[i:i+n]


def main(list_of_links,name, n_jobs = 7): 
    berita = Paragraf()
    print('getting ',len(list_of_links))

    with Pool(n_jobs) as p :
        try: 
            hasil = list(tqdm(p.imap(berita.get_kompas, list_of_links), total=len(list_of_links)))
        except Exception as e: 
            print(str(e))
        finally: 
            p.terminate()
            p.join()
            with open(f'csv/{name}___dump_kompas_parallel_hasil.json', "a+") as f: 
                json.dump(hasil, f,indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
    kompas = open('json/kompas_sisa.txt').read().splitlines()
    kl = list(pembagi(kompas, 700))
    for j in kl: 
        print(len(j))
    for i,link in enumerate(kl): 
        print(f'part {i}')
        main(link, i)