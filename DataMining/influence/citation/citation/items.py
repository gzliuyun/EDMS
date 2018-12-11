# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CitationItem(scrapy.Item):
    # define the fields for your item here like:
    cita = scrapy.Field()
    id = scrapy.Field()
    pass
