# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from exts.spiders import RedisSpider
from exts.utils import sql_template2xpath

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re

class SlaveSpider(RedisSpider):
    name = 'test'
    
    def __init__(self, *args, **kwargs):
        super(SlaveSpider, self).__init__(*args, **kwargs)
        self.meta = None
    def parse_item(self, response):
        template = self.meta.get("template")
        ftp = self.meta.get('ftp')
        loader = ItemLoader(item={}, response=response)
        if template:
            xpaths = sql_template2xpath(template)
            for item, xpath in xpaths.items():
                # if '|' in xpath:
                #     xpath = xpath.split('|')[0]
                loader.add_xpath(item, xpath)
        xmlcontent = loader.load_item()
        
        if not xmlcontent.get('title') or not xmlcontent.get('content'):
            return None

        xmlcontent = self.clear_html_tag(xmlcontent)
        xmlcontent['url'] = response.url
        return {"url": response.url,            # use to generate md5 as xml file name
                "xmlcontent": xmlcontent,       # content write to xml file
                "comment": self.meta,           # comment of zipfile
                "ftp": ftp}

    def parse(self, response):
        # get next urls
        self.meta = response.meta
        next_selector = response.xpath('//*/a/@href')

        for url in next_selector.extract():
            if url.endswith('html') or url.endswith('htm'):
                yield response.follow(url, callback=self.parse_item, errback=None)


    def get_title_if_not_exists(self, xmlcontent, response):
        """get title using css selector"""
        title = response.css("title::text").extract_first()
        if not xmlcontent.get("title"):
            xmlcontent['title'] = title
        return xmlcontent

    def clear_html_tag(self, xmlcontent):
        pattern = re.compile('<[^>]*>')
        for k, v in xmlcontent.items():
            if type(v) != type('strtype'):
                v = ''.join(v)
            v = pattern.sub("", v)
            if k == 'time':
                v = re.sub('\(|\)', "", v)
            xmlcontent[k] = v
        return xmlcontent