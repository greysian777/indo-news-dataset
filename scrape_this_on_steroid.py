"""
WARM ON A COLD NIGHT!
"""
import pandas as pd
from ehe import pull_paragraf, pull_source
from pertanggalan import file_name
import os
import threading
import fire


def half_links(list_of_links):
    half = len(list_of_links)//2
    return list_of_links[:half], list_of_links[half:]


def generate_paragraphs(links: list, file_name=file_name):
    """
    made a csv of paragraphs from a csv of links, where the csv must have a header of 'links'
    """
    p_source = pd.DataFrame()
    for i, link in enumerate(links):
        print(f'getting par of {link}')

        try:
            p = pull_paragraf(link)
        except Exception as e:
            time.sleep(60)
            p = None
            pass

        df_ = pd.Series([link, p])
        df__ = p_source.append(df_, ignore_index=True)
        df__.to_csv(f'csv/berhasil_{file_name}_p.csv', mode='a')
        print(f'done {i}/{len(links)}')

def main(path_to_csv): 
    df = pd.read_csv(path_to_csv)
    df.dropna(inplace=True)
    a,b=half_links(df.links.values)
    return a,b


if __name__ == "__main__":
    fire.Fire()
