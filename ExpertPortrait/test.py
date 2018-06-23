# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import requests
import re
from ExpertPortrait.items import ExpertportraitItem


class TestSpider(scrapy.Spider):
    name = 'test'
    #allowed_domains = ['www.irtree.cn']
    #需要手动输入学院链接
    start_urls = ['http://www.irtree.cn/1710/author.aspx?idlevel=55957&organname=%E4%BA%BA%E6%96%87%E5%AD%A6%E9%99%A2%E5%8E%86%E5%8F%B2%E7%B3%BB&cpage=6']
    #start_urls = ['http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?pageIndex=1&id=1710']

    # def parse(self, response):
    #     sel =Selector(response)
    #     urls = sel.xpath('/html/body/div/ul/li/a/@href').extract()
    #     for url in urls[1:]:
    #         print('http://www.irtree.cn'+url)
    获取每个专家的url
    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//*[@id="author"]/div[1]/dl/dt/a[1]/@href').extract()
        for url in urls:
            item = ExpertportraitItem()
            item['expert_url'] = 'http://www.irtree.cn'+url
            item['expert_id'] = re.search('writer/(.*?)/rw_zp.aspx',url).group(1)
            yield Request(url=item['expert_url'], callback=self.parse_content, meta={'item': item})
        #翻页
        next_page = sel.xpath('//*[@id="author"]/div[2]/div[2]/span[2]/a[3]/@href').extract_first()
        if next_page:
            next_page = re.search(r"g_GetGotoPage\('(.*?)'\)", next_page).group(1)
            next_url=TestSpider.start_urls[0]+'&q=%7B"page"%3A"'+next_page+'"%7D'
            yield Request(next_url,callback=self.parse)

    #分析每个专家主页（发文量需要大于等于3）
    def parse_content(self, response):
        item = response.meta['item']
        sel = Selector(response)
        paper_count = sel.xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[3]/p/i/text()').extract_first()
        paper_count = int(paper_count.strip())
        if paper_count >= 3:
            name = sel.xpath('/html/body/div[2]/div/div[1]/h1/text()').extract_first()
            print(name)
