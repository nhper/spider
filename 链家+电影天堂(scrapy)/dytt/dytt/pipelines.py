# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import pymongo
conn = pymongo.MongoClient("mongodb://localhost :27017")
mydb = conn['test']
myset = mydb['movie']
class DyttPipeline(object):
    def process_item(self, item, spider):
        myset.insert(item['content'])
        return item
