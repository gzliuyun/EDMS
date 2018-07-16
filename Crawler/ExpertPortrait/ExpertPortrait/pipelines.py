# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sys
from ExpertPortrait.items import paper,person
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
        if isinstance(item, person):
            query = self.dbpool.runInteraction(self.do_insert_person, item)
            # 指定异常处理方法
            query.addErrback(self.handle_error, item, spider) #处理异常
        if isinstance(item, paper):
            query = self.dbpool.runInteraction(self.do_insert_paper, item)
            # 指定异常处理方法
            query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)

    def do_insert_person(self, cursor, item):
        expert_id = item.get('expert_id')
        expert_name = item.get('expert_name')
        university = item.get('university')
        college = item.get('college')
        theme_list = item.get('theme_list')
        sub_list = item.get('sub_list')
        expert_url = item.get('expert_url')
        amount1 = item.get('amount1')
        amount2 = item.get('amount2')
        h_index = item.get('h_index')
        core = item.get('core')
        cssci = item.get('cssci')
        rdfybkzl = item.get('rdfybkzl')
        co_experts = item.get('co_experts')
        co_agencies = item.get('co_agencies')
        sql_bas = 'INSERT INTO basic_info(id, name, university, college,theme_list,sub_list, url1) values(%s,%s,%s,%s,' \
                  '%s,%s,%s) ON DUPLICATE KEY UPDATE name =%s'
        sql_aca = 'INSERT INTO academic_info(id, name, amount1, amount2, h_index, core, cssci, rdfybkzl,co_expert,' \
                  'co_agency) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name =%s'
        cursor.execute(sql_bas, (expert_id, expert_name, university, college, theme_list, sub_list, expert_url, expert_name))
        cursor.execute(sql_aca, (expert_id, expert_name, amount1, amount2, h_index, core, cssci, rdfybkzl, co_experts, co_agencies, expert_name))

    def do_insert_paper(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        paper_id = item.get('paper_id')
        paper_title = item.get('paper_title')
        paper_type = item.get('paper_type')
        source = item.get('source')
        abstract = item.get('abstract')
        date = item.get('date')
        keyword = item.get('keyword')
        p_authors = item.get('p_authors')
        p_author1 = item.get('p_author1')
        p_author2 = item.get('p_author2')
        p_author3 = item.get('p_author3')
        p_author4 = item.get('p_author4')
        p_author5 = item.get('p_author5')
        sql_pap1 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `date`, `abstract`, `keyword`,`authors`,`author1`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `author1`= %s'
        sql_pap2 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `date`, `abstract`, `keyword`,`authors`, `author2`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `author2`= %s'
        sql_pap3 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `date`, `abstract`, `keyword`,`authors`, `author3`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `author3`= %s'
        sql_pap4 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `date`, `abstract`, `keyword`,`authors`, `author4`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `author4`= %s'
        sql_pap5 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `date`, `abstract`, `keyword`,`authors`, `author5`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `author5`= %s'

        if p_author1 != '':
            cursor.execute(sql_pap1,(paper_id, paper_title, paper_type, source, date, abstract, keyword, p_authors, p_author1, p_author1))

        if p_author2 != '':
            cursor.execute(sql_pap2, (paper_id, paper_title, paper_type, source, date, abstract, keyword, p_authors, p_author2, p_author2))
        if p_author3 != '':
            cursor.execute(sql_pap3, (paper_id, paper_title, paper_type, source, date, abstract, keyword, p_authors, p_author3, p_author3))
        if p_author4 != '':
            cursor.execute(sql_pap4, (paper_id, paper_title, paper_type, source, date, abstract, keyword, p_authors, p_author4, p_author4))
        if p_author5 != '':
            cursor.execute(sql_pap5, ( paper_id, paper_title, paper_type, source, date, abstract, keyword, p_authors, p_author5, p_author5))


