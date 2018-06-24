# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import requests
import MySQLdb
import sys
from ExpertPortrait.items import ExpertItem
from ExpertPortrait.items import PaperItem

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.irtree.cn']
    start_urls = []

    def __init__(self):
        file = open('starturls.txt')
        url_list = file.readlines()
        file.close()
        for url in url_list:
            self.start_urls.append(url.rstrip('\n').split(' ')[0])

    def parse(self, response):
        expert = ExpertItem()
        paper = PaperItem()

        print("##############")
        sel = Selector(response)
        ## 维普主页
        url = response.url
        # print(url)
        expert['expert_url'] = url

        ## 学者ID 学校ID
        id = url.lstrip("http://www.irtree.cn/").rstrip("/rw_zp.aspx").split("/writer/")[1].strip()
        school_id = url.lstrip("http://www.irtree.cn/").rstrip("/rw_zp.aspx").split("/writer/")[0].strip()
        # print(school_id)
        # print(id)
        expert['university'] = school_id
        expert['expert_id'] = id

        ### 姓名
        name = sel.xpath('//*[@class="summary"]/h1/text()').extract_first().strip()
        # print(name)
        expert['expert_name'] = name

        ## 研究主题
        themes = sel.xpath('//*[@class="summary"]/p[4]/text()').extract_first().strip()
        theme_list = themes.lstrip(" 研究主题：").rstrip("    ").split("    ")
        # print(theme_list)
        # expert['theme_list'] = theme_list

        ## 研究学科
        subs = sel.xpath('//*[@class="summary"]/p[5]/text()').extract_first()
        sub_list = subs.lstrip(" 研究学科：").rstrip("    ").split("    ")
        # print(sub_list)
        # expert['sub_list'] = sub_list

        ## 发文量
        amount1 = sel.xpath('//*[@class="search_count"]/p/i/text()').extract_first().replace(' ', '').replace('\n', '')
        amount1 = amount1.lstrip('\r')
        # print(amount1)
        expert['amount1'] = amount1

        ## 被引量
        amount2 = sel.xpath('//*[@class="summary"]/p[6]/span[2]/i/a/text()').extract_first().replace(',', '')
        # print(amount2)
        expert['amount2'] = amount2

        ## H指数
        h_index = sel.xpath('//*[@class="summary"]/p[6]/span[3]/i/text()').extract_first()
        # print(h_index)
        expert['h_index'] = h_index

        ## 北大核心
        core = sel.xpath('//*[@class="summary"]/p[6]/span[4]/@title').extract_first().lstrip("北大核心:")
        # print(core)
        ## 中文社会科学引文索引
        cssci = sel.xpath('//*[@class="summary"]/p[6]/span[5]/@title').extract_first().lstrip("中文社会科学引文索引:")
        # print(cssci)
        expert['cssci'] = cssci

        ## 人大复印报刊资料
        rdfybkzl = sel.xpath('//*[@class="summary"]/p[6]/span[6]/@title').extract_first().lstrip("人大复印报刊资料:")
        # self.load_data1(url, id, name, theme_list, sub_list, amount1, amount2, h_index, core, cssci, rdfybkzl)
        expert['rdfybkzl'] = rdfybkzl

        ## 总页数
        pagenum = int(sel.xpath('//*[@class="pages"]/span[1]/text()').extract_first().lstrip('共').rstrip('页'))
        # print(pagenum)
        # for i in range(1, pagenum+1):
        ### TEST ###
        for i in range(1, 2):
            paper_url = url + "?q=%7B\"page\"%3A\"" + str(i) + "\"%7D"
            # print(paper_url)
            yield Request(paper_url, callback=lambda response, id=id: self.parse2(response, id))

        tp_url = url.rstrip("zp.aspx") + "tp.aspx"
        yield Request(tp_url, callback=lambda response, id=id: self.parse4(response, id))

    def parse2(self, response, id):
        url = response.url
        # print(url, id)
        sel = Selector(response)
        urls = sel.xpath('//*[@class="search_list"]//dt//@href').extract()

        ## 所有论文链接
        url_list = []
        # for url in urls:
        #     tmp = "http://www.irtree.cn" + url
        #     url_list.append(tmp)
        #     yield Request(tmp, callback=lambda response, id=id: self.parse3(response, id))

        ### TEST ###
        tmp = "http://www.irtree.cn" + urls[0]
        yield Request(tmp, callback=lambda response, id=id: self.parse3(response, id))
        ### TEST ###

        # print(url_list)

    def parse3(self, response, id):
        sel = Selector(response)
        url = response.url
        # print(url, id)
        ## 论文ID
        paper_id = url.lstrip("http://www.irtree.cn/").rstrip("/article_detail.aspx").split("/articles/")[1].strip()
        # print(paper_id)
        title = sel.xpath('//*[@class="summary"]/h1/text()').extract_first().strip()
        # print(title)
        ## 文献类型
        type = sel.xpath('//*[@class="article_detail "]/p[1]/text()').extract_first().strip()
        # print(type)
        ## 出处
        source = sel.xpath('//*[@class="article_detail "]/p[5]/text()').extract_first().strip()
        # print(source)
        ## 收录情况
        cover_info = sel.xpath('//*[@class="article_detail "]/p[12]/text()').extract_first().strip()
        # print(cover_info)
        ## 摘要
        abstract = sel.xpath('//*[@class="article_detail "]/p[13]/text()').extract_first().strip()
        # print(abstract)
        ## 关键词
        keywords = sel.xpath('//*[@class="article_detail "]/p[14]/text()').extract()
        # for kw in keywords:
        #     print(kw)
        ## 作者
        authors = sel.xpath('//*[@class="article_detail "]/p[2]/text()').extract()
        # for a in authors:
        #     print(a)

        print("---------DETAIL---------")
        detail_list = sel.xpath('//*[@class="article_detail "]/p/text()').extract()
        tag_list = sel.xpath('//*[@class="article_detail "]/p/strong/text()').extract()
        print(len(detail_list))
        print(detail_list)
        print(len(tag_list))
        print(tag_list)


    def parse4(self, response, id):
        sel = Selector(response)
        url = response.url
        print(url, id)
        ## 合作学者
        co_experts_urls = sel.xpath('//*[@class="list_writer"]//dt//@href').extract()
        co_experts_list = []
        for url in co_experts_urls:
            tmp = url.rstrip("/rw.aspx").split("/writer/")[1]
            co_experts_list.append(tmp)
        # print(co_experts_list)
        ## 合作机构
        co_angency = sel.xpath('//*[@class="list organ"]//li//@title').extract()
        # print(co_angency)

    def load_data1(self, url, id, name, theme_list, sub_list, amount1, amount2, h_index, core, cssci, rdfybkzl):
        print("--------------  load_data1  --------------")
        try:
            conn = MySQLdb.Connect(
                host='111.205.121.93',
                user='root',
                passwd='root@buaa',
                db='EDMS',
                port=3306,
                charset="utf8"
            )
            cur = conn.cursor()
            head1 = "INSERT INTO academic_info(`id`,`name`,`amount1`,`amount2`,`h_index`,`core`,`cssci`,`rdfybkzl`) VALUES "
            sql1 = head1 + "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            id, name, amount1, amount2, h_index, core, cssci, rdfybkzl)
            print(sql1)
            # cur.execute(sql)
            # conn.commit()
            # conn.close()

        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
