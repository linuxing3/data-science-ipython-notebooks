# -*- coding: utf-8 -*-
# Define your spider here
# Don't forget to add your parse method
import scrapy

from VeNews.items import YoutubeItem


class YoutubeSpider(scrapy.Spider):
    """
        youtube爬虫
    """
    name = "youtube"
    allowed_domains = ["youtube.com"]
    start_urls = [
        # "https://www.youtube.com/feed/trending",
        # "https://www.youtube.com/playlist?list=PLiSJ-0KobHCKnku5ZuypaSwoTYjOJLjWL",
        "https://www.youtube.com/playlist?list=PL5-da3qGB5ICeMbQuqbbCOQWcS6OYBr5A",
        "https://www.youtube.com/playlist?list=PL5-da3qGB5ICCsgW1MxlZ0Hq8LL5U3u9y"
    ]


    def parse(self, response):
        """
            获取视频页面
        """
        # for each in response.css('h3.yt-lockup-title'):
        for each in response.css('.pl-video-title'):
            video_url = each.css('a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(video_url), callback=self.parse_youtube)

    def parse_youtube(self, response):
        """
            获取视频网页的元素
        """
        item = YoutubeItem()
        item['files'] = response.css('.watch-title::text').extract_first()
        item['file_urls'] = [response.url]
        yield item
