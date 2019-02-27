# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
from ExpertBaike.items import ExpertInfoItem, SuppleItem
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

        keyword = unquote(url. \
                          lstrip("https://baike.baidu.com/search/none?word="). \
                          rstrip("&pn=0&rn=10&enc=utf8"))

        # print("####: " + keyword )
        # print(self.keyword_dict[keyword].id)

        sel = Selector(response)
        contents = sel.xpath('//*[@id="body_wrapper"]/div[1]/dl/dd[1]/a').extract()

        ckword1 = "result-title"
        ckword2 = "<em>" + keyword.split('+')[0] + "</em>"
        ckword3 = "_百度百科"

        for con in contents:
            if con.find(ckword1) and con.find(ckword2) and con.find(ckword3) and (len(con) > 30):
                # 有搜索结果
                # 搜索结果中有专家姓名
                # 搜索结果是指向百度百科
                next_url = con[30:].split(' ')[0].rstrip('"')
                if next_url.find("/item/"):  # 百度百科url的必有子串
                    yield Request(next_url, callback=self.parse2, meta={'keyword': keyword})

    def parse2(self, response):
        print("---"*20)
        url = response.url
        keyword = response.meta['keyword']
        # print(url)
        if keyword in self.keyword_dict:
            id = self.keyword_dict[keyword].id
            school = keyword.split('+')[0]
            name = keyword.split('+')[1]
            print(name, school, id)
            sel = Selector(response)
            info_list = sel.xpath('//*[@class="basicInfo-item value"]//text()').extract()
            ck_school = False
            for info in info_list:
                if info.find(school):
                    ck_school = True
                    break
            if ck_school:
                resume_list = sel.xpath('//*[@class="para"]//text()').extract()
                resume = ""
                for tmp in resume_list:
                    resume += tmp
                # print(resume)
                pic_url = "https://baike.baidu.com" + \
                          sel.xpath('//*[@class="summary-pic"]/a/@href').extract_first()
                # print(pic_url)
                item = SuppleItem()
                item['id'] = id
                item['resume'] = resume
                item['pic_url'] = pic_url
                yield item
