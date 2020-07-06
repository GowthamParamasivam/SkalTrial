# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import re
from SkalTrial.items import StoreOpen


class SystembolagetstoreSpider(scrapy.Spider):
    name = 'systembolagetstore'

    def start_requests(self):
            yield scrapy.Request(
                url=f'https://www.systembolaget.se/api/site/getallstoresandagentsformap/1',
                callback=self.parse
            )
    
    def parse(self, response):
        json_resp = json.loads(response.body)
        stores = json_resp.get('Stores')
        Agents = json_resp.get('Agents')
        for store in stores:
            storeopen = StoreOpen()
            now = datetime.datetime.now()
            storeopen['Alias'] = store.get('Alias')
            storeopen['Address'] = store.get('Address')
            storeopen['City'] = store.get('City')
            storeopen['County'] = store.get('County')
            storeopen['Lat'] = store.get('Lat')
            storeopen['Long'] = store.get('Long')
            storeopen['OpenToday'] = store.get('OpenToday')
            storeopen['SiteId'] = store.get('SiteId')
            storeopen['IsAgent'] = store.get('IsAgent')
            storeopen['IsTastingStore'] = store.get('IsTastingStore')
            storeopen['ScrappedDate'] = now.strftime("%Y-%m-%d %H:%M:%S")
            yield storeopen
        for store in Agents:
            storeopen = StoreOpen()
            now = datetime.datetime.now()
            storeopen['Alias'] = store.get('Alias')
            storeopen['Address'] = store.get('Address')
            storeopen['City'] = store.get('City')
            storeopen['County'] = store.get('County')
            storeopen['Lat'] = store.get('Lat')
            storeopen['Long'] = store.get('Long')
            storeopen['OpenToday'] = store.get('OpenToday')
            storeopen['SiteId'] = store.get('SiteId')
            storeopen['IsAgent'] = store.get('IsAgent')
            storeopen['IsTastingStore'] = store.get('IsTastingStore')
            storeopen['ScrappedDate'] = now.strftime("%Y-%m-%d %H:%M:%S")
            yield storeopen
