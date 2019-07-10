from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

df = pd.DataFrame(columns=['title', 'image', 'url', 'date'])


def pull_data_kompas(domain, date, name, pagination=50):
    try:
        for date_current in date:
            for j in range(1, pagination):
                dict_ = {}
                url = domain + str(date_current) + '/' + str(j)
                print(url)

                # Get article from website
                req = requests.get(url)
                soup = BeautifulSoup(req.content, 'lxml')

                try:
                    container = soup.find(
                        'div', attrs={'class': 'latest--indeks mt2 clearfix'})

                except:
                    print('container not found')
                    continue

                try:
                    boxes = container.find_all(
                        'div', attrs={'class': 'article__list clearfix'})
                except:
                    print('box not found')
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

                    df1.to_csv(f'berhasil_{name}.csv', mode='a', header=False)
            print(date_current)
        return "done"
    except:
        pass


def main():

    pull_data_kompas('https://indeks.kompas.com/all/', 50, 365)


if __name__ == "__main__":
    main()
