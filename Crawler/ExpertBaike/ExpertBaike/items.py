# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ExpertbaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ExpertInfoItem:
    def __init__(self):
        self.school = ""
        self.name = ""
        self.id = ""

    def __init__(self, school, name, id):
        self.school = school
        self.name = name
        self.id = id
