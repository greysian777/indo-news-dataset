from itertools import islice


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def generate_date(prev_date):
    from datetime import date, timedelta
    date_list = []
    for i in range(1, prev_date):
        tanggal = date(2019, 1, 1) - timedelta(i)
        date_list.append(tanggal)

    return date_list


def generate_date_from_today(prev_date=174):
    from datetime import date, timedelta
    date_list = []
    for i in range(1, prev_date):
        tanggal = date.today() - timedelta(i)
        date_list.append(tanggal)

    return date_list

tahun_2018 = list(chunk(generate_date(366), 73))

q1 = tahun_2018[0]
q2 = tahun_2018[1]
q3 = tahun_2018[2]
q4 = tahun_2018[3]
q5 = tahun_2018[4]

tahun2019 = generate_date_from_today()

link = 'https://indeks.kompas.com/all/'