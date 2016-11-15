# -*- coding: utf-8 -*-

# Define your spider here
#
# Don't forget to add your parse method
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

from VeNews.items import OschinaItem


class OschinaSpider(scrapy.Spider):
    """
        抓去博客
    """
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
            blog_url = post.css(
                'header.blog-title-box > a.blog-title-link::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(blog_url), callback=self.parse_blog)
        """
            check every page
        """
        for next_page in response.css('a.next'):
            next_page_url = next_page.css('::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_blog)

    def parse_blog(self, response):
        """
            parse the blog detail page
        """
        item = OschinaItem()
        item['link'] = response.url
        item['file_urls'] = response.url

        texts = response.css('.blog-heading > .title::text').extract()
        title = ""
        for text in texts:
            title += text
        item['link_text'] = title.strip()

        yield item


class ScrapyOschinaSpider(scrapy.Spider):
    """
        抓去全局文章
    """
    name = "scrapy_oschina"
    allowed_domains = ["oschina.net"]
    start_urls = (
        'http://www.oschina.net/',
    )

    def parse(self, response):
        sel = scrapy.Selector(response)
        links_in_a_page = sel.xpath('//a[@href]')  # 页面内的所有链接

        for link_sel in links_in_a_page:
            item = OschinaItem()
            link = str(link_sel.re('href="(.*?)"')[0])    # 每一个url
            if link:
                if not link.startswith('http'):  # 处理相对URL
                    link = response.url + link
                # 生成新的请求, 递归回调self.parse
                yield scrapy.Request(link, callback=self.parse)
                item['link'] = link
                # 每个url的链接文本, 若不存在设为None
                link_text = link_sel.xpath('text()').extract()
                if link_text:
                    item['link_text'] = str(
                        link_text[0].encode('utf-8').strip())
                else:
                    item['link_text'] = None
                yield item
