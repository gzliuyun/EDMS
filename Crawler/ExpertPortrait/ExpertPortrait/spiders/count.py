#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 19:09
# @Author  : zyk
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import re
from ExpertPortrait.items import person,paper,target,all
from urllib.parse import unquote


it = all()
it['total'] = 0
it['col_count'] = 0
it['page_count'] = 0
class CountSpider(scrapy.Spider):
    name = 'count'
    # allowed_domains = ['www.irtree.cn']
    # 需要手动输入学院链接
    start_urls = ['http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id=1710']

    def parse(self, response):
        url = response.url
        # print(url)

        # id = url.split('=')[-1]
        # id_index = school_ids.index(id)
        # school_name = school_names[id_index]
        #print(school_name+str(id_index)+' :'+id)
        item = person()
        item['university'] = '清华大学'
    #     #print(url + item['university'])
        sel = Selector(response)
        col_pages = sel.xpath('/html/body/div/div/span/text()').extract_first()
        col_pages = col_pages.split('/')[-1].strip()
        if int(col_pages):
            # for x in range(int(col_pages)):
            x = 10
            col_page = str(x+1)
            col_page_url = (url+'&pageIndex='+col_page)
            yield Request(col_page_url, callback=self.parse_getcol, meta={'item_l': item})

    # 进入每个学院
    def parse_getcol(self, response):
        item_l = response.meta['item_l']
        # print(response.url+item_l['university'])
        items = []
        sel = Selector(response)
        cols = sel.xpath('/html/body/div/ul/li/a')
        for col in cols[1:]:
            url = col.xpath('./@href').extract_first()
            item = target()
            item['university'] = item_l['university']
            col_url = 'http://www.irtree.cn' + url
            items.append(item)
        for item in items:
            yield Request(col_url, callback=self.parse_college, meta={'item_l': item}, dont_filter=False)


    # 获取每个专家的url
    def parse_college(self, response):
        item_l = response.meta['item_l']
        page_url = response.url
        print(page_url)

    # #     if page_url == 'http://www.irtree.cn/tootip.html':
    # #         university = item_l['university']
    # #         index = school_names.index(university)
    # #         id = school_ids[index]
    # #         for_url = 'http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id=' + id
    # #         with open('forbidden.txt', 'a', encoding='utf-8') as file:
    # #             file.write('没有权限:' +university)
    # #             file.write('\n')
    # #             file.write(for_url)
    # #             file.write('\n')
    # #     else:
    # #         print(page_url)
        sel = Selector(response)
        page_count = 0
        counts = sel.xpath('//*[@id="author"]/div[1]/dl/dd[3]/span[1]/span/a/text()').extract()
        for count in counts:
            tmp = int(count)
            if tmp >= 3:
                yield item_l


        #翻页
        next_page = sel.xpath('//*[@id="author"]/div[2]/div[2]/span[2]/a[3]/@href').extract_first()
        if next_page:
            next_page = re.search(r"g_GetGotoPage\('(.*?)'\)", next_page).group(1)
            next_url = page_url.split('&q=%7B%22page')[0]+'&q=%7B"page"%3A"'+next_page+'"%7D'
            yield Request(next_url, callback=self.parse_college,  meta={'item_l':item_l})
        # else:
        #     it['col_count'] += it['page_count']
            #it['total'] += it['col_count']
            # print(it['total'])