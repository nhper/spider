# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
conn = MySQLdb.connect(host="localhost",port=3306,user="root",password="123456",
                       db = "spider",charset="utf8"
                       )
cur = conn.cursor()
class ShangbiaoPipeline(object):
    def process_item(self, item, spider):
        sql = 'insert into br values(%s,%s,%s)'
        cur.executemany(sql,item['content'])
        conn.commit()
        return item
