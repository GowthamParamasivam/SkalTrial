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
        # sub_cats = ['Bitter','Vitt%20vin','Whisky','Sake','Tequila%20och%20Mezcal',
        #             'Anissprit','Aperitif%20och%20dessert','Alkoholfritt','Armagnac%20och%20Brandy',
        #             'Blanddrycker','Blandl%C3%A5dor%20vin','Calvados','Mousserande%20vin','Cider','Cognac',
        #             'Drinkar%20och%20Cocktails','Dryckestillbeh%C3%B6r','Frukt%20och%20Druvsprit',
        #             'Gl%C3%B6gg%20och%20Gl%C3%BChwein','Grappa%20och%20Marc','Lik%C3%B6r','Aperitif%20och%20dessert',
        #             'Presentf%C3%B6rpackningar','Punsch','Rom','Ros%C3%A9vin','Ros%C3%A9%20-%20l%C3%A4gre%20alkoholhalt',
        #             'Smaksatt%20sprit','Sprit%20av%20flera%20typer','Vermouth','Vitt%20vin','Vita%20-%20l%C3%A4gre%20alkoholhalt',
        #             'Vodka%20och%20Br%C3%A4nnvin','%C3%96l','R%C3%B6tt%20vin','R%C3%B6da%20-%20l%C3%A4gre%20alkoholhalt',
        #             'Akvavit%20och%20Kryddat%20br%C3%A4nnvin','Gin%20och%20Genever','Mousserande%20vin']
        sub_cats = ['Bitter']
        for sub_cat in sub_cats:
            yield scrapy.Request(
                url=f'https://www.systembolaget.se/api/productsearch/search/sok-dryck/?subcategory={sub_cat}&sortfield=Name&sortdirection=Ascending&site=all&fullassortment=1&page=0&nofilters=1',
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
                stre['SiteId'] = store1.get('Site').get('SiteId')
                stre['Alias'] = store1.get('Site').get('Alias')
                stre['StreetAddress'] = store1.get('Site').get('StreetAddress')
                stre['PostalCode'] = store1.get('Site').get('PostalCode')
                stre['City'] = store1.get('Site').get('City')
                stre['Phone'] = store1.get('Site').get('Phone')
                stre['County'] = store1.get('Site').get('County')
                stre['IsTastingStore'] = store1.get('Site').get('IsTastingStore')
                stre['IsActiveForAgentOrder'] = store1.get('Site').get('IsActiveForAgentOrder')
                stre['IsStore'] = store1.get('Site').get('IsStore')
                stre['IsDepot'] = store1.get('Site').get('IsDepot')
                stre['IsAgent'] = store1.get('Site').get('IsAgent')
                stre['OpeningHours'] = store1.get('Site').get('OpeningHours')
                stre['DeliverySchedule'] = store1.get('Site').get('DeliverySchedule')
                stre['PickupHours'] = store1.get('Site').get('PickupHours')
                stre['SiteUrl'] = store1.get('Site').get('SiteUrl')
                stre['OpeningHoursTodayText'] = store1.get('Site').get('OpeningHoursTodayText')
                stre['Shelf'] = store1.get('Stock').get('Shelf')
                stre['Stock'] = store1.get('Stock').get('Stock')
                stre['SectionLabel'] = store1.get('Stock').get('SectionLabel')
                stre['ShelfLabel'] = store1.get('Stock').get('ShelfLabel')
                stre['StockLabel'] = store1.get('Stock').get('StockLabel')
                stre['NotYetSaleStarted'] = store1.get('Stock').get('NotYetSaleStarted')
                stre['Latitude'] = store1.get('Site').get('Position').get('Lat')
                stre['Longitude'] = store1.get('Site').get('Position').get('Long')
                stre['Rt90x'] = store1.get('Site').get('Position').get('Rt90x')
                stre['Rt90y'] = store1.get('Site').get('Position').get('Rt90y')
                stre['StoreTimingToday'] = 'N/A'
                # append the store the list
                stre_list.append(stre)
                Item['Store'] = stre_list

                # send the current existing stores list.
            yield scrapy.Request(url+"/"+str(cnt_url), callback=self.parse_store, meta={'item': Item, 'cnt_url': cnt_url, 'stre_list': stre_list})
        else:
            yield Item
        


