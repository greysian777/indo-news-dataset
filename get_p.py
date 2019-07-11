import pandas as pd
from ehe import pull_paragraf, pull_source
import time


df = pd.read_csv('berhasil_2019.csv')
df1 = pd.read_csv('KOMPAS 2018.csv')
df.columns = ['0', 'judul', 'image', 'link', 'tanggal']
links = df.link

p_source = pd.DataFrame()
for i, link in enumerate(links):
    print(f'getting par of {link}')
    try:
        p = pull_paragraf(link)
        html = pull_source(link)
    except:
        time.sleep(60)
        p, html = None, None
        pass
    df_ = pd.Series([link, p, html])
    df__ = p_source.append(df_, ignore_index=True)
    df__.to_csv('KOMPAS 2019_p_dan_source.csv', mode='a')
    print(f'done {i}/{len(links)}')
