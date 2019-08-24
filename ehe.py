#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pertanggalan import generate_n_days_from_today
import requests
import pandas as pd
import time
import os
import random
from datetime import date


USER_AGENTS = open('user_agent.txt').read().splitlines()
headers = {
    'User-Agent': f'{random.choice(USER_AGENTS)}'}
df = pd.DataFrame()
FILE_NAME = date.today().strftime("%Y-%m-%d")


class Link():
    def __init__(self, list_of_date, sumber, pagination=50):
        self.pagination = pagination
        self.list_of_date = list_of_date
        self.sumber = sumber
        if not os.path.exists('csv/') and not os.path.exists('json/'):
            os.makedirs('csv/')
            os.makedirs('json/')

    def masukkan_link_ke_df(self, list_of_links):
        """ unpack list of list the returns it as a df, depends on sumber news """
        list_of_links = [l for item in list_of_links for l in item]
        list_of_dicts = []
        for link in list_of_links:
            kumpulan_info = {}
            kumpulan_info['links'] = link
            kumpulan_info['sumber'] = self.sumber
            list_of_dicts.append(kumpulan_info)
        print(list_of_dicts)
        df = pd.DataFrame(list_of_dicts)
        return df

    def pull_link_bisnis(self):
        list_of_links = []
        for current_date in self.list_of_date:
            current_date = current_date.strftime('%d+%B+%Y')
            for j in range(self.pagination+1):
                kumpulan_info = {}
                link = f'https://www.bisnis.com/index?c=5&d={current_date}&per_page={j}'
                print(link)
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                box = soup.find('ul', class_='l-style-none')
                if box.find('h2') is not None:
                    print('no more berita')
                    break
                links = list(
                    set([a['href'] for a in box.find_all('a') if len(a['href']) > 55]))
                list_of_links.append(links)
        return self.masukkan_link_ke_df(list_of_links)

    def pull_link_tempo(self):
        # https://www.tempo.co/indeks/2019/08/13
        list_of_links = []
        for current_date in self.list_of_date:
            current_date = current_date.strftime('%Y/%m/%d')
            link = f'https://www.tempo.co/indeks/{current_date}'
            req = requests.get(link)
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('ul', class_='wrapper')
            links = list(set([a['href'] for a in box.find_all('a')]))
            list_of_links.append(links)
        return self.masukkan_link_ke_df(list_of_links)

    def pull_link_detik(self):
        # https://news.detik.com/indeks/all/{page_number}?date={08}}/{month}/{year}}
        list_of_links = []
        for current_date in self.list_of_date:
            d, m, y = current_date.strftime('%d'), current_date.strftime(
                '%m'), current_date.strftime('%Y')
            for page_number in range(self.pagination+1):
                try:
                    link = f'https://news.detik.com/indeks/all/{page_number}?date={d}/{m}/{y}'
                    print(link)
                    header = {
                        'User-Agent': f'{random.choice(USER_AGENTS)}'}
                    req = requests.get(link)
                    soup = BeautifulSoup(req.content, 'lxml')
                    box = soup.find('ul', {'id': 'indeks-container'})
                    links = list(set([a['href'] for a in box.find_all('a')]))
                    list_of_links.append(links)

                except Exception as e:
                    print('error', str(e))
        return self.masukkan_link_ke_df(list_of_links)

    def pull_link_kompas(self):
        list_of_links = []
        for date_current in self.list_of_date:
            for j in range(1, self.pagination):
                url = f'https://indeks.kompas.com/all/{str(date_current)}/{j}'
                print(url)
                headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
                req = requests.get(url, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                if soup.find('a', class_='article__link'):
                    pass
                else:
                    print('halaman terakhir')
                    break
                box = soup.find('div', class_='latest--indeks mt2 clearfix')
                links = list(set([a['href']
                                  for a in box.find_all('a')]))
                list_of_links.append(links)
        return self.masukkan_link_ke_df(list_of_dict)

    def run(self):
        if self.sumber.lower() == 'kompas':
            return self.pull_link_kompas()
        elif self.sumber.lower() == 'detik':
            return self.pull_link_detik()
        elif self.sumber.lower() == 'tempo':
            return self.pull_link_tempo()
        elif self.sumber.lower() == 'bisnis':
            return self.pull_link_bisnis()
        else:
            print('sumber tidak jelas, dick stuck.')


class Paragraf:
    def __init__(self, csv, parallel=False):
        self.csv = csv
        self.parallel = parallel
        self.df = self.df_cleaner(self.csv)

    def df_cleaner(self, csv=self.csv, kasih_judul=False):
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

    def berita_template(self, judul, tanggal_berita, paragraf, tanggal_scraped=date.today()):
        template = {
            'judul': judul,
            'tanggal_berita': tanggal_berita,
            'tanggal_scraped': tanggal_scraped,
            'paragraf': paragraf
        }
        return template

    def get_kompas(self):
        r = requests.get(self.link, headers=headers)
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

    def get_tempo(self):
        r = requests.get(self.link)
        s = BeautifulSoup(r.content, 'lxml')
        box = s.find('div', {'itemprop': 'articleBody'})
        # get paragraf
        paragraf = [x.text.strip() for x in box.find_all('p')]
        # get date
        tanggal_berita = s.find('span', class_='date').text
        # get title
        judul = s.find('h1', {'itemprop': headline}).text
        # masukkin semua ke dalam dictionary
        return self.berita_template(judul, tanggal_berita, paragraf=paragraf)

    def get_detik(self):
        """ seluruh link harus ada '/' di belakangnya."""
        if self.link[-] is not '/':
            print('link harus mempunyai "/" di char terakhir.\n\n\nmenambahkan...')
            self.link = self.link + '/'
        else:
            pass

        r = requests.get(self.link)
        s = BeautifulSoup(r.content, 'lxml')
        last_page = s.find('div', class_='mid_multi').text.split('/')[-1]
        print(f'getting {int(last_page)} pages\n\n\n')
        kumpulan_paragraf = []
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

    def get_bisnis(self):
        r = requests.get(self.link)
        soup = BeautifulSoup(r.content, 'lxml')
        box = soup.find('div', class_='col-sm-10')
        desc = soup.find('div',class_='new-description')
        tanggal_berita = desc.find('span').text.strip().split('|')[0]
        judul = soup.find('h1').text.strip()
        paragraf = " ".join([p.text for p in box.find_all('p') if 'simak berita' not in p.text.lower()])
        return self.berita_template(judul, tanggal_berita, paragraf)

def remove_punctuation(kata):
    return kata.translate(None, string.punctuation)
