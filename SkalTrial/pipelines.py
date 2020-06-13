# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import scrapy
import datetime
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request, Selector
import requests
from SkalTrial.items import DrinksLatest, StoreOpen, Store

class SkaltrialPipeline:
    collection_name = "ProductsList"
    sotre_collection = 'StoreList'

    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb://hello:hello@127.0.0.1:27017/?authSource=admin&authMechanism=SCRAM-SHA-256")
        self.db = self.client['systembolaget']
        if spider.name in ['systembolagetstore']:
            try:
                self.db[self.sotre_collection].drop()
                logging.warning("Starting Time fo the Store Spider")
            except:
                logging.warning("Exception occurred while deleting the store database")
                # Since systembolaget1 is the first spider, we need to do the cleaning and start fresh
        if spider.name in ['systembolaget1']:
            try:
                self.db[self.collection_name].drop()
                logging.warning("Starting Time fo the Product Spider")
                self.db['Stores'].drop()
            except Exception as ex:
                logging.info(str(ex))
                logging.warning("Exception occurred while deleting the products database")

    def close_spider(self,spider):
        if spider.name in ['systembolagetstore']:
            try:
                self.db[self.sotre_collection].create_index([("Lat",1),("Long",1)])
                self.db[self.sotre_collection].create_index([("OpenToday",1)])
                self.db[self.sotre_collection].create_index([("SiteId",1)])
                logging.warning("stopping Time fo the Store Spider")
            except:
                logging.warning("Exception occurred while closing the store database")
            logging.warning(self.stats.get_value('item_scraped_count'))
            # Since systembolaget4 is the last running spider we are creating index in this part
        if spider.name in ['systembolaget4']:
            self.db[self.collection_name].create_index([("Store.Location","2dsphere")])
            try:
                stores = self.db[self.sotre_collection].find({'OpenToday':{ '$ne': None }})
                logging.info("************")
                logging.info(str(stores.count()))                
                for store in stores:
                    result = self.db[self.collection_name].update({"Store.SiteId":store['SiteId']},{ "$set": { "Store.$.StoreTimingToday":store['OpenToday']}},multi=True)
                    products = self.db[self.collection_name].find()
                for product in products:
                    stores1=[]
                    if(product['Store']==None):
                        break
                    stores1 = product['Store']
                    for st in stores1:
                        self.db['Stores'].insert(st)
                #Adding the index to the stores
                self.db['Stores'].create_index([("Location","2dsphere")])
            except Exception as ex:
                logging.warning("Exception occurred while closing the product database")
                logging.info(str(ex))
        logging.warning("stopping Time fo the product Spider")
        logging.warning(self.stats.get_value('item_scraped_count'))
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,DrinksLatest):
            self.db[self.collection_name].insert(item)
        if isinstance(item,StoreOpen):
            self.db[self.sotre_collection].insert(item)
        if isinstance(item,Store):
            self.db['Stores'].insert(item)
        return item
    
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item,DrinksLatest):
            try:
                for image_url in item['image_urls']:
                    yield scrapy.Request(image_url)
            except ValueError:
                logging.info("Exception of Value Error happened in pipeline")
            except KeyError:
                logging.info("Exception of Key Error happened in pipeline")

    def item_completed(self, results, item, info):
        if isinstance(item,DrinksLatest):
            image_paths = [x['path'] for ok, x in results if ok]
            item['image_paths'] = image_paths
        return item


class MyPipelineToAddOpeningTime:
    def process_item(self, item, spider):
        base_url = 'https://www.systembolaget.se'
        try:
            stores = item['Store']
            for store in stores:
                custom_url = base_url+str(store['SiteUrl'])
                response = requests.get(custom_url)
                response1 = Selector(response)
                if response.status_code == 200:
                    time1 = response1.css('#main > div.container > div.row.site-page-content > div.col-sm-6.col-md-5.col-lg-4.opening-hours > ul > li:nth-child(1) > span.pull-right::text').get()
                    store['StoreTimingToday'] = time1
        except ValueError:
            logging.info("Exception of Value Error happened in pipeline")
        except KeyError:
            logging.info("Exception of Key Error happened in pipeline")
        return item