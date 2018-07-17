# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubang250Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    print('Item_start')
    name = scrapy.Field()
    title = scrapy.Field()
    quote =scrapy.Field()
    print("Item_end")
    pass
