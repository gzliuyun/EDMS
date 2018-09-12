# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class person(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    expert_id = scrapy.Field()      #专家id
    expert_name = scrapy.Field()  #专家姓名
    university = scrapy.Field()   #专家所在大学
    college = scrapy.Field()       #专家所在院系
    expert_url = scrapy.Field()    #专家维普主页
    theme_list = scrapy.Field()
    sub_list = scrapy.Field()
    col_url = scrapy.Field()   #学院url

    amount1 = scrapy.Field()       #专家发文量
    amount2 = scrapy.Field()       #专家引文量
    h_index = scrapy.Field()      #h指数
    core = scrapy.Field()       #北大核心
    cssci = scrapy.Field()
    rdfybkzl = scrapy.Field()
    co_experts = scrapy.Field()
    co_agencies = scrapy.Field()

class paper(scrapy.Item):
    paper_id = scrapy.Field()       #论文id
    paper_title = scrapy.Field()    #论文标题
    paper_type = scrapy.Field()
    source = scrapy.Field()
    data1 = scrapy.Field()
    data2 = scrapy.Field()
    data3 = scrapy.Field()
    data4 = scrapy.Field()
    data5 = scrapy.Field()
    date = scrapy.Field()
    abstract = scrapy.Field()
    keyword = scrapy.Field()
    category = scrapy.Field()
    p_authors = scrapy.Field()
    p_author1 = scrapy.Field()
    p_author2 = scrapy.Field()
    p_author3 = scrapy.Field()
    p_author4 = scrapy.Field()
    p_author5 = scrapy.Field()


    pass
