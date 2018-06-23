# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import requests
import re
from ExpertPortrait.items import ExpertportraitItem
from urllib.parse import unquote

school_names = ['清华大学', '浙江大学', '北京大学', '吉林大学', '上海交通大学', '华中科技大学', '武汉大学', '四川大学',
                '南京大学', '山东大学', '华南理工大学', '复旦大学', '同济大学', '哈尔滨工业大学', '中山大学', '天津大学',
                '东南大学', '中南大学', '北京师范大学', '大连理工大学', '郑州大学', '中国人民大学', '西安交通大学', '南开大学',
                '华东师范大学', '苏州大学', '厦门大学', '重庆大学', '南京师范大学', '湖南大学', '武汉理工大学',
                '中国科学技术大学', '东北大学', '北京航空航天大学', '电子科技大学', '华中师范大学', '西南交通大学',
                '西北工业大学', '暨南大学', '上海大学', '西南大学', '兰州大学', '广西大学', '北京理工大学', '北京交通大学',
                '合肥工业大学', '中国农业大学', '中国矿业大学', '南昌大学', '华北电力大学', '华南师范大学', '北京科技大学',
                '南京理工大学', '太原理工大学', '河海大学', '湖南师范大学', '西安电子科技大学', '西北农林科技大学',
                '北京工业大学', '陕西师范大学', '北京邮电大学', '南京农业大学', '南京航空航天大学', '华东理工大学',
                '哈尔滨工程大学', '东北师范大学', '中国海洋大学', '安徽大学', '中国地质大学', '江南大学', '贵州大学',
                '云南大学', '西北大学', '福州大学', '华中农业大学', '东华大学', '长安大学', '北京林业大学', '东北林业大学',
                '西南财经大学', '辽宁大学', '北京化工大学', '中南财经政法大学', '上海财经大学', '东北农业大学',
                '河北工业大学', '内蒙古大学', '新疆大学', '石河子大学', '大连海事大学', '对外经济贸易大学', '北京中医药大学',
                '四川农业大学', '中国政法大学', '宁夏大学', '中央民族大学', '中央财经大学', '延边大学', '中国石油大学（北京）',
                '天津医科大学', '中国传媒大学', '中国药科大学', '中国矿业大学（北京）', '海南大学', '中国石油大学',
                '北京体育大学', '上海外国语大学', '青海大学', '西藏大学', '北京外国语大学', '中央音乐学院', '哈尔滨工业大学(威海)']
school_ids = ['1710', '2507', '426', '1194', '1965', '996', '2054', '2006', '1112', '1923', '2151', '325', '2434', '732',
              '3112', '2418', '497', '3627', '434', '287', '2525', '3078', '2066', '1122', '990', '2012', '2982', '3120',
              '1310', '969', '4020', '3323', '86', '1553', '843', '1403', '1890', '2076', '1204', '2826', '2945', '1264',
              '535', '1559', '1556', '745', '3193', '2558', '1508', '3722', '1397', '612', '1520', '2890', '199', '1170',
              '2925', '2078', '1549', '3412', '257', '1522', '1304', '1177', '168', '846', '4109', '203', '3589', '1423',
              '150', '2489', '2074', '514', '998', '494', '1578', '614', '490', '1888', '1474', '607', '4146', '2337',
              '666', '2098', '1291', '2991', '3937', '286', '850', '42', '2874', '3107', '1327', '3119', '3634', '3265',
              '4139', '2903', '2541', '3213', '4113', '1674', '63537', '1565', '3432', '3875', '2942', '621', '2587', '92945']
keywords = ['经济','文','医','法','政治'
                             ''
                             '']

class TestSpider(scrapy.Spider):
    name = 'test'
    #allowed_domains = ['www.irtree.cn']
    #需要手动输入学院链接
    #start_urls = ['http://www.irtree.cn/1710/author.aspx?idlevel=55957&organname=%E4%BA%BA%E6%96%87%E5%AD%A6%E9%99%A2%E5%8E%86%E5%8F%B2%E7%B3%BB&cpage=6']
    start_urls = ['http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id=1710']

    #得到每个学校里院系所导航页面的页数
    def parse(self, response):
        item = ExpertportraitItem()
        id = TestSpider.start_urls[0].split('=')[-1]
        id_index = school_ids.index(id)
        school_name = school_names[id_index]
        item['university'] = school_name
        sel =Selector(response)
        col_pages = sel.xpath('/html/body/div/div/span/text()').extract_first()
        col_pages = col_pages.split('/')[-1].strip()
        for x in range(int(col_pages)):
            col_page = str(x+1)
            col_page_url=(TestSpider.start_urls[0]+'&pageIndex='+col_page)
            yield Request(col_page_url, callback=self.parse_getcol, meta = {'item':item})

    #进入每个学院
    def parse_getcol(self, response):
        item = response.meta['item']
        sel = Selector(response)
        cols = sel.xpath('/html/body/div/ul/li/a')
        for col in cols[1:]:
            url = col.xpath('./@href').extract_first()
            col_name_code = re.search('organname=(.*?)&cpage',url).group(1)
            col_name = unquote(col_name_code)
            for keyword in keywords:
                if keyword in col_name:
                    item['college'] = col_name
                    print(item['university']+' '+item['college'])
    #         col_url = 'http://www.irtree.cn'+url
    #         yield Request(col_url, callback=self.parse_college, meta = {'item':item})
    #
    # #获取每个专家的url
    # def parse_college(self, response):
    #     item = response.meta['item']
    #     sel = Selector(response)
    #     urls = sel.xpath('//*[@id="author"]/div[1]/dl/dt/a[1]/@href').extract()
    #     for url in urls:
    #         item['expert_url'] = 'http://www.irtree.cn'+url
    #         item['expert_id'] = re.search('writer/(.*?)/rw_zp.aspx',url).group(1)
    #         yield Request(url=item['expert_url'], callback=self.parse_content, meta={'item': item})
    #     #翻页
    #     next_page = sel.xpath('//*[@id="author"]/div[2]/div[2]/span[2]/a[3]/@href').extract_first()
    #     if next_page:
    #         next_page = re.search(r"g_GetGotoPage\('(.*?)'\)", next_page).group(1)
    #         next_url=TestSpider.start_urls[0]+'&q=%7B"page"%3A"'+next_page+'"%7D'
    #         yield Request(next_url,callback=self.parse_college)
    #
    # #分析每个专家主页（发文量需要大于等于3）
    # def parse_content(self, response):
    #     item = response.meta['item']
    #     sel = Selector(response)
    #     paper_count = sel.xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[3]/p/i/text()').extract_first()
    #     paper_count = int(paper_count.strip())
    #     if paper_count >= 3:
    #         name = sel.xpath('/html/body/div[2]/div/div[1]/h1/text()').extract_first()
    #         print(name)
