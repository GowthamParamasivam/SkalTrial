# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import datetime
import re
from SkalTrial.items import DrinksLatest, Store
from urllib.parse import parse_qs, urlparse
  
class Systembolaget1Spider(scrapy.Spider):
    name = 'systembolaget1'
    total = 0
    parsed_count = 0
 
    def start_requests(self):
        sub_cats = ['Bitter','Vitt%20vin','Whisky','Sake','Tequila%20och%20Mezcal']
        # sub_cats = ['Bitter']
        for sub_cat in sub_cats:
            yield scrapy.Request(
                url=f'https://www.systembolaget.se/api/productsearch/search/sok-dryck/?subcategory={sub_cat}&sortfield=Name&sortdirection=Ascending&site=all&fullassortment=1&page=1&nofilters=1',
                callback=self.parse
            )
 
    def parse(self, response):
        Item = DrinksLatest()
        json_resp = json.loads(response.body)
        products = json_resp.get('ProductSearchResults')
        cat = parse_qs(urlparse(str(response.request.url)).query)['subcategory'][0]
        now = datetime.datetime.now()
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
            Item['BeverageDescriptionShort'] = product.get(
                'BeverageDescriptionShort')
            Item['Taste'] = product.get('Taste')
            Item['SellStartText'] = product.get('SellStartText')
            Item['Availability'] = product.get('Availability')
            Item['VolumeText'] = product.get('VolumeText')
            Item['image_urls'] = [product.get('ProductImage').get('ImageUrl')]
            Item['ScrappedDate'] = now.strftime("%Y-%m-%d %H:%M:%S")
            # Forming url for the stores
            find_store_url = f'https://www.systembolaget.se/api/site/findallstoreswhereproducthasstock/{Item["ProductId"]}/1'
            # You need  to send the stores list in the request meta
            yield scrapy.Request(find_store_url, callback=self.parse_store, meta={'item': Item, 'cnt_url': 1, 'stre_list': []})
        next_page = json_resp.get('Metadata').get('NextPage')
        if next_page != -1:
            yield scrapy.Request(
                url=f"https://www.systembolaget.se/api/productsearch/search/sok-dryck/?subcategory={cat}&sortfield=Name&sortdirection=Ascending&site=all&fullassortment=1&page={next_page}&nofilters=1",
                callback=self.parse
            )
 
 
    def parse_store(self, response):
        # grab the current stores list
        stre_list = response.meta['stre_list']
        json_store = json.loads(response.body)
        total = json_store.get('DocCount')
        Item = response.meta['item']
        cnt_url = response.meta['cnt_url']
        url = str(response.request.url).rsplit('/', 1)[0]
        cnt_url = cnt_url+1
        if total != 0:
            stores = json_store.get('SiteStockBalance')
            for store1 in stores:
                stre = Store()
                stre['StoreNumber'] = store1.get('Site').get('StoreNumber')
                # append the store the list
                stre_list.append(stre)
                Item['Store'] = stre_list
                # send the current existing stores list.
                yield scrapy.Request(url+"/"+str(cnt_url), callback=self.parse_store, meta={'item': Item, 'cnt_url': cnt_url, 'stre_list': stre_list})
        else:
            yield Item