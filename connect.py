#!/usr/bin/env python

from pymongo import MongoClient
import json
from fire import Fire
from typing import List, Set, Dict, Tuple, Optional, NewType


def fill_single():
    pass


class db_berita:
    def __init__(self, client, sumber, path_to_news_json,*args, **kwargs):
        self.client = MongoClient()
        self.sumber = sumber
        self.db = client['news'].sumber
        self.path_to_news_json = path_to_news_json

    def get_json(self):
        with open(self.path_to_news_json) as f:
            data = json.load(f)
        return data

    def insert_berita(self):
        result = self.db.insert_many(self.get_json(self.path_to_news_json))
        for o_id in result.inserted_ids:
            print(f'added new {self.sumber}, berita id is {o_id}')


if __name__ == '__main__':
    mydb = client['news']
    print(client.list_database_names())
    db_bisnis = mydb.bisnis
    berita = {
        "judul": "Pengembangan Model dan Sistem Pembiayaan JKN Butuh Dukungan Regulasi",
        "link": None,
        "paragraf": "Bisnis.com, JAKARTA \u2013 Pengembangan model dan sistem pembiayaan dalam program Jaminan Kesehatan Nasional (JKN) yang dijalankan BPJS Kesehatan dinilai membutuhkan dukungan regulasi. Pasalnya, langkah itu dinilai menjadi salah satu alternatif mengatasi tantangan mismatch atau defisit pengelolaan dana jaminan sosial. Direktur Utama BPJS Kesehatan Fachmi Idris mengatakan, sesuai dengan ketentuan perundang-undangan pihaknya diberi kewenangan untuk mengembangkan model pembiayaan dan sistem pembayaran kepada fasilitas kesehatan. Implementasinya dituangkan dalam kontrak kerja sama dengan fasilitas kesehatan yang diharapan bisa memberikan pelayanan yang lebih efektif dan efisien dengan mutu kualitas yang tetap terjaga. \u201cPengembangan model dan sistem pembiayaan fasilitas kesehatan juga merupakan bagian upaya implementasi strategi bauran kebijakan pengendalian defisit JKN. Namun, untuk mengimplementasikannya memerlukan regulasi pendukung,\u201d kata Fachmi kala memberikan paparan dalam International Health Economics Assosiation (IHEA) Congress, di Basel Swiss, seperti dikutip dalam keterangan resmi, Rabu (17/7/2019). Fachmi mengakui bahwa salah satu tantangan dalam penyelengaraan program JKN \u2013 Kartu Indonesia Sehat (JKN-KIS) saat ini adalah bagaimana menyelaraskan anggaran atau biaya yang terbatas dengan tingginya angka pemberian pelayanan kesehatan. Oleh karena itu, pengembangan model dan sistem pembiayaan menjadi salah satu alternatif mengatasi tantangan tersebut. Saat ini metode pembiayaan yang digunakan pihaknya adalah kapitasi dan INA CBG\u2019s. Namun, pihaknya tengah melakukan pengembangan model pembiayaan yang lebih efektif, antara lain kapitasi berbasis komitmen pelayanan (KBKP), hospital-value base, dan global budget. KBKP, jelasnya, merupakan sistem pembayaran kapitasi kepada Fasilitas Kesehatan Tingkat Pertama (FKTP) berdasarkan pemenuhan atau pencapaian empat indikator, yakni angka kontak, rasio rujukan rawat jalan kasus non spesialistik, rasio kunjungan rutin peserta program pengelolaan penyakit kronis atau Prolanis. Dengan begitu, kualitas pelayanan peserta di FKTP dapat ditingkatkan. \u201cUntuk metode hospital-value base sistem pembayaran yang dinilai menggunakan indikator value yang mewakili kebutuhan pasien, pembayar, rumah sakit dan regulator. Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL) dengan value yang baik dapat memperoleh insentif sedangkan jika memperoleh value yang tidak baik akan memperoleh disinsentif.\u201d Fachmi menambahkan metode global budget merupakan cara pembayaran klaim ke rumah sakit berdasarkan kepada anggaran yang dihitung secara keseluruhan. Proses administrasi metode ini, sebut dia, terbilang mudah sehingga dapat meningkatkan kemampuan rumah sakit untuk membuat keputusan yang rasional dalam memaksimalkan sumber daya yang tersedia. \u201cSelain itu, ada semacam fleksibilitas bagi rumah sakit untuk melakukan realokasi biaya pelayanan kesehatan sesuai dengan prioritas kebutuhannya,\u201d jelasnya.",
        "tanggal_berita": "17 Juli 2019 \u00a0",
        "tanggal_scraped": "2019-09-01"
    }
    result = db_bisnis.insert_many(get_json(r'hasil/bisnis.json'))
    for object_id in result.inserted_ids:
        print(f'added berita, course id is {object_id}')
