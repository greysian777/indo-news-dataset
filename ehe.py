#!/usr/bin/env python3

from colorama import Fore, init, Back
from bs4 import BeautifulSoup
from datetime import date
from typing import List, Dict, Text
import numpy as np
from typing import List
import pandas as pd
from tqdm import tqdm
import requests
import time
import os
import random

init(autoreset=True)
USER_AGENTS: List[Text] = open('user_agent.txt').read().splitlines()
headers = {
    'User-Agent': f'{random.choice(USER_AGENTS)}'}
FILE_NAME: Text = date.today().strftime("%Y-%m-%d")


class Link():
    def __init__(self, list_of_date: List[Text], sumber: Text, pagination=50, txt_mode=True):
        self.pagination = pagination+1
        self.list_of_date = np.asarray(list_of_date)
        self.sumber = sumber
        self.txt_mode = txt_mode
        if not os.path.exists('hasil/') and not os.path.exists('links/'):
            os.makedirs('hasil/')
            os.makedirs('links/')

    def parse_pagination(self, link):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
        last_page = soup.find(
            'a', class_='paging__link paging__link--prev')['data-ci-pagination-page']
        if last_page is None:
            return 50
        else:
            return int(last_page)

    def pull_link_bisnis(self) -> None:
        for current_date in tqdm(self.list_of_date, desc='links scraped'):
            current_date = current_date.strftime('%d+%B+%Y')
            for j in range(self.pagination+1):
                link = f'https://www.bisnis.com/index?c=5&d={current_date}&per_page={j}'
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                box = soup.find('ul', class_='l-style-none')
                if box.find('h2') is not None:
                    break
                links = list(
                    set([a['href'] for a in box.find_all('a') if len(a['href']) > 55]))
                with open(f'links/{self.sumber}_links.txt', 'a') as f:
                    for link in links:
                        f.writelines(link+'\n')
        print(f'{Back.GREEN}save ke txt berhasil')

    def pull_link_tempo(self) -> None:
        for current_date in tqdm(self.list_of_date, desc='links saved'):
            current_date = current_date.strftime('%Y/%m/%d')
            link = f'https://www.tempo.co/indeks/{current_date}/bisnis'
            req = requests.get(link)
            soup = BeautifulSoup(req.content, 'lxml')
            box = soup.find('ul', class_='wrapper')
            links = list(set([a['href'] for a in box.find_all('a')]))
            with open(f'links/{self.sumber}_links.txt', 'a') as f:
                for link in links:
                    f.writelines(link+'\n')
        print(f'{Back.GREEN}berhasil save txt')

    def pull_link_detik(self) -> None:
        # https://news.detik.com/indeks/all/{page_number}?date={08}}/{month}/{year}}
        for current_date in tqdm(self.list_of_date, desc='links saved'):
            d, m, y = current_date.strftime('%d'), current_date.strftime(
                '%m'), current_date.strftime('%Y')
            try:
                link = f'https://finance.detik.com/indeks?date={d}%2F{m}%2F{y}'
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                links = list(set([artikel.div.a['href']
                                  for artikel in soup.find_all('article') if 'foto-bisnis' not in artikel.div.a['href']]))
                with open('links/detik_links.txt', 'a') as f:
                    for link in links:
                        f.writelines(link+'\n')
            except Exception as e:
                print(f'{Fore.RED}error', str(e))
        print(f'{Fore.GREEN}berhasil save ke txt')

    def get_all_link_kompas(self) -> List[str]:
        hasil = []
        for i, date_current in enumerate(self.list_of_date):
            print(f'{Back.CYAN}{i}/{len(self.list_of_date)}')
            url = f'https://indeks.kompas.com/?site=all&date={date_current}'
            page_count = self.parse_pagination(url)
            for j in tqdm(range(1, page_count), desc='page'):
                url = f'https://indeks.kompas.com/?site=all&date={date_current}&page={j}'
                hasil.append(url)
        return hasil

    def run_one_link_kompas(self, link_kompas: str) -> List[str]:
        headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
        req = requests.get(link_kompas, headers=headers)
        soup = BeautifulSoup(req.content, 'lxml')
        box = soup.find('div', class_='latest--indeks mt2 clearfix')
        try:
            links = list(set([a['href']
                                for a in box.find_all('a') if 'travel' not in a['href']]))
        except:
            print(f'{Fore.RED}failed')
        return links


    def pull_link_kompas(self) -> None:
        for i, date_current in enumerate(self.list_of_date):
            print(f'{Back.CYAN}{i}/{len(self.list_of_date)}')
            url = f'https://indeks.kompas.com/?site=all&date={date_current}'
            page_count = self.parse_pagination(url)
            for j in tqdm(range(1, page_count), desc='page'):
                url = f'https://indeks.kompas.com/?site=all&date={date_current}&page={j}'
                headers = {'User-Agent': f'{random.choice(USER_AGENTS)}'}
                req = requests.get(url, headers=headers)
                soup = BeautifulSoup(req.content, 'lxml')
                if soup.find('a', class_='article__link'):
                    pass
                else:
                    break
                box = soup.find('div', class_='latest--indeks mt2 clearfix')
                try:
                    links = list(set([a['href']
                                      for a in box.find_all('a') if 'travel' not in a['href']]))
                except:
                    print(f'{Fore.RED}failed')
                    continue
                with open(f'links/{FILE_NAME}_kompas_links.txt', 'a+') as f:
                    for link in links:
                        f.writelines(link+'\n')
        print(f'{Fore.GREEN}berhasil save txt')

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
            print(f'{Back.RED}sumber tidak jelas, dick stuck.')


class Paragraf:
    def __init__(self, csv=None, txt_mode=True, parallel=False):
        self.csv = csv
        self.parallel = parallel
        self.txt_mode = txt_mode

    def run(self, save_to_folder, txt_path=None):
        """ single threading scraping paragraphs of a txt full of links """
        if self.txt_mode:
            list_of_links = open(txt_path).read().splitlines()
            self.sumber = txt_path.split('.')[0].split('/')[-1].split('_')[0]
            print(f'{Back.GREEN}{self.sumber}')
        else:
            print(f'{Back.RED}you need to specify the list of links')

        _FILE_NAME = save_to_folder+f'{FILE_NAME}_{self.sumber}_p.csv'
        print(f'{Fore.CYAN}get {len(list_of_links)} links')
        save_df = pd.DataFrame(
            columns=['judul',  'tanggal_berita', 'paragraf', 'tanggal_scraped'])
        for link in tqdm(list_of_links, desc='links scraped'):
            try:
                if self.sumber == 'kompas' or self.sumber == 'kompas_finansial':
                    series = pd.Series(self.get_kompas(link))
                elif self.sumber == 'detik':
                    series = pd.Series(self.get_detik(link))
                elif self.sumber == 'bisnis':
                    series = pd.Series(self.get_bisnis(link))
                elif self.sumber == 'tempo':
                    series = pd.Series(self.get_tempo(link))
                else:
                    print(f'{Back.RED}sumber is not recognized, dick stuck')
                    os._exit()
                save_df = save_df.append(series, ignore_index=True)
                save_df.to_csv(_FILE_NAME, mode='a', header=False)
            except Exception as e:
                print(f'{Fore.RED}error on link {link}')
                print(str(e))
                continue
        save_df.to_csv(_FILE_NAME)
        print(f'{Fore.GREEN}sukses mengambil semua paragraf di {_FILE_NAME}')

    def berita_template(self, judul, tanggal_berita, paragraf, tanggal_scraped=date.today(), link=None) -> Dict:
        """ dictionary template for berita """
        template = {
            'judul': judul,
            'tanggal_berita': tanggal_berita,
            'tanggal_scraped': tanggal_scraped,
            'paragraf': paragraf,
            'link': link
        }
        return template

    def get_kompas(self, link: Text) -> Dict:
        """ returns a dictionary of kompas news """
        r = requests.get(link, headers=headers)
        s = BeautifulSoup(r.content, 'lxml')
        reader = s.find('div', {'class': 'read__content'})
        try:
            if 'maaf' in s.text.lower():
                return None
            elif type(reader) == type(None):
                reader = s.find('div', {'class': 'main-artikel-paragraf'})
                par = ' '.join([p.text for p in reader.find_all(
                    'p') if 'Baca juga' not in p.text])
            elif 'jeo' in link.split('/'):
                print(f'{Back.RED}jeo link')
                return None
            else:
                par = ' '.join([p.text for p in reader.find_all(
                    'p') if 'Baca juga' not in p.text])
            tanggal_berita = s.find(
                'div', class_="read__time").text.split('-')[-1].strip()
            judul = s.find("h1").text.strip()
        except Exception as e:
            print(str(e))
            print(f'{Back.RED}{link}')
            return None
        return self.berita_template(judul, tanggal_berita, par, link=link)

    def get_tempo(self, link: Text) -> Dict:
        """ returns a dictionary of tempo article """
        r = requests.get(link)
        s = BeautifulSoup(r.content, 'lxml')
        box = s.find('div', {'itemprop': 'articleBody'})
        paragraf = [x.text.strip() for x in box.find_all('p')]
        tanggal_berita = s.find('span', {'itemprop': 'datePublished'}).text
        judul = s.find('h1', {'itemprop': 'headline'}).text
        return self.berita_template(judul, tanggal_berita, paragraf, link=link)

    def get_detik(self, link):
        """ returns a dictionary of detik article """
        r = requests.get(link)
        s = BeautifulSoup(r.content, 'lxml')
        kumpulan_paragraf = []
        try:
            last_page = s.find('div', class_='mid_multi').text.split('/')[-1]
        except AttributeError:
            r = requests.get(link)
            s = BeautifulSoup(r.content, 'lxml')
            box = s.find('div', class_='itp_bodycontent detail_text')
            kumpulan_paragraf.append(box.text)
        except:
            print(f'{Fore.CYAN}getting {int(last_page)} pages\n\n\n')
            for i in range(2, int(last_page)+1):
                print(f'{Fore.CYAN}{i} / {last_page}')
                r = requests.get(link+f'{i}')
                s = BeautifulSoup(r.content, 'lxml')
                box = s.find('div', class_='itp_bodycontent detail_text')
                par = box.find("p")
                kumpulan_paragraf.append(par.text.strip())
        paragraf = ' '.join(kumpulan_paragraf)
        tanggal_berita = s.find('div', class_='date').text.strip()
        judul = s.find('h1').text.strip()
        return self.berita_template(judul, tanggal_berita, paragraf, link=link)

    def get_bisnis(self, link: Text) -> Dict:
        """ returns a dictionary of bisnis article """
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
        box = soup.find('div', class_='col-sm-10')
        desc = soup.find('div', class_='new-description')
        tanggal_berita = desc.find('span').text.strip().split('|')[0]
        judul = soup.find('h1').text.strip()
        paragraf = " ".join([p.text for p in box.find_all(
            'p') if 'simak berita' not in p.text.lower()])
        return self.berita_template(judul, tanggal_berita, paragraf, link=link)
