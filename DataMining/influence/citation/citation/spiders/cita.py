# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
import pymysql.cursors
from citation.items import CitationItem



class CitaSpider(scrapy.Spider):
    name = 'cita'
    # allowed_domains = []
    start_urls = []

    def __init__(self):
        config = {
            'host': '111.205.121.93',
            'user': 'root',
            'password': 'root@buaa',
            'db': 'EDMS',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }

        db = pymysql.connect(**config)
        cur = db.cursor()
        sql = 'select paper_id from paper_info where citation is NULL '
        # sql = 'select paper_id from paper_info'
        cur.execute(sql)
        data = cur.fetchall()
        for i in data:
            id = i['paper_id']
            url = 'http://www.irtree.cn/Template/t5/ajax/Article_Relative_Graph.ashx?id='+id+'_1710'
            self.start_urls.append(url)


    def parse(self, response):
        sel = Selector(response)
        tmp = sel.xpath('/html/body').extract()[0]
        cita = '0'
        num = re.search(r'引证文献\",\r\n      \"relNum\": (.*?),\r\n',tmp).group(1)
        if num:
            cita = num
        item = CitationItem()
        item['cita'] = cita
        id = response.url.split('=')[-1].split('_')[0]
        item['id'] = id
        yield item
