from itertools import islice
from datetime import date, timedelta, datetime


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def generate_date(prev_date):
    date_list = []
    for i in range(1, prev_date):
        tanggal = date(2019, 1, 1) - timedelta(i)
        date_list.append(tanggal)

    return date_list


def generate_n_days_from_today(n_days=174):
    return [date.today() - timedelta(i) for i in range(1, n_days)]


def generate_from_date_range(start_date, end_date):
    # default bakal ngescrape tahun 2018
    start = datetime.strptime(start_date, "%d-%m-%Y").date()
    end = datetime.strptime(end_date, "%d-%m-%Y").date()
    return [start + timedelta(days=x) for x in range(0, (end-start).days)]


file_name = date.today().strftime("%Y-%m-%d")
tahun_2018 = list(chunk(generate_date(366), 73))

q1 = tahun_2018[0]
q2 = tahun_2018[1]
q3 = tahun_2018[2]
q4 = tahun_2018[3]
q5 = tahun_2018[4]

tahun2019 = generate_n_days_from_today()

link = 'https://indeks.kompas.com/all/'
