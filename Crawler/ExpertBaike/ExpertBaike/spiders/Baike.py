# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
from ExpertBaike.items import ExpertInfoItem
import re
from urllib.parse import unquote

class BaikeSpider(scrapy.Spider):
    name = 'Baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = []
    keyword_dict = dict()

    def __init__(self):
        with open('data.txt') as f:
            lines = f.readlines()
            for line in lines:
                words = line.rstrip('\n').split(' ')
                ei = ExpertInfoItem(words[0], words[1], words[2])
                keyword = words[0] + "+" + words[1]
                url = "https://baike.baidu.com/search/none?word=" + \
                       keyword + \
                      "&pn=0&rn=10&enc=utf8"
                self.start_urls.append(url)
                self.keyword_dict[keyword] = ei

    def parse(self, response):
        url = response.url

        keyword = unquote(url.\
            lstrip("https://baike.baidu.com/search/none?word=").\
            rstrip("&pn=0&rn=10&enc=utf8"))

        # print("####: " + keyword )
        # print(self.keyword_dict[keyword].id)

        sel = Selector(response)
        contents = sel.xpath('//*[@id="body_wrapper"]/div[1]/dl/dd[1]/a').extract()
        for con in contents:
            if con.find("result-title"):
                next_url = con[30:].split(' ')[0].rstrip('"')
                yield Request(next_url, callback=self.parse2, meta={'keyword': keyword})

    def parse2(self, response):
        url = response.url
        keyword = response.meta['keyword']
        print(url)
        print(keyword)

