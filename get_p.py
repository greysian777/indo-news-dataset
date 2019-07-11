import pandas as pd 
from ehe import user_agent_list, pull_source

tahun2018 = pd.read_csv('KOMPAS 2018.csv')
links = tahun2018.link

print(type(link))
