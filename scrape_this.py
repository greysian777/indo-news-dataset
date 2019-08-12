from ehe import pull_link_kompas, pull_paragraf_kompas, file_name, df_cleaner
from pertanggalan import generate_n_days_from_today, link, generate_from_date_range
import fire
import time
import os


def generate_links(n_days, file_name=file_name):
    """
    makes a csv of links from kompas within n_days from today (date of running)
    """
    list_of_dates = generate_n_days_from_today(n_days=n_days)
    print(f'generating {n_days} days worth of news')
    pull_link_kompas(link, list_of_dates, name=file_name+'_links')


def generate_links_with_date_range(start, end, file_name=file_name):
    """
    made a csv of links from kompas within start until end range of dates
    """
    list_of_dates = generate_from_date_range(start, end)
    print(f'scraping {len(list_of_dates)} days')
    pull_link_kompas(link, list_of_dates, name=file_name+'_links')


def generate_paragraphs(path_to_csv_links, file_name=file_name):
    """
    made a csv of paragraphs from a csv of links, where the csv must have a header of 'links'
    """
    import pandas as pd
    df = pd.read_csv(path_to_csv_links)
    df.dropna(inplace=True)
    links = df.links
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


if __name__ == "__main__":
    if not os.path.exists('csv/'):
        os.makedirs('csv/')
    fire.Fire()
