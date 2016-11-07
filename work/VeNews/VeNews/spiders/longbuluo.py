# -*- coding: utf-8 -*-
import scrapy
# from scrapy.exceptions import DropItem
from VeNews.items import longbuluoItem


class LongbuluoSpider(scrapy.Spider):
    name = "longbuluo"
    allowed_domains = ["lbldy.com"]
    start_urls = (
        'http://www.lbldy.com/movie/',
    )

    def parse(self, response):
        """
            open the move page
        """
        for post in response.css('div.postlist'):
            movie_page_url = post.css('h4 > a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(movie_page_url), callback=self.parse_movie)
        """
            check every page
        """
        for next_page in response.css('a.next'):
            next_page_url =  next_page.css('::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)

    def parse_movie(self, response):
        for movie in response.css('.entry > p'):
            item = longbuluoItem()
            """
                filter only thunder
            """
            urls = movie.css('a::attr(href)').extract()
            item['file_urls'] = [url for url in urls if url[0:7] == 'thunder']
            if item['file_urls']:
                yield item
