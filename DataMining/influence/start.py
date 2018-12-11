#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/28 15:41
# @Author  : zyk

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 19:23
# @Author  : zyk

import pymysql.cursors
from score import cal_score
from collections import Counter
import re


config = {
    'host': '111.205.121.93',
    'user': 'root',
    'password': 'root@buaa',
    'db': 'EDMS',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)
p = 1000
st = 8000
ed = 1093249

def select_persons():
    try:
        cursor = connection.cursor()
        # cur = st
        # while cur < ed:
        #     sql_person = 'select id from basic_info limit %s, %s'
        #     cursor.execute(sql_person, (cur, p))
        #     persons = cursor.fetchall()
        #     for person in persons:
        #         id = person['id']
        #         select_paper(id, cursor)
        #
        #     cur += p
        #     connection.commit()
        #     print(cur)
        id = '100000004875195'
        select_paper(id, cursor)
    finally:
        connection.close()

def select_paper(id,cursor):
    influence = 0
    score1 = 0
    score23 = 0
    score45 = 0
    fields = {}
    #一作
    sql_paper = "select * from paper_info where author1 = %s"
    cursor.execute(sql_paper, id)
    data = cursor.fetchall()

    for i in data:
        type = i['type']
        if type in ['期刊文章', '会议']:
            cates = i['category']
            if cates != '':
                include = i['data5']
                citation = 0
                if i['citation']:
                    citation = i['citation']
                score1 = cal_score(include, citation)

                cate_list = cates.split()
                for cate in cate_list:
                    match = re.search(r'([\w|\.|-]+)', cate)
                    if match:
                        tmp = match.group(1)
                        if tmp not in fields:
                            fields["%s" % tmp] = 0
                        fields["%s" % tmp] += score1
                        print(fields)
                print('-------------------')




    # # 二作三作
    # sql_paper = "select * from paper_info where author2 = %s or author3 = %s"
    # cursor.execute(sql_paper, (id,id))
    # data = cursor.fetchall()
    #
    # for i in data:
    #     type = i['type']
    #     if type in ['期刊文章', '会议']:
    #         cate = i['category']
    #         if cate != '':
    #             fields.append(cate[0])
    #         include = i['data5']
    #         citation = 0
    #         if i['citation']:
    #             citation = i['citation']
    #
    #         score23 += cal_score(include, citation)
    #
    # # 四作五作
    # sql_paper = "select * from paper_info where author4 = %s or author5 = %s"
    # cursor.execute(sql_paper, (id,id))
    # data = cursor.fetchall()
    #
    # for i in data:
    #     type = i['type']
    #     if type in ['期刊文章', '会议']:
    #         cate = i['category']
    #         if cate != '':
    #             fields.append(cate[0])
    #         include = i['data5']
    #         citation = 0
    #         if i['citation']:
    #             citation = i['citation']
    #         score45 += cal_score(include, citation)

    # influence = score1 + score23*0.8 + score45*0.6
    # field = ''
    # if fields != []:
    #     c = Counter(fields)
    #     field = c.most_common(1)[0][0]
    #
    # sql = 'INSERT INTO `influence_info` (`id`, `field`, `influ`) values(%s,%s,%s)'
    # cursor.execute(sql, (id, field, influence))

if __name__ == "__main__":
    select_persons()



