# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo

class SkaltrialPipeline:
    collection_name = "ProductsList"

    def open_spider(self,spider):
        logging.info("Pipeline *************** Open spider")
        self.client = pymongo.MongoClient("mongodb://hello:hello@127.0.0.1:27017/?authSource=admin&authMechanism=SCRAM-SHA-256")
        self.db = self.client['systembolaget']
        logging.info(str(self.client.server_info))

    def close_spider(self,spider):
        self.client.close()
        logging.info("close Spider *********************")

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item


