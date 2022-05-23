import scrapy
import json
from Tencent.items import TencentItem
import logging

logger = logging.getLogger(__name__)


class TxSpider(scrapy.Spider):
    name = 'TX'
    allowed_domains = ['careers.tencent.com']
    url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1653310646054&countryId=&cityId=&bgIds=&productId=&categoryId=40001001,40001002,40001003,40001004,40001005,40001006&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn"
    start_urls = [url.format(1)]

    def parse(self, response):
        for index in range(2, 11):
            url_page = self.url.format(index)
            yield scrapy.Request(url=url_page, callback=self.parse_info)

    def parse_info(self, response):
        data = json.loads(response.text)
        jdata = data["Data"]["Posts"]
        for post in jdata:
            PostId = post["PostId"]
            Post_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1653312923664&postId={}&language=zh-cn".format(
                PostId)
            yield scrapy.Request(url=Post_url, callback=self.re_data)

    def re_data(self, response):
        items = TencentItem()
        data = json.loads(response.text)
        items["name"] = data["Data"]["RecruitPostName"]
        items["request"] = data["Data"]["Requirement"]
        items["duty"] = data["Data"]["Responsibility"]
        items["addr"] = data["Data"]["LocationName"]
        yield items
