# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from exts.spiders import RedisSpider
from exts.utils import sql_template2xpath

class SlaveSpider(RedisSpider):
    name = 'test'
    allowed_domains = ['test']

    def __init__(self, *args, **kwargs):
        super(SlaveSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        template = response.meta.pop("template")
        ftp = response.meta.pop('ftp')
        loader = ItemLoader(item={}, response=response)
        if template:
            xpaths = sql_template2xpath(template)
            for item, xpath in xpaths.items():
                loader.add_xpath(item, xpath)
        xml = loader.load_item()
        
        return {"url": response.url,      # use to generate md5 as xml file name
                "xmlcontent": xml,        # content write to xml file
                "comment": response.meta, # comment of zipfile
                "ftp": ftp}