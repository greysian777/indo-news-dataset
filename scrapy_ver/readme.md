# scrapy version
- 9920 berita selesai dalam 32 detik

todo:
- [x] buat scraping paragraph
  - [ ] handle 403 error --> try this [one](https://stackoverflow.com/questions/13724730/how-to-get-the-scrapy-failure-urls) collects all failed url
- [ ] handle all links inside a page, can be implemented to all berita_links, [check here](https://www.varunpant.com/posts/web-crawling-or-scraping-using-scrapy-in-python), atau bisa pake [CrawlSpider](https://stackoverflow.com/questions/44527996/scrapy-understanding-crawlspider-and-linkextractor) which is better
    - ```python
        # -*- coding: utf-8 -*-
        import scrapy


        # item class included here
        class DmozItem(scrapy.Item):
            # define the fields for your item here like:
            link = scrapy.Field()
            attr = scrapy.Field()


        class DmozSpider(scrapy.Spider):
            name = "dmoz"
            allowed_domains = ["craigslist.org"]
            start_urls = [
            "http://chicago.craigslist.org/search/emd?"
            ]

            BASE_URL = 'http://chicago.craigslist.org/'

            def parse(self, response):
                links = response.xpath('//a[@class="hdrlnk"]/@href').extract()
                for link in links:
                    absolute_url = self.BASE_URL + link
                    yield scrapy.Request(absolute_url, callback=self.parse_attr)

            def parse_attr(self, response):
                item = DmozItem()
                item["link"] = response.url
                item["attr"] = "".join(response.xpath("//p[@class='attrgroup']//text()").extract())
                return item
        ```
- [x] buat scraping interval tanggal

