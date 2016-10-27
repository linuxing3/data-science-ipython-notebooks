
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib
import scrapy
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

"""OrinocoPipeline is a filespipeline which
can download a pdf from the orinoco newpaper

we overwrite get_media_requests function to crawl url
and send the crawled item for further process

overwrite filepath function to generate customized file
saving path

item completed and send back item
"""
class OrinocoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'item': item})
    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        item['file_paths'] = file_paths
        return item
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_guid = request.url.split('/')[-1]
        if file_guid[-3:] == 'pdf':
            filename = u'full/orinoco-{0}'.format(file_guid)
            return filename
