import dask.dataframe as dd
from ehe import pull_paragraf_kompas


#using dask dataframe
df = dd.read_csv('csv/berhasil_2019.csv')
test = df.to_delayed()
dd.to_json(df, 'json/berhasil_2019.json')

from dask.distributed import Client
aing = Client()

futures = aing.compute(test)