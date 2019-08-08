#!/usr/bin/env pipenv run python
"""
WARM ON A COLD NIGHT!
"""
import pandas as pd
from ehe import pull_paragraf_kompas, pull_source
from pertanggalan import file_name
import os
import threading
import fire
import time

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
            p = pull_paragraf_kompas(link)
        except Exception as e:
            time.sleep(60)
            p = None
            pass

        df_ = pd.Series([link, p])
        df__ = p_source.append(df_, ignore_index=True)
        df__.to_csv(f'csv/berhasil_{file_name}_p.csv', mode='a', index=False)
        print(f'done {i}/{len(links)}')

def merger(csv1: pd.DataFrame, csv2: pd.DataFrame):
    if csv1.columns == csv2.columns:
        df = pd.concat([csv1, csv2])
        if not df.isnull().values.any():
            return df
    else:
        print('dataframe doesn\'t have the same column names.')
        col_title = []
        print('csv1: \n', csv1.head(5))
        print('csv2: \n', csv2.head(5))
        for a1, a2 in zip(csv1, csv2): 
            if a1=='Unnamed: 0': 
                csv1.drop([a1], axis=1, inplace=True)
            elif a2=='Unnamed: 0':
                csv2.drop([a2], axis=1, inplace=True)
            col_title.append(input('title: \n'))
        csv1.columns = col_title
        csv2.columns = col_title
        merger(csv1, csv2)
        

def main(path_to_csv): 
    df = pd.read_csv(path_to_csv)
    df.dropna(inplace=True)
    a,b=half_links(df.links.values)
    return a,b


if __name__ == "__main__":
    fire.Fire()
