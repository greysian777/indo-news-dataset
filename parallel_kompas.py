#!/usr/bin/env python3

from ehe import Paragraf
from multiprocessing import Pool
import json 
import time 
import dask


kompas_links = open('json/kompas_links.txt').read().splitlines()
print(f'ada {len(kompas_links)} link')

if __name__ == "__main__":
    start = time.time()
    kompas = Paragraf()
# parallel
    print('starting multi process')
    p = Pool(20)
    hasil = p.map(kompas.get_kompas, kompas_links)
    p.terminate()
    p.join()
    print(f'berhasil scraping dalam waktu {time.time() - start}')

    start = time.time()
    with open('json/dump_kompas_parallel_hasil.json', "a+") as f: 
        json.dump(hasil, f,indent=4, sort_keys=True, default=str)
    print(f'berhasil dumps dalam waktu {time.time() - start}')

# using dask 
    print("starting dask")
    start = time.time()
    data = [dask.delayed(kompas.get_tempo)(link) for link in kompas_links]
    data = dask.compute(data)
    print(f'berhasil scraping pake dask dalam waktu {time.time() - start}')
    start = time.time()
    with open('json/dump_kompas_dask_hasil.json', "a+") as f: 
        json.dump(data, f,indent=4, sort_keys=True, default=str)
    print(f'berhasil dumps dalam waktu {time.time() - start}')
    

# single
    print('starting 1 thread process')
    data = []
    start = time.time()
    for link in kompas_links: 
        data.append(kompas.get_tempo(link))
    with open('json/dumps_kompas_serial_hasil.json', "a+") as f: 
        json.dump(hasil,f , indent=4, sort_keys=True, default=str)
    print(f'berhasil dump dalam waktu {time.time() - start}')

    
