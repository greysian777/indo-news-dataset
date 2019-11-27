# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import logging
from twisted.internet.defer import Deferred

logger = logging.getLogger()


class KompasParagrafSpider(scrapy.Spider):
    name = 'kompas_paragraf'
    df = pd.read_csv('./csv/kompas.csv')
    allowed_domains = ['kompas.com',]
    logger.info('getting all the links')
    start_urls = list(df.link)

    def parse(self, response:scrapy.http.Response):
        ## /text() to extract all elements of p inside div
        for l in self.start_urls:
            yield scrapy.Request(l,callback=self.parse_paragraf,errback=self.non_stop_func,dont_filter=True)
    def parse_paragraf(self,response:scrapy.http.Response):
        paragraph = ' '.join(response.xpath('//div[@class="read__content"]/p//text()').extract())
        yield {
            'link':response.url,
            'p':paragraph
        }


    def non_stop_func(self,failure):
        self.logger.error(f'{repr(failure)}')
        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            self.logger.error(f'HttpError on {response.url}')

