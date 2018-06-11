# -*- coding: utf-8 -*-
import scrapy
import requests
import json

from scrapy.http import Request

import exts.weiboUtils as wbutils
from exts.spiders import MysqlRedisSpider
from exts.utils import sql_weibo_with_ftp, sql_weibo_tuple2dict_with_ftp
class WeiboSpider(MysqlRedisSpider):
    name = 'weibo'
    allowed_domains = ['weibo']
    apiformat = "https://api.weibo.com/2/statuses/user_timeline.json?source=82966982&uid={}&page=1&count=1"

    def __init__(self, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)

    def read_mysql(self):
        """Returns a request to be scheduled or none."""
        # if no data in cursor, then fetch from mysql
        if self.mysql_cursor.rowcount == -1:
            # make sure mysql connection is valid
            if not self.mysql_server.open:
                self.mysql_server.connect()
            self.mysql_cursor.execute(sql_weibo_with_ftp())
        # TODO: add support for reading a sql batch
        records = self.mysql_cursor.fetchmany(200)
        
        if records:
            for record in records:
                recordict = sql_weibo_tuple2dict_with_ftp(record)
                url = self.apiformat.format(recordict.pop('uid'))
                yield Request(url, meta=recordict, dont_filter=True)

        if records:
            self.logger.debug("Read %s requests from mysql server", len(records))


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