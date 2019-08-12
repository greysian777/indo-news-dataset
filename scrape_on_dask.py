import dask
import pandas as pd
from scrape_this_on_steroid import generate_single_paragraph
import time

from dask.distributed import Client
client = Client()
print(client)
# using dask dataframe
df = pd.read_csv('csv/berhasil_2019.csv')
links = list(df.links)
links = links[:100]

start = time.time()
data = [dask.delayed(generate_single_paragraph)(link) for link in links]
dd = dask.delayed(pd.DataFrame)(data)
dd.compute()
print(f'{time.time() - start}')