#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pertanggalan import generate_n_days_from_today, file_name
import requests
import pandas as pd
import time
import os
import random
from datetime import date


USER_AGENTS = open('user')
df = pd.DataFrame()
FILE_NAME = date.today().strftime("%Y-%m-%d")


class Berita(object):
    def __init__():
        self.berita = {}

    def masuk_dict(self, judul, link, sumber, tanggal):
        self.berita['judul'] = judul
        self.berita['link'] = link
        self.berita['sumber'] = sumber
        self.berita['tanggal'] = tanggal
        return self.berita


def pull_link_bisnis(list_of_date, file_name=FILE_NAME):
    # https://www.bisnis.com/index?c=&d=13+August+2019
    if not os.path.exists('csv/'):
        os.makedirs('csv/')
   for current_date in list_of_date: 
        current_date = current_date.strftime('%d+%B+%Y')
        for j in range(pagination+1):
            kumpulan_info = {}
            link = f'https://www.bisnis.com/index?c=&d={current_date}&per_page={j}'
            req = requests.get(link)
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('ul',class_='l-style-none')
            list_of_links = [a['href'] for a in box.find_all('a')]
            list_of_judul = [div.h2.text for div in box.find_all('div')]
            list_of_tanggals =[div.span.text.strip() for div in box.find_all('div')]
            kumpulan_info['links'] = list_of_links
            kumpulan_info['judul'] = list_of_juduls
            kumpulan_info['tanggal'] = list_of_tanggals
            kumpulan_info['sumber'] = 'bisnis'
            list_of_df.append(kumpulan_info)
        df = pd.DataFrame(list_of_df)
        df.drop_duplicates(inplace=True, keep='first')
        df.to_csv(f'csv/links_bisnis_{file_name}.csv', index=False)
    
 

def pull_link_tempo(list_of_date,file_name=FILE_NAME): 
    # https://www.tempo.co/indeks/2019/08/13
    if not os.path.exists('csv/'): 
        os.makedirs('csv/')
    list_of_df = []
    for current_date in list_of_date: 
        kumpulan_info = {}
        current_date = current_date.strftime('%Y/%m/%d')
        link = f'https://www.tempo.co/indeks/{current_date}'
        req = requests.get(link)
        soup = BeautifulSoup(req.content, 'lxml')
        box = soup.find('ul',class_='wrapper')
        list_of_links = list(set([a['href'] for a in box.find_all('a')]))
        list_of_tanggals = [a.text for a in box.find_all('span',class_='col')]
        list_of_judul = [a.text for a in box.find_all('h2',class_='title')]
        kumpulan_info['links'] = list_of_links
        kumpulan_info['judul'] = list_of_juduls
        kumpulan_info['tanggal'] = list_of_tanggals
        kumpulan_info['sumber'] = 'tempo'
        list_of_df.append(kumpulan_info)
    df = pd.DataFrame(list_of_df)
    df.to_csv(f'csv/links_tempo_{file_name}.csv', index=False)
       

def pull_link_detik(list_of_date, file_name=FILE_NAME , pagination=50):
    # https://news.detik.com/indeks/all/{page_number}?date={08}}/{month}/{year}}
    if not os.path.exists('csv/'):
        os.makedirs('csv/')
    list_of_df = []
    for current_date in list_of_date:
        d, m, y = current_date.strftime('%d'), current_date.strftime(
            '%m'), current_date.strftime('%Y')
            for page_number in range(pagination+1):
                try:
                    kumpulan_info = {}
                    link = f'https://news.detik.com/indeks/all/{page_number}?date={d}/{m}/{y}'
                    print(link)
                    header = {
                        'User-Agent': f'{random.choice(USER_AGENTS)}'}
                    req = requests.get(link)
                    soup = BeautifulSoup(req.content, 'lxml')
                    box = soup.find('ul', {'id': 'indeks-container'})
                    list_of_links = [a['href'] for a in box.find_all('a')]
                    list_of_juduls = [a.text for a in box.find_all('a')]
                    list_of_tanggals = [a.text for a in box.find_all(
                        'span') if 'wib' in a.text.lower()]
                    kumpulan_info['links'] = list_of_links
                    kumpulan_info['judul'] = list_of_juduls
                    kumpulan_info['tanggal'] = list_of_tanggals
                    kumpulan_info['sumber'] = 'detik'
                    list_of_df.append(kumpulan_info)
                except Exception as e:
                    print('error', str(e))
    df = pd.DataFrame(list_of_df)
    df.to_csv(f'csv/links_detik_{file_name}.csv', index=False)



def pull_link_kompas(link, list_of_date, file_name= FILE_NAME, pagination=50):
    if not os.path.exists('csv/'):
        os.makedirs('csv/')
    list_of_df = []
    for date_current in list_of_date:
        for j in range(1, pagination):
            kumpulan_info = {}
            url = f'https://indeks.kompas.com/all/{str(date_current)}/{j}'
            print(url)
            headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('div', class_='latest--indeks mt2 clearfix')
            # hack for not same element erere
            list_of_links = list(set([a['href'] for a in box.find_all('a')]))
            list_of_titles = [
                a.text for a in box.find_all('a') if len(a.text) > 2]
            list_of_tanggals = [a.text for a in box.find_all(
                'div', class_='article__date')]
            kumpulan_info['links'] = list_of_links
            kumpulan_info['judul'] = list_of_juduls
            kumpulan_info['tanggal'] = list_of_tanggals
            kumpulan_info['sumber'] = 'detik'
            list_of_df.append(kumpulan_info)]
    df = pd.DataFrame(list_of_df)
    df.to_csv(f'csv/links_kompas_{file_name}.csv', index=False)


def pull_paragraf_kompas(link=None):
    headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
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


def get_latest_date(path_to_csv):
    df = pd.read_csv(path_to_csv)
    df.dropna(inplace=True)
    return df.sort_values(by='date', ascending=False).iloc[0][-1]


def df_cleaner(path_to_csv, kasih_judul=False):
    df = pd.read_csv(path_to_csv)
    if not kasih_judul:
        df = df.drop([x for x in df.columns if 'Unnamed' in x], axis=1)

        df.to_csv(path_to_csv)
    else:
        df = df.drop([x for x in df.columns if 'Unnamed' in x], axis=1)

        print(df.head())
        print(f'terdapat {df.columns} sebagai judul')
        judul = [input(f'judul ke-{x}: \n>') for x in range(len(df.columns))]
        df.columns = judul
        df.to_csv(path_to_csv, index=False)
    df = df.drop([x for x in df.columns if 'Unnamed' in x], axis=1)
    return df
