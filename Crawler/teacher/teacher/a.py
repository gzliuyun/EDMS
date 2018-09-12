#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 18:29
# @Author  : zyk

import pymysql
schools = []
counts = []
db = pymysql.connect(host='111.205.121.93',user='root',password = 'root@buaa',port=3306,db='EDMS',charset="utf8")
cursor = db.cursor()
# cursor.execute("delete from basic_info where university=%s", '电子科技大学')
# db.commit()
cursor.execute("select university from expert_intro")
data = cursor.fetchall()
for i in data:
    x=i[0]
    if x not in schools:
        schools.append(x)
        counts.append(1)
    else:
        index = schools.index(x)
        counts[index]+=1

unfinished = []
with open('total.txt','r',encoding='utf-8') as f:
    tmp = f.readlines()
    for t in tmp:
        for i in range(len(schools)):
            if schools[i] == t.split()[0] and 1.5*counts[i]<int(t.split()[-1]):
                unfinished.append(schools[i])

#
# unfinished = []
# for a in all:
#     if a not in schools:
#         unfinished.append(a)
#
print(unfinished)
