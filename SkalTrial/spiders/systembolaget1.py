# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from SkalTrial.items import DrinksLatest
import datetime
import re
from urllib.parse import parse_qs, urlparse

class Systembolaget1Spider(scrapy.Spider):
    name = 'systembolaget1'
    def start_requests(self):
        sub_cats = ['Bitter','Vitt%20vin','Whisky','Sake','Tequila%20och%20Mezcal']
        for sub_cat in sub_cats:
            yield scrapy.Request(
                url=f'https://www.systembolaget.se/api/productsearch/search/sok-dryck/?subcategory={sub_cat}&sortfield=Name&sortdirection=Ascending&site=all&fullassortment=1&page=1&nofilters=1',
                callback=self.parse
            )

    def parse(self, response):
        json_resp = json.loads(response.body)
        products = json_resp.get('ProductSearchResults')
        now = datetime.datetime.now()
        cat = parse_qs(urlparse(str(response.request.url)).query)['subcategory'][0]
        logging.info(response.request.url)
        logging.info(cat)
        for product in products:
            Item = DrinksLatest()
            Item['ProductId'] = product.get('ProductId')
            Item['ProductNumber'] = product.get('ProductNumber')
            Item['ProductNameBold'] = product.get('ProductNameBold')
            Item['ProductNameThin'] = product.get('ProductNameThin')
            Item['Category'] = product.get('Category')
            Item['ProductNameBold'] = product.get('ProductNameBold')
            Item['ProductNumberShort'] = product.get('ProductNumberShort')
            Item['ProducerName'] = product.get('ProducerName')
            Item['BottleTextShort'] = product.get('BottleTextShort')
            Item['Volume'] = product.get('Volume')
            Item['Price'] = product.get('Price')
            Item['Country'] = product.get('Country')
            Item['SubCategory'] = product.get('SubCategory')
            Item['Type'] = product.get('Type')
            Item['BeverageDescriptionShort'] = product.get('BeverageDescriptionShort')
            Item['Taste'] = product.get('Taste')
            Item['SellStartText'] = product.get('SellStartText')
            Item['Availability'] = product.get('Availability')
            Item['VolumeText'] = product.get('VolumeText')
            Item['image_urls'] = [product.get('ProductImage').get('ImageUrl')]
            Item['ScrappedDate'] = now.strftime("%Y-%m-%d %H:%M:%S")
            yield Item
        next_page = json_resp.get('Metadata').get('NextPage')
        logging.info(next_page)
        if next_page:
            yield scrapy.Request(
                url=f"https://www.systembolaget.se/api/productsearch/search/sok-dryck/?subcategory={cat}&sortfield=Name&sortdirection=Ascending&site=all&fullassortment=1&page={next_page}&nofilters=1",
                callback=self.parse
            )
