# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class SkaltrialPipeline:
    collection_name = "ProductsList"

    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb://hello:hello@127.0.0.1:27017/?authSource=admin&authMechanism=SCRAM-SHA-256")
        self.db = self.client['systembolaget']

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        try:
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)
        except ValueError:
            logging.info("Exception of Value Error happened")

    def item_completed(self, results, item, info):
        logging.info(item['_id'])
        logging.info(item['image_urls'])
        return item
