# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['ctti.nju.edu.cn']
    start_urls = ['https://ctti.nju.edu.cn/CTTI/professor/toSearch.do']

    def parse(self, response):
        print(response.url)
