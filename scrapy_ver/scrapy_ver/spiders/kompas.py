# -*- coding: utf-8 -*-
import scrapy
import logging
logger = logging.getLogger()



class KompasSpider(scrapy.Spider):
    name = 'kompas'
    allowed_domains = ['indeks.kompas.com']
    start_urls = ['https://indeks.kompas.com/']

    def parse(self,response):
        url = response.url
        total_page = int(response.xpath('//a[@class="paging__link paging__link--prev"]/@data-ci-pagination-page').get())
        for page in range(1,total_page):
            url_fix =f'{url}/?page={page}/'
            logging.info(f'URL: {url}/?page={page}/')
            yield scrapy.Request(url=url_fix, callback=self.parse_page)

    def parse_page(self, response: scrapy.http.Response):
        link = response.xpath('//a[@class="article__link"]/@href').extract()
        judul = response.xpath('//a[@class="article__link"]/text()').extract()
        tanggal = response.xpath('//div[@class="article__date"]/text()').extract()
        kategori = response.xpath('//div[@class="article__subtitle article__subtitle--inline"]/text()').extract()

        for l,j,t,k in zip(link,judul,tanggal,kategori):
            berita = {
                'link':l,
                'judul':j,
                'tanggal': t,
                'kategori':k
            }
            yield berita

