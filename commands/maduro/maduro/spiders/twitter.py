# -*- coding: utf-8 -*-
import scrapy

import maduro.items

class TwitterSpider(scrapy.Spider):
    name = "press"
    allowed_domains = ["https://twitter.com/"]
    start_urls = (
        'https://twitter.com/maduro_en',
    )


    contentSelector = '.stream-items > .stream-item > .content'
    textSelector = 'div.js-tweet-text-container > p.js-tweet-text'
    photoSelector = 'div.AdaptiveMedia-singlePhoto > div.js-adaptive-photo::data-image-url'
	# https://twitter.com/search?q=maduro&src=typd
	# ol.stream-items > li.stream-item > div.content > div.stream-item-header
	                                                 #> div.js-tweet-text-container > p.js-tweet-text
	                                                 #> div.AdaptiveMedia-singlePhoto > .js-adaptive-photo
	# js-tweet-text
    def parse(self, response):
    	items = []
        for post in response.css(self.contentSelector).extract():
	    	item = MaduroItem()
        	item.text = post.css(self.textSelector)
        	item.photo = post.css(self.photoSelector)
        	items.append(item)
        	yield item
