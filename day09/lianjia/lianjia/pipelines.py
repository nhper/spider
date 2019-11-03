# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

conn = pymongo.MongoClient("mongodb://10.103.86.62:27017")
mydb = conn['test']
myset = mydb['zufang']

class LianjiaPipeline(object):
    def process_item(self, item, spider):
        myset.insert(dict(item))
        return item
