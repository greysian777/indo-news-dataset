#!/usr/bin/env python3

from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from tqdm import tqdm
import requests
import time
import os
import random
import json 


USER_AGENTS = open('user_agent.txt').read().splitlines()
headers = {
    'User-Agent': f'{random.choice(USER_AGENTS)}'}
df = pd.DataFrame()
FILE_NAME = date.today().strftime("%Y-%m-%d")


class Link():
    def __init__(self, list_of_date, sumber, pagination=50, txt_mode=True):
        self.pagination = pagination
        self.list_of_date = list_of_date
        self.sumber = sumber
        self.txt_mode = txt_mode
        if not os.path.exists('csv/') and not os.path.exists('json/'):
            os.makedirs('csv/')
            os.makedirs('json/')

    def pull_link_bisnis(self):
        list_of_links = []
        for current_date in tqdm(self.list_of_date, desc='links scraped'):
            current_date = current_date.strftime('%d+%B+%Y')
            for j in range(self.pagination+1):
                kumpulan_info = {}
                link = f'https://www.bisnis.com/index?c=5&d={current_date}&per_page={j}'
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                box = soup.find('ul', class_='l-style-none')
                if box.find('h2') is not None:
                    break
                links = list(
                    set([a['href'] for a in box.find_all('a') if len(a['href']) > 55]))
                with open(f'json/{self.sumber}_links.txt','a') as f : 
                    for link in links: 
                        # print(link)
                        f.writelines(link+'\n')
        print('save ke txt berhasil')

    def pull_link_tempo(self):
        for current_date in tqdm(self.list_of_date, desc='links saved'):
            current_date = current_date.strftime('%Y/%m/%d')
            link = f'https://www.tempo.co/indeks/{current_date}/bisnis'
            req = requests.get(link)
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('ul', class_='wrapper')
            links = list(set([a['href'] for a in box.find_all('a')]))
            with open(f'json/{self.sumber}_links.txt','a') as f : 
                for link in links: 
                    # print(link)
                    f.writelines(link+'\n')
        print('berhasil save txt')

    def pull_link_detik(self):
        print('rusak dari sananya. gak punya indeks yang baik dan benar ')
        break
        # https://news.detik.com/indeks/all/{page_number}?date={08}}/{month}/{year}}
        for current_date in tqdm(self.list_of_date, desc='links saved'):
            d, m, y = current_date.strftime('%d'), current_date.strftime(
                '%m'), current_date.strftime('%Y')
            try:
                link = f'https://finance.detik.com/indeks?date={d}%2F{m}%2F{y}'
                print(link)
                header = {
                    'User-Agent': f'{random.choice(USER_AGENTS)}'}
                req = requests.get(link)
                soup = BeautifulSoup(req.content, 'lxml')
                links = list(set([artikel.div.a['href'] for artikel in soup.find_all('article')]))
                with open('json/detik_links.txt','a') as f : 
                    for link in links: 
                        f.writelines(link+'\n')
            except Exception as e:
                print('error', str(e))
        print('berhasil save ke txt')

    def pull_link_kompas(self):
        for date_current in tqdm(self.list_of_date, desc='links scraped'):
            for j in range(1, self.pagination):
                url = f'https://indeks.kompas.com/all/{str(date_current)}/{j}'
                print(url)
                headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
                req = requests.get(url, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                if soup.find('a', class_='article__link'):
                    pass
                else:
                    break
                box = soup.find('div', class_='latest--indeks mt2 clearfix')
                links = list(set([a['href']
                                  for a in box.find_all('a')]))
                with open('json/kompas_links.txt', 'a+') as f: 
                    for link in links: 
                        f.writelines(link+'\n')
        print('berhasil save txt')
        

    def pull_link_kompas_finansial(self): 
        for j in tqdm(range(1, 9), desc='scraped'):
            url = f'https://www.kompas.com/tag/finansial/desc/{j}'
            headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('div', class_='latest--topic mt2 clearfix')
            links = list(set([a['href']
                                for a in box.find_all('a')]))
            with open('json/kompas_finansial_links.txt', 'a+') as f: 
                for link in links: 
                    f.writelines(link+'\n')
        print('berhasil save txt')

    def run(self):
        if self.sumber.lower() == 'kompas':
            return self.pull_link_kompas()
        elif self.sumber.lower() == 'detik':
            break
            return self.pull_link_detik()
        elif self.sumber.lower() == 'kompas_finansial':
            return self.pull_link_kompas_finansial()
        elif self.sumber.lower() == 'tempo':
            return self.pull_link_tempo()
        elif self.sumber.lower() == 'bisnis':
            return self.pull_link_bisnis()
        else:
            print('sumber tidak jelas, dick stuck.')


class Paragraf:
    def __init__(self, csv=None, txt_mode=False, parallel=False):
        self.csv = csv
        self.parallel = parallel
        if csv is None:
            print('initializing txt mode...')
            self.sumber = 'kompas_finansial' 
        else:
            self.df = self.df_cleaner(self.csv)
            self.sumber = csv.split('_')[-2]
        self.txt_mode = txt_mode

    def df_cleaner(self,kasih_judul=False):
        print(f'now cleaning {self.csv}')
        df = pd_read_csv(df)
        if not kasih_judul:
            df = df.drop(
                [x for x in df.columns if 'Unnamed' in x or 'index' in x], axis=1)
            df.to_csv(path_to_csv)
        else:
            df = df.drop([x for x in df.columns if 'Unnamed' in x], axis=1)
            print(df.head())
            print(f'terdapat {df.columns} sebagai judul')
            judul = [input(f'judul ke-{x}: \n>')
                     for x in range(len(df.columns))]
            df.columns = judul
            df.to_csv(path_to_csv, index=False)
        df = df.drop([x for x in df.columns if 'Unnamed' in x], axis=1)
        return df

    def get_links(self):
        return list(self.df.links)

    def run(self, save_to_folder, txt_path=None): 
        if self.txt_mode: 
            list_of_links = open(txt_path).read().splitlines()
            self.sumber = txt_path.split('.')[0].split('/')[-1].split('_')[0]
            print(self.sumber)
        else:
            list_of_links = self.get_links()
        _FILE_NAME = save_to_folder+f'{FILE_NAME}_{self.sumber}_p.csv'
        print(f'get {len(list_of_links)} links')
        save_df = pd.DataFrame(columns=['judul',  'tanggal_berita', 'paragraf', 'tanggal_scraped' ])
        for link in tqdm(list_of_links, desc='links scraped'):
            try: 
                if self.sumber == 'kompas' or self.sumber == 'kompas_finansial': 
                    series = pd.Series(self.get_kompas(link))
                elif self.sumber == 'detik': 
                    print('DETIK TIDAK MASUK')
                    break
                    series = pd.Series(self.get_detik(link))
                elif self.sumber == 'bisnis': 
                    series = pd.Series(self.get_bisnis(link))
                elif self.sumber == 'tempo': 
                    series = pd.Series(self.get_tempo(link))
                else: 
                    print('sumber is not recognized, dick stuck')
                    os._exit()
                save_df = save_df.append(series, ignore_index=True)
                save_df.to_csv(_FILE_NAME, mode='a', header=False)
            except Exception as e : 
                print(f'error on link {link}')
                print(str(e))
                continue
        save_df.to_csv(_FILE_NAME)
        print(f'sukses mengambil semua paragraf di {_FILE_NAME}')
    
    def run_dask(self, save_to_folder): 
        pass

    def berita_template(self, judul, tanggal_berita, paragraf, tanggal_scraped=date.today()):
        template = {
            'judul': judul,
            'tanggal_berita': tanggal_berita,
            'tanggal_scraped': tanggal_scraped,
            'paragraf': paragraf
        }
        return template

    def get_kompas(self, link: str) -> dict:
        r = requests.get(link, headers=headers)
        s = BeautifulSoup(r.content, 'lxml')
        reader = s.find('div', {'class': 'read__content'})
        if 'maaf' in s.text.lower():
            return None
        elif type(reader) == type(None):
            reader = s.find('div', {'class': 'main-artikel-paragraf'})
        elif 'jeo' in link:
            print('jeo link')
            return None
        else:
            for child in reader.find_all("strong"):
                child.decompose()
            par = reader.get_text()
        par = reader.text.strip()
        tanggal_berita = s.find(
            'div', class_="read__time").text.split('-')[-1].strip()
        judul = s.find("h1").text.strip()
        return self.berita_template(judul, tanggal_berita, par)

    def get_tempo(self, link):
        r = requests.get(link)
        s = BeautifulSoup(r.content, 'lxml')
        box = s.find('div', {'itemprop': 'articleBody'})
        # get paragraf
        paragraf = [x.text.strip() for x in box.find_all('p')]
        # get date
        tanggal_berita = s.find('span', class_='date').text
        # get title
        judul = s.find('h1', {'itemprop': 'headline'}).text
        # masukkin semua ke dalam dictionary
        return self.berita_template(judul, tanggal_berita, paragraf=paragraf)

    def get_detik(self, link):
        print('DETIK TIDAK MASUK')
        break
        r = requests.get(link)
        s = BeautifulSoup(r.content, 'lxml')
        kumpulan_paragraf = []
        last_page = s.find('div', class_='mid_multi').text.split('/')[-1]
        if type(last_page) is 'NoneType':
            r = requests.get(link)
            s = BeautifulSoup(r.content, 'lxml')
            box = s.find('div', class_='itp_bodycontent detail_text')
            kumpulan_paragraf.append(box.text)
        else:
            print(f'getting {int(last_page)} pages\n\n\n')
            for i in range(2, int(last_page)+1):
                print(f'{i} / {last_page}')
                r = requests.get(link+f'{i}')
                s = BeautifulSoup(r.content, 'lxml')
                box = s.find('div', class_='itp_bodycontent detail_text')
                par = box.find("p")
                kumpulan_paragraf.append(par.text.strip())
        paragraf = ' '.join(kumpulan_paragraf)
        tanggal_berita = s.find('div', class_='date').text.strip()
        judul = s.find('h1').text.strip()
        return self.berita_template(judul, tanggal_berita, paragraf)

    def get_bisnis(self,link):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
        box = soup.find('div', class_='col-sm-10')
        desc = soup.find('div', class_='new-description')
        tanggal_berita = desc.find('span').text.strip().split('|')[0]
        judul = soup.find('h1').text.strip()
        paragraf = " ".join([p.text for p in box.find_all(
            'p') if 'simak berita' not in p.text.lower()])
        return self.berita_template(judul, tanggal_berita, paragraf)

def remove_punctuation(kata):
    return kata.translate(None, string.punctuation)
