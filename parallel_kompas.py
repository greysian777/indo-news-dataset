#!/usr/bin/env python3

from ehe import Paragraf
from multiprocessing import Pool
import json 
from tqdm import tqdm
import time 
import json

def main(txt_path, n_jobs = 7): 
    berita = Paragraf()
    links = open(txt_path).read().splitlines()
    links = list(set(links))
    print('getting ',len(links))
    sumber = txt_path.split('_')[1]
    print(sumber)

    with Pool(n_jobs) as p :
        try: 
            hasil = list(tqdm(p.imap(berita.get_kompas, links), total=len(links)))
        except: 
            pass
        finally: 
            p.terminate()
            p.join()
            with open('csv/dump_kompas_parallel_hasil.json', "a+") as f: 
                json.dump(hasil, f,indent=4, sort_keys=True, default=str)


if __name__ == "__main__":
        main('json/2019-09-01_kompas_links.txt')