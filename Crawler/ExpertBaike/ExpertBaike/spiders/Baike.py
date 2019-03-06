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
        with open('data4.txt', encoding='utf-8') as f:
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
        ckword2 = "<em>" + keyword.split('+')[1] + "</em>"
        ckword3 = "_百度百科"
        # print(ckword1, ckword2, ckword3)

        for con in contents:
            st = con.find(ckword2)
            if st < 0:
                continue
            if con[st-7:st] != 'blank">':
                continue
            # 搜索结果中有专家姓名且在第一位
            if (con.find(ckword1) > 0) and \
                    (con.find(ckword3) > 0) and \
                    (len(con) > 30):
                # 有搜索结果
                # 搜索结果是指向百度百科
                next_url = con[30:].split(' ')[0].rstrip('"')
                if next_url.find("/item/"):  # 百度百科url的必有子串
                    yield Request(next_url, callback=self.parse2, meta={'keyword': keyword})

    def parse2(self, response):
        url = response.url
        keyword = response.meta['keyword']
        # print(keyword)
        # print(url)
        if keyword in self.keyword_dict:
            id = self.keyword_dict[keyword].id
            school = keyword.split('+')[0]
            name = keyword.split('+')[1]
            # college = keyword.split('+')[2]
            sel = Selector(response)
            # info_list = sel.xpath('//*[@class="basicInfo-item value"]//text()').extract()
            # print(info_list)
            # ck_school = False
            # for info in info_list:
            #     if info.find(school) > 0:
            #         print(info.find(school))
            #         print(school)
            #         ck_school = True
            #         break
            # if ck_school:
            resume_list = sel.xpath('//*[@class="para"]//text()').extract()
            resume = ""
            for tmp in resume_list:
                tmp = tmp.lstrip("\xa0\n").rstrip("\n").strip()
                if len(tmp) > 0:
                    tmp = tmp + "<br />"
                resume += tmp
            resume.replace("<br />。", "")
            resume.replace("<br />，", "")
            resume.replace("<br />[1]", "")
            # print(resume)
            if (resume.find(school) > 0):
                print("---" * 20)
                print(name, school, id)
                suffix = sel.xpath('//*[@class="summary-pic"]/a/@href').extract_first()
                # print(suffix)
                pic_url = ""
                if suffix != None:
                    pic_url = "https://baike.baidu.com" + suffix
                item = SuppleItem()
                item['id'] = id
                item['resume'] = resume
                item['pic_url'] = pic_url

                with open("record.txt", "a+", encoding='utf-8') as f:
                    # print("xixixi")
                    str = id + " " + name + " " + school + " " + url + "\n"
                    f.write(str)
                f.close()

                if len(pic_url) > 0:
                    yield Request(pic_url, callback=self.parse_pic, meta={'item': item})
                else:
                    yield item

    def parse_pic(self, response):
        url = response.url
        sel = Selector(response)
        item = response.meta['item']

        # print(item['id'])

        pic_url = sel.xpath('//*[@id="imgPicture"]/@src').extract_first()
        # print(pic_url)

        if len(pic_url) > 0:
            item['pic_url'] = pic_url

        yield item
