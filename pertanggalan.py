from itertools import islice
from datetime import date, timedelta


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def generate_date(prev_date):
    date_list = []
    for i in range(1, prev_date):
        tanggal = date(2019, 1, 1) - timedelta(i)
        date_list.append(tanggal)

    return date_list


def generate_n_date_from_today(n_days=174):
    return [date.today() - timedelta(i) for i in range(1, n_days)]


def generate_date_from_range(last, latest=date.today()): 
    last = [int(x) for x in last.split('-')]
    last = date(last[0], last[-2],last[-1])
    delta: date = latest-last
    print(f'updating for {delta.days} days from {last}')
    return [latest-timedelta(i) for i in range(1,delta.days)]


tahun_2018 = list(chunk(generate_date(366), 73))

q1 = tahun_2018[0]
q2 = tahun_2018[1]
q3 = tahun_2018[2]
q4 = tahun_2018[3]
q5 = tahun_2018[4]

tahun2019 = generate_n_date_from_today()

link = 'https://indeks.kompas.com/all/'