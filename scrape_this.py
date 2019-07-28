from ehe import pull_data_kompas, pull_paragraf, file_name, df_cleaner
from pertanggalan import generate_n_days_from_today, link
import fire, time, os


# `python scrape_this.py <N_DAYS_TO_SCRAPE_FROM_TODAY>`

def generate_links(n_days): 
    list_of_dates = generate_n_days_from_today(n_days=n_days)
    print(f'generating {n_days} days worth of news')
    pull_data_kompas(link, list_of_dates, name=file_name+'_links')

def generate_paragraphs(path_to_csv_links): 
    import pandas as pd 
    df = pd.read_csv(path_to_csv_links)
    df.dropna(inplace=True)
    links = df.links
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

if __name__ == "__main__":
    if not os.path.exists('csv/'):
        os.makedirs('csv/')
    fire.Fire()