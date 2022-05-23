# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import logging

logger = logging.getLogger(__name__)


class TencentPipeline:
    coon = None
    cursor = None

    def open_spider(self, spider):
        print('爬虫开始')
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
            print('正在保存{}'.format(item["name"]))
            sql = "insert into tx(name,duty,request,addr) values(%s,%s,%s,%s)"
            params = [(item["name"], item["duty"], item["request"], item["addr"])]
            self.cursor.executemany(sql,params)
            self.coon.commit()
            return item
        except Exception as e:
            logger.error(e)
            self.coon.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.coon.close()
        print('爬虫关闭')

