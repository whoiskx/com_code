#encoding=utf-8
import scrapy
from doubang250.items import Doubang250Item
from pyquery import PyQuery as pq


class DobangSpider(scrapy.Spider):
    name = 'doban'
    start_urls = ['https://movie.douban.com/top250']
    # allow_domains = 'douban.com'

    def parse(self, response):
        print("begin")
        # print(response.text)
        e = pq(response.text)
        q = e(".item")
        for i in q.items('.info'):
            item = Doubang250Item()
            item['name'] = i("span").eq(0).text()
            item['quote'] = i('.quote').eq(0).text()
            yield item