# -*- coding: utf-8 -*-

""" Correo del orinoco

1. urls of news article:
http://www.correodelorinoco.gob.ve/categoria/categorias/venezuela/nacionales/

2. selectors of DOM elments:
archive > div.spoiler > a.left
archive > div.spoiler > div > h3.subtitle
archive > div.spoiler > div > h2.title
archive > div.spoiler > div > div.meta
archive > div.spoiler > div > p

"""
import scrapy
from VeNews.items import orinocoItem


orinocoUrl1 = 'http://www.correodelorinoco.gob.ve',
orinocoUrl1 = 'http://www.correodelorinoco.gob.ve',

def checkURL(url):
    file_guid = url.split('/')[-1]
    if file_guid[-3:] != 'pdf':
        url = u'{0}print'.format(url)
    return url


class OrinocosSpiderPage(scrapy.Spider):
    name = "orinocoSpiderPage"
    start_urls = (
        'http://www.correodelorinoco.gob.ve/categoria/categorias/venezuela/nacionales',
        'http://www.correodelorinoco.gob.ve/categoria/categorias/venezuela/caracas',
        'http://www.correodelorinoco.gob.ve/categoria/categorias/venezuela/regiones',
        'http://www.correodelorinoco.gob.ve/categoria/categorias/venezuela/politica',
        'http://www.correodelorinoco.gob.ve/categoria/categorias/opinion/',
        'http://espejo3.correodelorinoco.gob.ve/categoria/categorias/venezuela/impacto/',
        'http://espejo3.correodelorinoco.gob.ve/categoria/categorias/venezuela/poder-popular/',
        'http://espejo3.correodelorinoco.gob.ve/categoria/categorias/venezuela/investigacion/',
        'http://espejo3.correodelorinoco.gob.ve/categoria/categorias/venezuela/alimentacion/',
    )

    def parse(self, response):
        for elm in response.css('div#archive > div.spoiler'):
            """
                Creating a item
            """
            item = orinocoItem()
            """
                Extracting titles
            """
            item['title'] = elm.css('div > h2.title ::text').extract()
            """
                Extracting href
            """
            urls = elm.css('a.left ::attr(href)').extract()
            urls = [checkURL(url) for url in urls if url]
            item['file_urls'] =  urls

            yield item


class OrinocoSpiderPdf(scrapy.Spider):
    name = "orinocoSpiderPdf"
    allowed_domains = ["correodelorinoco.gob.ve"]
    start_urls = (
        'http://www.correodelorinoco.gob.ve/edicion-impresa',
    )

    def start_request(self):
        pass

    def log(self, message, level=3, **kw):
        scrapy.Spider.logger.info('msg')

    def parse(self, response):
        """ parse the table
        for elm in response.css('table > tr > td:nth-child(even)')
        for elm in response.css('table > tr > td:nth-child(even) > img ::attr(src)'):
        for elm in response.css('table > tr > td:nth-child(odd) > p.date1')
        for elm in response.css('table > tr > td:nth-child(odd) > p.date2')
        for elm in response.css('table > tr > td:nth-child(odd) > p.numero')
        for elm in response.css('table > tr > td:nth-child(odd) > p.text')
        for elm in response.css('table > tr > td:nth-child(odd) > p.link:nth-child(even) > a.text ::attr(href)')
        for elm in response.css('table > tr > td:nth-child(odd) > p.link:nth-child(odd) > a.text ::attr(href)')
        """
        for elm in response.css('table > tr'):
            item = orinocoItem()
            """get even table data, which has images link
            """
            item['image_urls'] = elm.css('td:nth-child(odd) > img.attachment-medium::attr(src)').extract()
            """get other meta data from odd table data
            """
            item['date1'] = elm.css('td:nth-child(even) > p.date1 ::text').extract()
            item['date2'] = elm.css('td:nth-child(even) > p.date2 ::text').extract()
            item['numero'] = elm.css('td:nth-child(even) > p.numero ::text').extract()
            item['texto'] = elm.css('td:nth-child(even) > p.texto ::text').extract()

            urls = elm.css('td:nth-child(even) > p.link > a.text ::attr(href)').extract()
            urls = [checkURL(url) for url in urls if url]
            item['file_urls'] = urls
            yield item

        for next_page in response.css('a.page'):
            """
                if you want to go through all pages, using following code
                next_page_url =  next_page.css('::attr(href)').extract_first()
                yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)
            """
            pass
