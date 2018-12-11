#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 19:23
# @Author  : zyk

import math
import pymysql.cursors
from score import cal_score
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
st = 0
ed = 1093249

def select_persons():
    try:
        cursor = connection.cursor()
        cur = st
        while cur < ed:
            sql_person = 'select id, field from influence_info limit %s, %s'
            cursor.execute(sql_person, (cur, p))
            persons = cursor.fetchall()
            for person in persons:
                id = person['id']
                field = person['field']
                select_paper(id, field, cursor)
            cur += p
            connection.commit()
            print(cur)
    finally:
        connection.close()


def select_paper(id, field, cursor):
    influ_time = {}
    for i in range(1989, 2019):
         influ_time["influ_%s" % i] = 0

    #一作
    sql_paper = "select * from paper_info where author1 = %s"
    cursor.execute(sql_paper, id)
    data = cursor.fetchall()

    for i in data:
        type = i['type']
        if type in ['期刊文章', '会议']:
            include = i['data5']
            citation = 0
            if i['citation']:
                citation = i['citation']
            date = i['date']
            for i in range(1989, 2019):
                if date.startswith(str(i)):
                    influ_time["influ_%s" % i] += cal_score(include, citation)




    # # 二作三作
    sql_paper = "select * from paper_info where author2 = %s or author3 = %s"
    cursor.execute(sql_paper, (id, id))
    data = cursor.fetchall()

    for i in data:
        type = i['type']
        if type in ['期刊文章', '会议']:
            include = i['data5']
            citation = 0
            if i['citation']:
                citation = i['citation']
            date = i['date']
            for i in range(1989, 2019):
                if date.startswith(str(i)):

                    influ_time["influ_%s" % i] += 0.8 * cal_score(include, citation)

    # 四作五作
    sql_paper = "select * from paper_info where author4 = %s or author5 = %s"
    cursor.execute(sql_paper, (id, id))
    data = cursor.fetchall()

    for i in data:
        type = i['type']
        if type in ['期刊文章', '会议']:
            include = i['data5']
            citation = 0
            if i['citation']:
                citation = i['citation']
            date = i['date']
            for i in range(1989, 2019):
                if date.startswith(str(i)):
                    influ_time["influ_%s" % i] += 0.6 * cal_score(include, citation)


    influ_time['influ_2018'] = 3 * influ_time['influ_2018']

    first = 0
    latest = 0
    for x in range(1989, 2019):
        if influ_time['influ_%s' % x] != 0:
            first = x
            break
    for y in range(2018, 1988, -1):
        if influ_time['influ_%s' % y] != 0:
            latest = y
            break
    longth = latest - first + 1

    if first != 0:
        for key in influ_time:
            influ_time[key] = longth * influ_time[key]

        for l in range(first+1, 2019):
            influ_time['influ_%s' % l] = 0.5 * influ_time['influ_%s' % (l-1)] + 0.5 * influ_time['influ_%s' % l]


        for m in range(first, 2019):
            influ_time['influ_%s' % m] = normalization(influ_time['influ_%s' % m], field)

    influ_time['id'] = id


    keys = ','.join(influ_time.keys())
    values = ','.join(['%s']*len(influ_time))
    sql = 'insert into  `influ_time` ({keys}) VALUE ({values})'.format(keys=keys, values=values)
    cursor.execute(sql, tuple(influ_time.values()))



def normalization(influ, field):
    with open('max.txt','r') as file:
        tmp = file.readlines()
        for t in tmp:
            f = t.split(':')[0]
            if field == f:
                max = float(t.split(':')[1].rstrip())
                if influ < 1:
                    update_influ = 0
                elif influ == 1:
                    update_influ = 1
                else:
                    update_influ = math.log10(influ) / math.log10(max) * 100
                if update_influ > 100:
                    update_influ = 100
    return update_influ





if __name__ == "__main__":
    select_persons()




