# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

class DemoSpiderDbItem(scrapy.Item):
    name = scrapy.Field()
    director = scrapy.Field()
    screenwriter = scrapy.Field()
    starring = scrapy.Field()
    synopsis = scrapy.Field()
