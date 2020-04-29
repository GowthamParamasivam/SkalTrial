# -*- coding: utf-8 -*-
import scrapy


class SystembolagetSpider(scrapy.Spider):
    name = 'systembolaget'
    allowed_domains = ['www.systembolaget.com']
    start_urls = ['http://www.systembolaget.com/']

    def parse(self, response):
        pass
