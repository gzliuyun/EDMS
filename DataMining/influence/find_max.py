#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 21:05
# @Author  : zyk

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
cursor = connection.cursor()
fields = []
sql = 'select field from influence_info'

cursor.execute(sql)
data = cursor.fetchall()
for i in data:
    field = i['field']
    if field not in fields:
        fields.append(field)

sql_max = "SELECT influ from influence_info WHERE field = %s  ORDER BY influ DESC limit 2,1"
for f in fields:
    cursor.execute(sql_max, f)
    tmp = cursor.fetchone()
    max = tmp['influ']
    print(f+str(max))
    with open('max.txt','a') as file:
        file.write(f+':{}\n'.format(max))

