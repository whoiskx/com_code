# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    # 小说地址
    noveurl = scrapy.Field()
    # 连载状态
    serialstatus = scrapy.Field()
    # 连载字数
    serialnumber = scrapy.Field()
    # 文章类别
    category = scrapy.Field()
    # 小说编号
    name_id = scrapy.Field()


class DcontentItem(scrapy.Item):
    # 小说编号
    id_name = scrapy.Field()
    chapter_content = scrapy.Field()
    # 章节顺序
    num = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_name = scrapy.Field()

