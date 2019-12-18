from typing import List
import datetime
from tqdm import tqdm
import json
from pathlib import Path
from fire import Fire


def load_scraped_links(json_path: str) -> List[str]:
    """
    json file path, yang hasil scraped nya
    return a list of links that already been scraped
    """
    is_there = True
    the_file = Path(json_path)
    while is_there:
        if not the_file.is_file():
            print('file not found. please choose wisely')
            json_path = input('input directory here: ')
            is_there = Path(json_path).is_file()
        else:
            is_there = False

    data = json.loads(open(the_file).read())

    return [x['link'] for x in data if x]

def load_links_to_scrape(txt_path: str) -> List[str]:
    the_file = Path(txt_path)
    if the_file.is_file():
        return open(the_file).read().splitlines()
    else:
        print('txt of links cannot be located')

def reduce(sudah_scraped: List[str], belum_scraped: List[str]) -> List[str]:
    return list(set(sudah_scraped) ^ set(belum_scraped))

def main(sudah, belum):
    hasil = reduce(load_scraped_links(sudah), load_links_to_scrape(belum))
    nama = input('nama sumber berita\n>')
    nama = f'links/{nama}_links_not_scraped_{datetime.datetime.now().strftime("%m-%d-%Y")}.txt'
    with open(nama, 'a+') as f:
        for h in tqdm(hasil, desc='writing link'):
            f.writelines(f'{h}\n')
    print(f'done writing {nama}, happy scraping')
if __name__ == "__main__":
    Fire(main)
