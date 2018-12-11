#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/30 9:55
# @Author  : zyk


import math

import pymysql.cursors


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
st = 38000

ed = 1093249

def select_persons():
    try:
        cursor = connection.cursor()
        cur = st
        while cur < ed:
            sql_person = 'select * from influence_info limit %s, %s'
            cursor.execute(sql_person, (cur, p))
            persons = cursor.fetchall()
            for person in persons:
                id = person['id']
                field = person['field']
                influ = person['influ']
                normalization(id, field, influ, cursor)

            cur += p
            connection.commit()
            print(cur)
    finally:
        connection.close()

def normalization(id,field,influ,cursor):
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
    # print(id)
    sql_update = 'update influence_info set influ = %s  where id = %s'
    cursor.execute(sql_update, (update_influ, id))


if __name__ == "__main__":
    select_persons()
