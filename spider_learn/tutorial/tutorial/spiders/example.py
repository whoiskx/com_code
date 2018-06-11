# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['examplec.com']
    start_urls = ['http://examplec.com/']

    def parse(self, response):
        pass
