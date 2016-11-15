# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class orinocoItem(scrapy.Item):
    title = scrapy.Field()
    date1 = scrapy.Field()
    date2 = scrapy.Field()
    numero = scrapy.Field()
    texto = scrapy.Field()
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class longbuluoItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()


class OschinaItem(scrapy.Item):
    link = scrapy.Field()
    link_text = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()


class YppptItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    description = scrapy.Field()