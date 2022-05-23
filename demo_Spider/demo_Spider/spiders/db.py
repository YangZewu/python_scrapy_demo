import scrapy
from demo_Spider.items import DemoSpiderDbItem


# import logging

# logger = logging.getLogger(__name__)
class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['movie.douban.com']
    url = "https://movie.douban.com/top250?start={}&filter="
    start_urls = [url.format(0)]

    def parse(self, response, **kwargs):
        for page in range(0, 11):
            page_url = self.url.format(page * 25)
            yield scrapy.Request(url=page_url, callback=self.parse_url)

    def parse_url(self, response):
        url_list = response.xpath("//div[@id='content']/div/div[1]/ol/li/div/div[2]/div/a/@href").extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.re_data)

    def re_data(self, response):
        items = DemoSpiderDbItem()
        items["name"] = ''.join(response.xpath("//div[@id = 'wrapper']/div/h1/span/text()").extract_first())
        items["director"] = ''.join(response.xpath("//div[@id='info']/span[1]/span[2]/a/text()").extract())
        items["screenwriter"] = ''.join(response.xpath("//div[@id='info']/span[2]/span[2]/a/text()").extract())
        items["starring"] = ''.join(response.xpath("//div[@id='info']/span[3]/span[2]/a/text()").extract())
        items["synopsis"] = ''.join(response.xpath("//*[@id='link-report']/span[2]/text()[1]").extract())
        # logger.warning('this is warning')
        yield items
