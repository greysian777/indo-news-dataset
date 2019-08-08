#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pertanggalan import generate_n_days_from_today, file_name
import requests
import pandas as pd
import time
import os
import random
from datetime import date


df = pd.DataFrame()
file_name = date.today().strftime("%Y-%m-%d")

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

class Berita(object):
    self.berita = {}

    def masuk_dict(self, judul, link, sumber, tanggal): 
        self.berita['judul'] = judul
        self.berita['link'] = link
        self.berita['sumber'] = sumber
        self.berita['tanggal'] = tanggal
        return self.berita

def pull_link_kontan(link, list_of_date, name, pagination=50):
    # TODO:
    # scrape-> judul:list, link:list, tanggal:list 
    # bikin list of dict, yaitu judul, link, tanggal
    # return Berita.berita(): dataframe
    pass

def pull_link_tempo(link, list_of_date, name, pagination=50): 
    pass

def pull_link_kompas(link, list_of_date, name, pagination=50):
    try:
        for date_current in list_of_date:
            for j in range(1, pagination):
                dict_ = {}
                url = link + str(date_current) + '/' + str(j)
                print(url)

                # Get article from website
                headers = {'User-Agent': f'{random.choice(user_agent_list)}'}
                req = requests.get(url, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')

                try:
                    container = soup.find(
                        'div', attrs={'class': 'latest--indeks mt2 clearfix'})

                except:
                    print('container not found')
                    print('will sleep for 30 seconds...')
                    time.sleep(30)
                    continue

                try:
                    boxes = container.find_all(
                        'div', attrs={'class': 'article__list clearfix'})
                except:
                    print('box not found')
                    print('will sleep for 30 seconds...')
                    time.sleep(30)
                    continue

                for i in range(0, len(boxes)):
                    box = container.find_all(
                        'div', attrs={'class': 'article__list clearfix'})[i]
                # Get Title Article
                    try:
                        title = box.find('h3').text
                    except:
                        print('h2.text not found')
                        break

                    # Get Image
                    try:
                        image = box.find('img').get('src')
                    except:
                        print('image not found')
                        break

                    # Get URL Article
                    try:
                        linknya = box.find('a').get('href')
                    except:
                        print('href not found')
                        break

                    # Get Date
                    date = date_current
                    # print(title, image, url)

                    if 'jeo' in linknya:
                        print('ada jeo')
                        pass
                    else:
    return self.berita                        dict_['image'] = image
                        dict_['links'] = linknya
                        dict_['date'] = date
                    df_ = pd.Series(dict_)
                    df1 = df.append(df_, ignore_index=True)
                    if not os.path.exists('csv/'):
                        os.makedirs('csv/')
                    df1.to_csv(f'csv/berhasil_{name}.csv', mode='a')
            print(date_current)
        return "done"
    except:
        pass


def pull_source(link=None):
    if not 'jeo' in link:
        headers = {'User-Agent': f'{random.choice(user_agent_list)}'}
        r = requests.get(link, headers=headers)
        s = BeautifulSoup(r.content, 'lxml')
        return (s.prettify())
    else:
        print('jeo detected')
        pass


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


def get_latest_date(path_to_csv):
    # assuming with the format of berhasil_2019.csv
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


def main():
    pull_link_kompas('https://indeks.kompas.com/all/',
                     generate_n_days_from_today(7), name=file_name)



if __name__ == "__main__":
    main()
