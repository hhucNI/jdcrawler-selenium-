# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from urllib.parse import quote
from jd.items import JdItem

class JdcrawlSpider(Spider):
    name = 'jdcrawl'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?keyword='

    def start_requests(self):

        for keyword in self.settings.get('KEYWORDS'):

            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)



    def parse(self, response):

        products = response.xpath(

            '//div[@id="J_searchWrap"]//div[@id="J_goodsList"]//li')

        for product in products:
            
            item = JdItem()
            
            item['image'] = ''.join(product.xpath('.//div[@class="p-img"]//a/@href').extract()).strip()#dei
            item['price'] = ''.join(product.xpath('.//div[@class="p-price"]//i/text()').extract()).strip()#dei
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//a/text()').extract()).strip()#dei
            item['title'] = ''.join(product.xpath('.//div[contains(@class,"p-name")]//em//text()').extract()).strip()#dei
            item['deal'] = ''.join(product.xpath('.//div[@class="p-commit"]//text()').extract()).strip()#dei
            
            
            yield item
