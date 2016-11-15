# -*- coding: utf-8 -*-
# Define your spider here
#
# Don't forget to add your parse method
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from VeNews.items import YppptItem


class YppptSpider(scrapy.Spider):
    name = "ypppt"
    allowed_domains = ["ypppt.com"]
    start_urls = (
        'http://www.ypppt.com/moban',
    )

    def parse(self, response):
        """
            打开细节页面
        """
        for each in response.css("ul.posts > li > a.p-title::attr(href)"):
            url = response.urljoin(each.extract())
            yield scrapy.Request(url, callback=self.parse_ppt_with_filepipeline)

        """
            访问下一模版页面
        """
        for each in response.css(".page-navi > a::attr(href)"):
            url = response.urljoin(each.extract())
            yield scrapy.Request(url, callback=self.parse)

    def parse_ppt(self, response):
        """
            在细节页面抓取元素，由于不使用管道，file_urls和image_urls可以是字符串
        """
        item = YppptItem()
        files = response.css("div.infoss > h1::text").extract_first()
        fileUrl = response.css("a.down-button::attr(href)").extract_first()
        imageUrl = response.css(
            "ul.img_ul > li > img::attr(src)").extract_first()
        item['files'] = files
        item['file_urls'] = response.urljoin(fileUrl)
        item['image_urls'] = response.urljoin(imageUrl)
        return item

    def parse_ppt_with_filepipeline(self, response):
        """
            在细节页面抓取元素，由于使用管道，file_urls和image_urls必须是数组
        """
        item = YppptItem()
        files = response.css("div.infoss > h1::text").extract_first()
        fileUrl = response.css("a.down-button::attr(href)").extract()
        imageUrl = response.css("ul.img_ul > li > img::attr(src)").extract()
        item['files'] = files
        item['file_urls'] = [response.urljoin(url) for url in fileUrl]
        item['image_urls'] = [response.urljoin(url) for url in imageUrl]
        return item
