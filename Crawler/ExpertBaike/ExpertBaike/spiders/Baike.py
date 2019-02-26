# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import re
from urllib.parse import unquote


class BaikeSpider(scrapy.Spider):
    name = 'Baike'
    allowed_domains = ['www.baidu.com']
    start_urls = []

    def __init__(self):
        with open('data.txt') as f:
            lines = f.readlines()
            for line in lines:
                words = line.rstrip('\n').split(' ')
                url = "https://baike.baidu.com/search/none?word=" + \
                      words[0] + "+" + words[1] + \
                      "&pn=0&rn=10&enc=utf8"
                # print(url)
                self.start_urls.append(url)

    def parse(self, response):
        url = response.url
        # print(url)
        sel = Selector(response)
        print("-------------")
        contents = sel.xpath('//*[@id="body_wrapper"]/div[1]/dl/dd[1]/a').extract()
        for con in contents:
            baike_url = re.sub(r"(https://.+?)/.*", lambda x: x.group(1), con)[30:]
            print(baike_url, baike_url[0])
            if baike_url[0] == 'h':
                yield Request(baike_url, callback=self.parse2)

    def parse2(self, response):
        print("~~~~~~~")
        url = response.url
        print(url)

