# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

from scrapy import signals
from scrapy.exporters import JsonItemExporter, BaseItemExporter, CsvItemExporter


"""

	电影项输出工具

	MovieItemExport is subclass of BaseItemExporter

	@fields_to_export, such as file_urls
	export_item(), return specific object instead of item itself

"""


class MovieItemExporter(BaseItemExporter):
    fields_to_export = 'file_urls'

    def export_item(item):
        return item['file_urls'][0]


"""

	奥利诺科邮报下载管道

	OrinocoPipeline is a filespipeline which
	can download a pdf from the orinoco newpaper

	we overwrite [get_media_requests] function to crawl url
	and send the crawled item for further process

	overwrite [filepath] function to generate customized file
	saving path

	item completed and send back item
"""


class OrinocoPipeline(FilesPipeline):
    """
        manipulating file url from the item got
        if url is ended with pdf, let it be
        if url is a webpage, redirecting to print version
    """
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'item': item})
    """
        Checking item with file_paths
    """
    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        item['file_paths'] = file_paths
        return item
    """
        Saving file with customized name and path
    """
    def file_path(self, request, response=None, info=None):
        """
            checking file extension, if pdf, rename it with pdf extension
            if a webpage, rename with url and html extension
        """
        file_guid = request.url.split('/')[-1]
        if file_guid[-3:] == 'pdf':
            filename = u'full/orinoco-{0}'.format(file_guid)
        else:
            filename = u'full/{0}.html'.format(request.url.split('/')[-2])
        return filename



"""
	电影处理管道
"""


class MoviePipeline(FilesPipeline):
    """
        manipulating file url from the item got
        if url is ended with pdf, let it be
        if url is a webpage, redirecting to print version
    """
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'item': item})
    """
        Checking item with file_paths
    """
    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        item['file_paths'] = file_paths
        return item
    """
        Saving file with customized name and path
    """
    def file_path(self, request, response=None, info=None):
        """
            checking file extension, if pdf, rename it with pdf extension
            if a webpage, rename with url and html extension
        """
        file_guid = request.url.split('/')[-1]
        if file_guid[-3:] == 'pdf':
            filename = u'full/movie-{0}'.format(file_guid)
        else:
            filename = u'full/{0}.html'.format(request.url.split('/')[-2])
        return filename


"""
	json文件导出器

	需要复写一下方法：

	from_crawler:调用信号，触发实例的方法

	spider_opended:打开爬虫时，输出到文件

	spider_closed:关闭爬虫时，关闭文件

	process_item:处理项幕
"""


class JsonExportPipeline(object):
	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('%s_products.json' % spider.name, 'w+b')
		self.files[spider] = file
		self.exporter = JsonItemExporter(file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item


import codecs
class FinancialspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('financial_file1', mode='ab', encoding='utf-8')
    def process_item(self, item, spider):
        content = item['html_content']
        #self.file.write(content.decode("unicode_escape"))
        self.file.write(content)
        return item


"""
	text文件导出器

	需要复写一下方法：

	from_crawler:调用信号，触发实例的方法

	spider_opended:打开爬虫时，输出到cvs文件

	spider_closed:关闭爬虫时，关闭文件

	process_item:处理项幕
"""
class TextExportPipeline(object):

	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('files/full/%s.csv' % spider.name, 'w+b')
		self.files[spider] = file
		self.exporter = CsvItemExporter(file, 0)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item



"""
	编码写入文件内容
"""
class EncodingPipeline(object):
	def __init__(self):
		self.files = {}

	def process_item(self, item, spider):
		content = item['file_urls']
		file = codecs.open('files/full/%s.txt' % spider.name, mode='ab', encoding='utf-8')
		#file.write(content.decode("unicode_escape"))
		file.write(content)
		return item

"""
    oschina pipeline
"""
class OschinaPipeline(object):

    def __init__(self):
        self.file = open('result.jl', 'w')
        self.seen = set()   #  重复检测集合

    def process_item(self, item, spider):
        if item['link'] in self.seen:
            raise DropItem('Duplicate link %s' % item['link'])
        self.seen.add(item['link'])
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item


import pymongo
class MongoPipeline(object):

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
		return cls(
				mongo_host=crawler.settings.get('MONGO_HOST'),
				mongo_port=crawler.settings.get('MONGO_PORT'),
				mongo_db=crawler.settings.get('MONGO_DB', 'oschinadb'),
				)
    def open_spider(self, spider):
        # 打来爬虫时候，连接mongo数据库
        # 生成客户端
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        # 连接数据库
        # self.db = spider.name
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 实用类名作为集合名称
        collection_name = item.__class__.__name__
        # 用客户端插入项的字典
        self.db[collection_name].insert(dict(item))
        return item
