import scrapy


class DobangSpider(scrapy.Spider):
    name = 'doban'
    start_url = 'https://movie.douban.com/top250'
    allow_domains = 'douban.com'

    def parse(self, response):
        print("begin")