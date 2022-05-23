# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
import pymysql
import logging

logger = logging.getLogger(__name__)


class DemoSpiderPipeline:
    def __init__(self):
        self.f = open("data.json", 'a', encoding="utf8")

    def open_spider(self, spider):
        print('爬虫开始')

    def process_item(self, item, spider):
        print('正在保存{}'.format(item["name"]))
        self.f.write(str(item) + "\n")
        return item

    def close_spider(self, spider):
        print('爬虫关闭')
        self.f.close()


class DemoMySqlPipeline:
    coon = None
    cursor = None

    def open_spider(self, spider):
        self.coon = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            db='mydb',
            user='root',
            password='123456'
        )

    def process_item(self, item, spider):
        self.cursor = self.coon.cursor()
        try:
            # print('正在将数据保存{}到mysql'.format(item["name"]))
            # self.cursor.execute(
            #     "insert into douban(name,director,screenwriter,starring,synopsis) values ({},{},{},{},{})".format(
            #         item["name"], item["director"], item["screenwriter"],
            #         item["starring"], item["synopsis"])
            # )
            sql = "insert into douban(name,director,screenwriter,starring,synopsis) values(%s,%s,%s,%s,%s)"
            params = [(item["name"], item["director"], item["screenwriter"], item["starring"], item["synopsis"])]
            self.cursor.executemany(sql, params)
            self.coon.commit()
            return item
        except Exception as e:
            logger.error(e)

    def close_spider(self, spider):
        self.cursor.close()
        self.coon.close()
