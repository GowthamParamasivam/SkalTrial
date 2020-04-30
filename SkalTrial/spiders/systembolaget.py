# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class SystembolagetSpider(scrapy.Spider):
    name = 'systembolaget'
    allowed_domains = ['www.systembolaget.com']
    start_urls = ['https://www.systembolaget.se/sok-dryck/?searchquery=Whisky']

    def start_requests(self):
        start_urls = ['https://www.systembolaget.se/sok-dryck/?searchquery=Whisky']
        for url in start_urls:
            print("inside start")
            yield SeleniumRequest(url=url, wait_time=10, callback=self.parse)


    def parse(self, response):
        #todo .result-list>.elm-product-list-item-full>a
        # print("selenium "+response.request.meta['driver'].title)
        r = response.css(".result-list>.elm-product-list-item-full").getall()
        yield{
            'output': r


        }
        pass
