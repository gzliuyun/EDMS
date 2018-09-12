# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sys
from teacher.items import TeacherItem
from twisted.enterprise import adbapi

class TeacherPipeline(object):
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
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 指定异常处理方法
        query.addErrback(self.handle_error, item, spider) #处理异常


    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        self.dbpool.reconnect
        print(failure)

    def do_insert(self, cursor, item):
        id = item.get('id')
        name = item.get('name')
        university = item.get('uni')
        department = item.get('dep')
        profile = item.get('pro')
        image_url = item.get('img_url')
        info_url = item.get('info_url')
        sql = 'INSERT INTO expert_intro(id, name, university,department,profile,image_url,info_url) values' \
              '(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name =%s'
        cursor.execute(sql, (id, name, university, department, profile, image_url, info_url, name))

