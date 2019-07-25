from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random 

df = pd.DataFrame(columns=['title', 'image', 'url', 'date'])

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def pull_data_kompas(link, list_of_date, name, pagination=50):
    try:
        for date_current in list_of_date:
            for j in range(1, pagination):
                dict_ = {}
                url = link + str(date_current) + '/' + str(j)
                print(url)

                # Get article from website
                headers = {'User-Agent': f'{random.choice(user_agent_list)}'}
                req = requests.get(url, headers = headers)
                soup = BeautifulSoup(req.content, 'lxml')

                try:
                    container = soup.find(
                        'div', attrs={'class': 'latest--indeks mt2 clearfix'})

                except:
                    print('container not found')
                    print('will sleep for 30 seconds...')
                    time.sleep(30)
                    continue

                try:
                    boxes = container.find_all(
                        'div', attrs={'class': 'article__list clearfix'})
                except:
                    print('box not found')
                    print('will sleep for 30 seconds...')
                    time.sleep(30)
                    continue

                for i in range(0, len(boxes)):
                    box = container.find_all(
                        'div', attrs={'class': 'article__list clearfix'})[i]
                # Get Title Article
                    try:
                        title = box.find('h3').text
                    except:
                        print('h2.text not found')
                        break

                    # Get Image
                    try:
                        image = box.find('img').get('src')
                    except:
                        print('image not found')
                        break

                    # Get URL Article
                    try:
                        url = box.find('a').get('href')
                    except:
                        print('href not found')
                        break

                    # Get Date
                    date = date_current
                    # print(title, image, url)

                    # Get Title Article
                    dict_['title'] = title
                    dict_['image'] = image
                    dict_['url'] = url
                    dict_['date'] = date
                    df_ = pd.Series(dict_)
                    df1 = df.append(df_, ignore_index=True)

                    df1.to_csv(f'csv/berhasil_{name}.csv', mode='a', header=False)
            print(date_current)
        return "done"
    except:
        pass

    
def pull_source(link=None): 
    headers = {'User-Agent': f'{random.choice(user_agent_list)}'}
    r = requests.get(link, headers = headers)
    s = BeautifulSoup(r.content, 'lxml')
    return (s.prettify())
    

def pull_paragraf(link = None): 
    headers = {'User-Agent': f'{random.choice(user_agent_list)}'}
    r = requests.get(link, headers = headers)
    s = BeautifulSoup(r.content, 'lxml')
    reader = s.find('div',{'class':'read__content'})
    if 'MAAF KAMI TIDAK MENEMUKAN HALAMAN YANG ANDA CARI' in s.text: 
        return '404'
    else if type(reader) == type(None): 
        reader=s.find('div', {'class': 'main-artikel-paragraf'})
    else if 'jeo' in link: 
        print('jeo link')
        return 'JEO TYPED SHIT'
    else:
        for child in reader.find_all("strong"):
            child.decompose()
    return(reader.get_text())

def main():

    pull_data_kompas('https://indeks.kompas.com/all/', 50, 365)


if __name__ == "__main__":
    frame = pd.read_csv('KOMPAS 2018.csv')
    print(pull_paragraf(frame.link[0]))
