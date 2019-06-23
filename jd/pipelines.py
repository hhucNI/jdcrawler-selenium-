# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import pymongo
from scrapy.exceptions import DropItem
class MongoPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_url=crawler.settings.get('MONGO_URL'),mongo_db=crawler.settings.get('MONGO_DB'))
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]
    def process_item(self,item,spider):
        res=self.db[item.collection].insert_one(dict(item))
        print(res.inserted_id)
        return item
    def close_spider(self,spider):
        self.client.close()


class Pipeline_toCSV(object):
    def __init__(self):
        self.location=os.path.curdir+"data2.csv"
    def open_spider(self,spider):
        self.file=open(self.location,'w')
        self.writer=csv.writer(self.file)
    def process_item(self,item,spider):
        if float(item['price'])<6000:
            raise DropItem("price is too low")
        if item:
            self.writer.writerow((item['title'].encode('utf8', 'ignore'), item['image'],item['price'],item['deal'],item['shop']))

        return item
    def close_spider(self,spider):
        self.file.close()