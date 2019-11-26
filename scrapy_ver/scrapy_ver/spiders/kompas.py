# -*- coding: utf-8 -*-
import scrapy
import logging
logger = logging.getLogger()



class KompasSpider(scrapy.Spider):
    name = 'kompas'
    allowed_domains = ['indeks.kompas.com']
    start_urls = ['https://indeks.kompas.com/']

    def parse(self, response: scrapy.http.Response):
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

