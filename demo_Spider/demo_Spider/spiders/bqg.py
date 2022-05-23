import re

import scrapy
from demo_Spider.items import DemoSpiderItem


class BqgSpider(scrapy.Spider):
    name = 'bqg'
    allowed_domains = ['www.xxxbiquge.com']
    start_urls = ['http://www.xxxbiquge.com/6/6321/']

    def parse(self, response, **kwargs):
        data_list = response.xpath("//div[@id='list']/dl/dd")
        items = DemoSpiderItem()
        for data in data_list:
            items["title"] = data.xpath("./a/text()").extract_first()
            items["url"] = "https://www.xxxbiquge.com" + data.xpath("./a/@href").extract_first()
            yield items
