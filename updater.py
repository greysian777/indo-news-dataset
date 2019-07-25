from ehe import pull_data_kompas, get_latest_date
from pertanggalan import generate_date_from_range, link
import pandas as pd 
from datetime import def funcname(self, parameter_list):
    raise NotImplementedError

# get csv from folder
# TESTING WITH BERHASIL_2019.csv
tanggal_terakhir = get_latest_date('csv/berhasil_TEST_1.csv')


file_name = date.today().strftime("%Y-%m-%d")
list_of_dates_to_be_updated = generate_date_from_range(last=tanggal_terakhir)

def main(): 
    pull_data_kompas(link, list_of_dates_to_be_updated, name=file_name)

if __name__ == "__main__":
    main()