import pandas as pd
from ehe import pull_paragraf, pull_source
import time
import os


df = pd.read_csv('berhasil_2019.csv')
df1 = pd.read_csv('KOMPAS 2018.csv')
df.columns = ['judul', 'image', 'link', 'tanggal']
links = df.link
links = links[31499:]

p_source = pd.DataFrame()
for i, link in enumerate(links):
    print(f'getting par of {link}')     
    try:
        p = pull_paragraf(link)
#         html = pull_source(link)
    except Exception as e: 
        time.sleep(60)
        p = None
        pass
    if i % 500 == 0 and i != 1 : 
        print('-- UPLOAD TIME -- \n\n\n\n\n')
        os.system('python3 pusher.py')
    
   
    df_ = pd.Series([link, p])
    df__ = p_source.append(df_, ignore_index=True)
    df__.to_csv('KOMPAS_2019_p.csv', mode='a')
    print(f'done {i}/{len(links)}')
os.system('python3 pusher.py')