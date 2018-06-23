# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sys

class ExpertportraitPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(host='111.205.121.93',user='root',password = 'root@buaa',port=3306,db='EDMS',charset="utf8")
        cursor = db.cursor()
        sql_bas = 'INSERT INTO basic_info(id, name, university, college, url1) values(%s,%s,%s,%s,%s)'
        sql_aca = 'INSERT INTO academic_info(id, name, amount1, amount2, h_index, core, cssci, rdfybkzl,co_expert,' \
                  'co_agency) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_pap = 'INSERT INTO paper_info(paper_id, title, type, source, cover_info, abstract, keyword, author1,' \
                  'author2, author3) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            if cursor.execute(sql_bas, (item['expert_id'], item['expert_name'],item['university'],item['college'],
                                        item['expert_url'])):
                db.commit()
            if cursor.execute(sql_aca, (item['expert_id'], item['expert_name'], item['amount1'], item['amount2'],
                                        item['h_index'],item['core'],item['cssci'],item['rdfybkzl'],item['co_expert'],
                                        item['co_agency'])):
                db.commit()
            if  cursor.execute(sql_pap,(item['paper_id'],item['paper_title'],item['paper_type'],item['source'],
                                        item['cover_info'],item['abstract'],item['keyword'],item['p_author1'],
                                        item['p_author2'],item['p_author3'])):
                db.commit()
        except:
            info = sys.exc_info()
            print(info[0], ":", info[1])
            db.rollback()


