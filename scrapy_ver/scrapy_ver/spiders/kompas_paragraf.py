# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import logging

logger = logging.getLogger()


class KompasParagrafSpider(scrapy.Spider):
    name = 'kompas_paragraf'
    df = pd.read_csv('./csv/kompas.csv')
    allowed_domains = ['kompas.com',]
    logger.info('getting all the links')
    start_urls = list(df.link)

    def parse(self, response:scrapy.http.Response):
        ## /text() to extract all elements of p inside div
        paragraph = ' '.join(response.xpath('//div[@class="read__content"]/p//text()').extract())
        yield {
            'link':response.url,
            'p':paragraph
        }