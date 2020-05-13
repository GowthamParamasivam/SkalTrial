# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request, Selector
import requests
from SkalTrial.items import DrinksLatest, StoreOpen

class SkaltrialPipeline:
    collection_name = "ProductsList"
    sotre_collection = 'StoreList'

    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb://hello:hello@127.0.0.1:27017/?authSource=admin&authMechanism=SCRAM-SHA-256")
        self.db = self.client['systembolaget']
        if spider.name in ['systembolagetstore']:
            try:
                self.db[self.sotre_collection].drop()
            except:
                logging.info("Exception occurred while deleting the store database")
        if spider.name in ['systembolaget1']:
            try:
                self.db[self.collection_name].drop()
            except Exception as ex:
                logging.info(str(ex))
                logging.info("Exception occurred while deleting the products database")

    def close_spider(self,spider):
        if spider.name in ['systembolagetstore']:
            try:
                self.db[self.sotre_collection].create_index([("Lat",1),("Long",1)])
                self.db[self.sotre_collection].create_index([("OpenToday",1)])
            except:
                logging.info("Exception occurred while closing the store database")
        if spider.name in ['systembolaget1']:
            self.db[self.collection_name].create_index([("Store.Latitude",1),("Store.Longitude",1)])
            try:
                stores = self.db[self.sotre_collection].find({'OpenToday':{ '$ne': None }})
                logging.info("************")
                logging.info(str(stores.count()))
                for store in stores:
                    # result = self.db[self.collection_name].update({"Store.Latitude":{"$eq":store['Lat']},"Store.Longitude":{"$eq":store['Long']},"Store.StoreTimingToday":{"$exists" : False}},{ "$set": { "Store.$['SiteId'].StoreTimingToday":store['OpenToday']}},{ "arrayFilters": [{"SiteId": { '$eq': store['SiteId'] } } ]},multi=True)
                    result = self.db[self.collection_name].update({"Store.SiteId":store['SiteId']},{ "$set": { "Store.$.StoreTimingToday":store['OpenToday']}},multi=True)
                    logging.info(str(result))
            except Exception as ex:
                logging.info("Exception occurred while closing the product database")
                logging.info(str(ex))
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,DrinksLatest):
            # if 'Store' in item and item['Store'] is not None:
            #     stores = item['Store']
            #     for store in stores:
            #         storeopen = self.db[self.sotre_collection].find_one({'Lat':store['Latitude'],'Long':store['Longitude']})
            #         if storeopen is not None:
            #             store['StoreTimingToday'] = storeopen['OpenToday']
            self.db[self.collection_name].insert(item)
        if isinstance(item,StoreOpen):
            self.db[self.sotre_collection].insert(item)
        return item


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
    # def __init__(self, crawler):
    #     self.crawler = crawler
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler)

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