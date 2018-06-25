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
        paper_id = item.get('paper_id')
        paper_title = item.get('paper_title')
        paper_type = item.get('paper_type')
        source = item.get('source')
        abstract = item.get('abstract')
        keyword = item.get('keyword')
        p_author1 = item.get('p_author1')
        p_author2 = item.get('p_author2')

        sql_bas = 'INSERT INTO basic_info(id, name, university, college,theme_list,sub_list, url1) values(%s,%s,%s,%s,%s,%s,%s)'
        sql_aca = 'INSERT INTO academic_info(id, name, amount1, amount2, h_index, core, cssci, rdfybkzl,co_expert,' \
                  'co_agency) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_pap1 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author1`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author1`= %s'
        sql_pap2 = 'INSERT INTO `paper_info`(`paper_id`, `title`, `type`, `source`, `abstract`, `keyword`, `author2`)' \
                   'VALUES (%s,%s,%s,%s,%s,%s,%s) ON duplicate KEY UPDATE `author2`= %s'
        try:
            if cursor.execute(sql_bas, (item['expert_id'], item['expert_name'],item['university'],item['college'],
                                        item['theme_list'],item['sub_list'],item['expert_url'])):
                db.commit()
            if cursor.execute(sql_aca, (item['expert_id'], item['expert_name'], item['amount1'], item['amount2'],
                                        item['h_index'],item['core'],item['cssci'],item['rdfybkzl'],item['co_experts'],
                                        item['co_agencies'])):
                db.commit()

            if p_author1 != '':
                if cursor.execute(sql_pap1,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author1, p_author1)):
                    print('success')
                    db.commit()
            if p_author2 != '':
                if cursor.execute(sql_pap2,(paper_id, paper_title, paper_type, source, abstract, keyword, p_author2, p_author2)):
                    print('success')
                    db.commit()
        except:
            info = sys.exc_info()
            print(info[0], ":", info[1])
            db.rollback()


