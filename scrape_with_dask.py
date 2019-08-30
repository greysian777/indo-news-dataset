import dask
import pandas as pd
import dask.dataframe as ddf
import time
from ehe import USER_AGENTS as user_agent_list
import requests
import fire
import random
from bs4 import BeautifulSoup

def generate_single_paragraph(link): 
    return {'p':pull_paragraf_kompas(link),'link':link}

def pull_paragraf_kompas(link=None):
    headers = {'User-Agent': f'{random.choice(user_agent_list)}'}
    r = requests.get(link, headers=headers)
    s = BeautifulSoup(r.content, 'lxml')
    reader = s.find('div', {'class': 'read__content'})
    if 'MAAF KAMI TIDAK MENEMUKAN HALAMAN YANG ANDA CARI' in s.text:
        return '404'
    elif type(reader) == type(None):
        reader = s.find('div', {'class': 'main-artikel-paragraf'})
    elif 'jeo' in link:
        print('jeo link')
        return 'JEO TYPED SHIT'
    else:
        for child in reader.find_all("strong"):
            child.decompose()
    return(reader.get_text())


from dask.distributed import Client
client = Client()
print(client)

def get_csv(path_to_csv)
    df = pd.read_csv('path_to_csv')
    if 'links' in df.columns: 
        links = list(df.links)
        return list(df.links)
    else: 
        print('no "links" in columns.')
        sabi=('insert directory csv with "links" columns: \n>')
        get_csv(sabi)

def daskifier(list_of_links):
    data = [dask.delayed(generate_single_paragraph)(link) for link in links]
    dd = dask.delayed(pd.DataFrame)(data)
    dasked = ddf.from_delayed(dd)
    dasked.to_csv('csv/berahasil-*.csv')

def main(path_to_csv): 
    daskifier(get_csv(path_to_csv))

if __name__ == "__main__":
    fire.Fire(daskifier)