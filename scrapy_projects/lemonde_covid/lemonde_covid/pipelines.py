# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class MongodbPipeline(object):
    collection_name = "3months_covid"

    def open_spider(self, spider):
        logging.warning("SPIDER OPENED FROM PIPELINE")
        self.client = pymongo.MongoClient("mongodb+srv://flabastie:oSccIqXjb2QBYNMh@cluster0.izrur.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.client["news_analysis"]

    def close_spider(self, spider):
        logging.warning("SPIDER CLOSED FROM PIPELINE")
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item