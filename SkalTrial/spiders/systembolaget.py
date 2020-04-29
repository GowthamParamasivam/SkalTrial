# -*- coding: utf-8 -*-
import scrapy


class SystembolagetSpider(scrapy.Spider):
    name = 'systembolaget'
    allowed_domains = ['www.systembolaget.com']
    start_urls = ['https://www.systembolaget.se/sok-dryck/?searchquery=Whisky']

    def parse(self, response):
        #todo .result-list>.elm-product-list-item-full>a
        #response.
        print (response)
        r = response.css(".result-list>.elm-product-list-item-full").getall();
        #print ("ouput")
        #print (r)
        yield{
            'output': r


        }
        pass
