# kompas news scraper

made a dataset.

## kumpulan dataset
[here](https://github.com/svmihar/ta-dump)

## how this works
1. generates the links scraped from certain date
2. links that are scraped saved into csv which makes `links_{source}_{date_generated}.csv`
    - hdf5 and json are optional
3. `links_{source}_{date_generated}.csv` will be scraped to generate the paragraph and makes `p_{source}_{date_generated}.csv`
4. all generated csv will be saved on `csv/` folder    
all generated csv, can be scraped single thread or concurrently.
## sumber 
sumber yang supported: 
- kompas 
- detik 
- bisnis 
- tempo


## scraping
**generate csv full of links for n_days from today**    
`python scrape_this.py generate_links <N_DAYS_TO_SCRAPE_FROM_TODAY> <SUMBER>`    

!TODO
- [ ] implementasi `class Paragraf`
  - [x] bikin puller paragraf, tanggal berita, author, judul --> dictionary
  - [ ] list_of_links --> links -> berita_template: Dict --> list_of_berita_template -> csv
  - bikin csv yang update per row
  - [ ] append csv_p dengan csv_link
- [ ] buat jadi `class Paragraf` concurrent
- [x] unpack list of dict buat class
  - [x] detik
  - [x] bisnis
  - [x] tempo
  - [x] kompas
  - [ ] jakarta post, lastpagenya 4074
 ~~ - [ ] kontan? ~~
- [x] make an updater for latest news. 
- [x] fix missing values in current dataset
- [x] implement cli
- [x] merging stuff for csv
- [x] buat multithreading pecah jadi 2 buat generate p 
    - jadi 1 buat 1/2 csv, 1 buat sisanya
- [x] buat dask? 
    - single thread: 128s
    - dask: 43s
  - [ ] bikin supaya ada airflow nya
- [x] sanity check buat 'jeo' di `ehe.py` - [x] bikin scrape biar punya parameter untuk save ke csv atau json atau semuanya 
- [x] implement link class
  - [x] implement pagination and fix on the generators 

skips all jeo links in kompas, few samples: 
- [sample4](https://entertainment.kompas.com/jeo/artis-indonesia-dan-moge-sekadar-hobi-dan-gaya)
- [sample9](https://entertainment.kompas.com/jeo/cerita-artis-indonesia-dan-moge-tunggangannya)
- [sample12](https://travel.kompas.com/jeo/riwayat-sambal-nusantara)
- [sample13](https://nasional.kompas.com/jeo/pecah-kongsi-bongkar-pasang-koalisi-pemilu-2019)
- [sample19](https://nasional.kompas.com/jeo/pansel-kpk-menjawab-polemik-dan-kritik)
- [sample22](https://nasional.kompas.com/jeo/setelah-putusan-mk-menolak-seluruh-gugatan-sengketa-pilpres-2019)
- [sample33](https://nasional.kompas.com/jeo/pokok-perkara-dan-jawaban-tergugat-sidang-mk-sengketa-pilpres-2019)
- [sample43](https://nasional.kompas.com/jeo/hal-hal-yang-perlu-kita-tahu-soal-sengketa-hasil-pemilu-2019)
- [sample46](https://money.kompas.com/jeo/tren-dan-tips-bisnis-jastip-raup-rupiah)
- [sample56](https://megapolitan.kompas.com/jeo/lebaran-di-jakarta-mau-apa-dan-liburan-ke-mana)
- [sample58](https://megapolitan.kompas.com/jeo/mudik-lebaran-pulang-menjemput-keajaiban-maaf)
- [sample74](https://bola.kompas.com/jeo/ke-olimpiade-2020-lalu-muhammad-zohri-terus-melaju)
- [sample99](https://nasional.kompas.com/jeo/sidang-isbat-rukyat-hisab-dan-penanggalan-islam)
- [sample106](https://entertainment.kompas.com/jeo/avengers-endgame-akhir-saga-11-tahun)
- [sample129](https://nasional.kompas.com/jeo/panduan-lengkap-buat-pemilih-pemilu-2019)
- [sample132](https://regional.kompas.com/jeo/memahami-pemilih-dengan-gangguan-jiwa-dan-berkebutuhan-khusus)
- [sample134](https://regional.kompas.com/jeo/membaca-peluang-jokowi-vs-prabowo-di-lumbung-suara-jateng-dan-diy)
- [sample135](https://regional.kompas.com/jeo/jokowi-maruf-vs-prabowo-sandi-berebut-suara-penentu-di-jawa-barat)
- [sample136](https://money.kompas.com/jeo/industri-40-janji-dan-tantangan-para-capres-pemilu-2019)
- [sample137](https://money.kompas.com/jeo/jokowi-vs-prabowo-intip-strategi-mereka-buat-pertumbuhan-ekonomi-indonesia)
- [sample138](https://regional.kompas.com/jeo/sulsel-peta-tak-terprediksi-jokowi-maruf-vs-prabowo-sandiaga)
- [sample139](https://nasional.kompas.com/jeo/buka-bukaan-biaya-caleg-demi-kursi-di-senayan)
- [sample141](https://money.kompas.com/jeo/polemik-utang-di-mata-para-capres-pemilu-2019)
- [sample143](https://money.kompas.com/jeo/adu-program-jokowi-dan-prabowo-soal-kesejahteraan-mana-yang-realistis)
- [sample144](https://regional.kompas.com/jeo/di-sumut-jokowi-maruf-dan-prabowo-sandiaga-berpeluang-sama-kuat)
- [sample145](https://regional.kompas.com/jeo/jokowi-maruf-vs-prabowo-sandiaga-siapa-lebih-berpeluang-di-jawa-timur)
- [sample147](https://nasional.kompas.com/jeo/pertanyaan-seputar-pemilu-2019-dan-jawabannya)
- [sample148](https://money.kompas.com/jeo/jokowi-vs-prabowo-pilpres-2019-dan-defisit-neraca-perdagangan)
- [sample152](https://entertainment.kompas.com/jeo/menunggu-akhir-kisah-game-of-thrones-season-8)
- [sample153](https://nasional.kompas.com/jeo/hal-hal-yang-pemilih-pemilu-2019-wajib-tahu)
- [sample170](https://internasional.kompas.com/jeo/fakta-dan-reaksi-dunia-atas-serangan-teroris-ke-masjid-di-selandia-baru)
- [sample174](https://bola.kompas.com/jeo/badminton-indonesia-mau-sampai-kapan-andalkan-ganda-putra)
- [sample176](https://nasional.kompas.com/jeo/caleg-eks-koruptor-siapa-saja-dan-apa-kata-parpolnya)
- [sample178](https://bola.kompas.com/jeo/timnas-indonesia-juara-aff-u-22-kado-kesejukan-di-tengah-kepahitan)
- [sample180](https://otomotif.kompas.com/jeo/cek-mobil-paling-laku-di-indonesia-sepanjang-2018)
- [sample185](https://ekonomi.kompas.com/jeo/hal-hal-krusial-terkait-debat-kedua-pilpres-2019)
- [sample186](https://properti.kompas.com/jeo/infrastruktur-tantangan-jokowi-dan-prabowo-memajukan-indonesia)
- [sample187](https://ekonomi.kompas.com/jeo/pilpres-2019-dan-bayang-bayang-ancaman-krisis-energi)
- [sample189](https://ekonomi.kompas.com/jeo/menunggu-eksplorasi-kebijakan-jokowi-dan-prabowo-soal-ketahanan-pangan)
- [sample190](https://nasional.kompas.com/jeo/pilpres-2019minus-gereget-pemberantasan-korupsi)
- [sample193](https://megapolitan.kompas.com/jeo/menelaah-3-pembunuhan-sadis-di-jabodetabek)
- [sample194](https://bola.kompas.com/jeo/perhentian-akhir-liliyana-natsir-terima-kasih-butet)
- [sample197](https://megapolitan.kompas.com/jeo/ahok-bebas)
- [sample199](https://nasional.kompas.com/jeo/polemik-pembebasanbaasyir-antara-kemanusiaan-dan-hukum)
- [sample200](https://nasional.kompas.com/jeo/pilpres-2019-antiklimaks-perlindungan-ham)
- [sample201](https://nasional.kompas.com/jeo/terorisme-menurut-jokowi-maruf-dan-prabowo-sandiaga)
