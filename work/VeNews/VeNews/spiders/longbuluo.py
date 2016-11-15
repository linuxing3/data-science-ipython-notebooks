# -*- coding: utf-8 -*-

# Define your spider here
#
# Don't forget to add your parse method
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# from scrapy.exceptions import DropItem
from VeNews.items import LongbuluoItem


class LongbuluoSpider(scrapy.Spider):
    name = "longbuluo"
    allowed_domains = ["lbldy.com"]
    start_urls = ('http://www.lbldy.com/movie/', )

    def parse(self, response):
        """
            open the movie page
        """
        for post in response.css('div.postlist'):
            movie_page_url = post.css('h4 > a::attr(href)').extract_first()
            yield scrapy.Request(
                response.urljoin(movie_page_url), callback=self.parse_movie)
        """
            check every page
        """
        for next_page in response.css('a.next'):
            next_page_url = next_page.css('::attr(href)').extract_first()
            yield scrapy.Request(
                response.urljoin(next_page_url), callback=self.parse)

    def parse_movie(self, response):
        for movie in response.css('.entry > p'):
            item = LongbuluoItem()
            """
                filter only thunder
            """
            urls = movie.css('a::attr(href)').extract()
            item['file_urls'] = [
                url for url in urls if url.startswith('thunder')]
            if item['file_urls']:
                yield item

