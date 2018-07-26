# -*- coding: utf-8 -*-
import scrapy
import requests
import json

from scrapy.http import Request

import exts.weiboUtils as wbutils
from exts.spiders import RedisSpider

class WeiboSpider(RedisSpider):
    name = 'weibo'
    allowed_domains = ['weibo']

    def __init__(self, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        text = json.loads(response.text)
        blogs = wbutils.create_blogs(text)
        ftp = response.meta.pop('ftp')

        if blogs:
            item = {
                'url': response.url,
                'xmlcontent': blogs[0],
                'comment': response.meta,
                'ftp': ftp,
            }
        else:
            item = None
        return item