# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import sys
from ExpertBaike.items import SuppleItem
from twisted.enterprise import adbapi


class MysqlTwistedPipline(object):
    def __init__(self, ):
        dbparms = dict(
            host='111.205.121.93',
            db='EDMS',
            user='root',
            passwd='root@buaa',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor, # 指定 curosr 类型
            use_unicode=True,
        )
        # 指定擦做数据库的模块名和数据库参数参数
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    # 使用twisted将mysql插入变成异步执行
    def process_item(self, item, spider):
        # 指定操作方法和操作的数据
        if isinstance(item, SuppleItem):
            query = self.dbpool.runInteraction(self.do_insert_supplement, item)
            # 指定异常处理方法
            query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)

    def do_insert_supplement(self, cursor, item):

        id = item['id']
        resume = item['resume']
        pic_url = item['pic_url']
        sql = 'UPDATE basic_info(resume, img_url) VALUES (%s, %s) WHERE id = %s'
        cursor.execute(sql, (resume, pic_url, id))
