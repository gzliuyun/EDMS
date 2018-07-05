# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sys
from ExpertPortrait.items import paper,person

class Expertportrait1Pipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(host='111.205.121.93',user='root',password = 'root@buaa',port=3306,db='EDMS',charset="utf8")
        cursor = db.cursor()

        if isinstance(item, person):
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
            sql_bas = 'INSERT INTO basic_info(id, name, university, college,theme_list,sub_list, url1) values(%s,%s,%s,%s,%s,%s,%s)'
            sql_aca = 'INSERT INTO academic_info(id, name, amount1, amount2, h_index, core, cssci, rdfybkzl,co_expert,' \
                      'co_agency) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                if cursor.execute(sql_bas, (expert_id, expert_name, university, college, theme_list, sub_list, expert_url)):
                    db.commit()
                if cursor.execute(sql_aca, (expert_id, expert_name, amount1, amount2, h_index, core, cssci, rdfybkzl, co_experts, co_agencies)):
                    db.commit()
            except:
                info = sys.exc_info()
                print(info[0], ":", info[1])
                db.rollback()

        if isinstance(item, paper):
            paper_id = item.get('paper_id')
            paper_title = item.get('paper_title')
            paper_type = item.get('paper_type')
            source = item.get('source')
            abstract = item.get('abstract')
            keyword = item.get('keyword')
            p_author1 = item.get('p_author1')
            p_author2 = item.get('p_author2')
            p_author3 = item.get('p_author3')
            p_author4 = item.get('p_author4')
            p_author5 = item.get('p_author5')
            sql_pap1 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author1`)' \
                       'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author1`= %s'
            sql_pap2 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author2`)' \
                       'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author2`= %s'
            sql_pap3 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author3`)' \
                       'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author3`= %s'
            sql_pap4 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author4`)' \
                       'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author4`= %s'
            sql_pap5 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author5`)' \
                       'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author5`= %s'
            try:
                if p_author1 != '':
                    if cursor.execute(sql_pap1,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author1, p_author1)):
                        db.commit()
                if p_author2 != '':
                    if cursor.execute(sql_pap2,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author2, p_author2)):
                        db.commit()
                if p_author3 != '':
                    if cursor.execute(sql_pap3,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author3, p_author3)):
                        db.commit()
                if p_author4 != '':
                    if cursor.execute(sql_pap4,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author4, p_author4)):
                        db.commit()
                if p_author5 != '':
                    if cursor.execute(sql_pap5,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author5, p_author5)):
                        db.commit()
            except:
                info = sys.exc_info()
                print(info[0], ":", info[1])
                db.rollback()





