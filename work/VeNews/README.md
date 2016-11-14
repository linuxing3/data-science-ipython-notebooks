# 使用scrapy自动获取工作用的网页

## 生成项目

以 oschina 为例

```shell
scrapy startproject oschina
cd oschina
```

## 爬虫

#### 生成模板`spider`然后修改:

```shell
scrapy genspider oschina oschina.net   # scrapy genspider 爬虫名 要爬取的域名
```

#### 基本功能

* 每一个爬虫有一个方法`parse`，可以实现网页的抓取

* 使用`css`来选择网页元素

* 基本的方法是`element::attr(href)`和`element::text`

* 输出元素的内容实用`extract`和`extract_first`

* 使用`scrapy.Request`可以请求新的页面

#### 编辑 `spiders/oschina.py`:

```python
class OschinaSpider(scrapy.Spider):
    name = "oschina"
    allowed_domains = ["oschina.net"]
    start_urls = (
        'https://www.oschina.net/blog',
    )

    def parse(self, response):
        """
            open the blog page
        """
        for post in response.css('.item'):
            blog_url = post.css('header.blog-title-box > a.blog-title-link::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(blog_url), callback=self.parse_blog)
        """
            check every page
        """
        for next_page in response.css('a.next'):
            next_page_url =  next_page.css('::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_blog)

    def parse_blog(self, response):
        item = OschinaItem()
        item['link'] = response.url
        item['file_urls'] = response.url

        texts = response.css('.blog-heading > .title::text').extract()
        title = ""
        for text in texts:
            title += text
        item['link_text'] = title.strip()

        yield item
```

#### 运行:

```shell
scrapy crawl oschina    #运行爬虫
```

## 项

编辑 items.py, 内容如下:

```python
class orinocoItem(scrapy.Item):
    link = scrapy.Field()
```

## 管道

#### 最强大的功能之一，可以自动化全部的流程

* 每个返回的`item`，必须要有一个`file_urls`和`file_path`

* 将`item`传入管道，`FilesPipeline`和`ImagesPipeline`就可以自动处理并下载

#### 编辑 `settings.py`, 内容如下:

```python
ITEM_PIPELINES = {
   'scrapy.pipelines.files.FilesPipeline': 1,
   'scrapy.pipelines.images.ImagesPipeline': 2,
}
FILES_STORE = 'files'
IMAGES_STORE = 'images'
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
```

#### 编辑 `pipelines.py`, 内容如下:

```python
"""
	text文件导出器
	需要复写一下方法：
	@from_crawler:调用信号，触发实例的方法
	@spider_opended:打开爬虫时，输出到cvs文件
	@spider_closed:关闭爬虫时，关闭文件
	@process_item:处理项幕
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
```

## 设置

## 中间件

## 其它

和`pyspider`比较，`scrapy`有强大的自定义功能