# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkaltrialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WhiskeyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name1 = scrapy.Field()
    name2 = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    bottle_text = scrapy.Field()
    pass
