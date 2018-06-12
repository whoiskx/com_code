# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from exts.spiders import MysqlRedisSpider
from exts.utils import sql_template2xpath, sql_query_with_ftp, sql_tuple2dict_with_ftp




class MasterSpider(MysqlRedisSpider):
    name = 'test'
    allowed_domains = ['test']

    def __init__(self, *args, **kwargs):
        super(MasterSpider, self).__init__(*args, **kwargs)

    def read_mysql(self):
        """Returns a request to be scheduled or none."""
        # if no data in cursor, then fetch from mysql
        if self.mysql_cursor.rowcount == -1:
            # make sure mysql connection is valid
            if not self.mysql_server.open:
                self.mysql_server.connect()
            self.mysql_cursor.execute(sql_query_with_ftp())
        # TODO: add support for reading a sql batch
        records = self.mysql_cursor.fetchmany(200)
        
        if records:
            for record in records:
                recordict = sql_tuple2dict_with_ftp(record)
                url = recordict.pop('url')
                yield Request(url, meta=recordict, dont_filter=True)

        if records:
            self.logger.debug("Read %s requests from mysql server", len(records))

    def parse(self, response):
        template = response.meta.pop("template")
        ftp = response.meta.pop('ftp')
        loader = ItemLoader(item={}, response=response)
        if template:
            xpaths = sql_template2xpath(template)
            for item, xpath in xpaths.items():
                loader.add_xpath(item, xpath)
        xmlcontent = loader.load_item()
        xmlcontent = self.get_title_if_not_exists(xmlcontent, response)
        return {"url": response.url,      # use to generate md5 as xml file name
                "xmlcontent": xmlcontent,        # content write to xml file
                "comment": response.meta, # comment of zipfile
                "ftp": ftp}
        
    
    def get_title_if_not_exists(self, xmlcontent, response):
        """get title using css selector"""
        title = response.css("title::text").extract_first()
        if not xmlcontent.get("title", None):
            xmlcontent['title'] = title
        return xmlcontent