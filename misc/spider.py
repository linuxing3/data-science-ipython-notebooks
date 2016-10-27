import scrapy

class orinocoSpider(scrapy.Spider):	
	name = 'orinocoSpider'
	start_urls = ['http://www.correodelorinoco.gob.ve/edicion-impresa']
	def parse(self, response):
		for p in response.css('p.link'):
			text = p.css('a ::text').extract_first()
			href = p.css('a ::attr(href)').extract_first()
			title = p.css('a ::attr(title)').extract_first()
			item = {'text':text, 'href': href, 'title':title}
			yield item
		
		for next_page in response.css('a.page'):
			next_page_url =  next_page.css('::attr(href)').extract_first()
			yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)
