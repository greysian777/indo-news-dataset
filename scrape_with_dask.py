import dask
import pandas as pd
import dask.dataframe as ddf
from ehe import USER_AGENTS as user_agent_list
import fire

def generate_single_paragraph(link): 
    return {'p':pull_paragraf_kompas(link),'link':link}


from dask.distributed import Client

from ehe import Paragraf
import time


def daskifier():
    list_of_links = open('json/kompas_finansial_links.txt').read().splitlines()
    
    # showcase buat kompas doang 

    sumber = 'kompas' 
    berita = Paragraf()
    if sumber == 'kompas':
        start = time.time()
        data = [dask.delayed(berita.get_kompas)(link) for link in list_of_links]
    data = dask.compute(data)
    dat = [i for i in data[0]]
    df = pd.DataFrame(dat) 
    df.to_csv('ngentot.csv')
    # print(type(df))  
    print(f'time: {time.time() - start}')


def get_all_links(txt_path) -> list: 
    return open(txt_path).read().splitlines()


if __name__ == "__main__":
    client = Client()
    print(client)
    daskifier()
