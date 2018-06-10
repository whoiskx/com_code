import scrapy

from tutorial.items import DmozItem


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allow_domains = ['dmoz-pdp.com']
    start_urls = [
        'http://www.dmoz-odp.org/Computers/Programming/Languages/Python/Books',
        "http://www.dmoz-odp.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            # /html/head/title
            item['title'] = sel.xpath('/html/head/title').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item