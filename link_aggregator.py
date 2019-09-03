import json 
import glob, os

kl = open('json/kompas_sisa.txt').read().splitlines()
contents = []
json_dir = "csv/"

json_pattern = os.path.join(json_dir, '*.json')
file_list = glob.glob(json_pattern)
for file in file_list: 
    print(file)
    contents.append(json.load(open(file,'r')))