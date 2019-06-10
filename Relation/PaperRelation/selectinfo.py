# -*- coding: utf-8 -*-

import pymysql.cursors

import sys
sys.path.append("..")
from init import config
from init import st
from init import ed
from init import p

# config = {
#     'host': '111.205.121.93',
#     'user': 'root',
#     'password': 'root@buaa',
#     'db': 'EDMS',
#     'charset': 'utf8',
#     'cursorclass': pymysql.cursors.DictCursor,
# }

connection = pymysql.connect(**config)

def do_select_info():
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT id FROM basic_info LIMIT %s, %s'
                cursor.execute(sql, (cur, p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    do_select_paper(cur + cnt, res, cursor)
                    cnt += 1

                cur += p + 1
        connection.commit()
    finally:
        connection.close();


def do_select_paper(cntid, arg, cursor):
    print(cntid)

    ## 查找一作
    sql1 = 'SELECT date, author2, author3, author4, author5 FROM paper_info WHERE author1 = %s'
    cursor.execute(sql1, arg['id'])
    r1 = cursor.fetchall()
    is_a1_coid = []
    is_a1_cork = []
    is_a1_date = []
    for r1i in r1:
        if r1i['author2']:
            is_a1_coid.append(r1i['author2'])
            is_a1_cork.append(2)
            is_a1_date.append(r1i['date'])
        if r1i['author3']:
            is_a1_coid.append(r1i['author3'])
            is_a1_cork.append(3)
            is_a1_date.append(r1i['date'])
        if r1i['author4']:
            is_a1_coid.append(r1i['author4'])
            is_a1_cork.append(4)
            is_a1_date.append(r1i['date'])
        if r1i['author5']:
            is_a1_coid.append(r1i['author5'])
            is_a1_cork.append(5)
            is_a1_date.append(r1i['date'])
        # print(r1i)
    # print(is_a1_coid)
    # print(is_a1_cork)
    # print(is_a1_date)

    ## 查找二作
    sql2 = 'SELECT date, author1, author3, author4, author5 FROM paper_info WHERE author2 = %s'
    cursor.execute(sql2, arg['id'])
    r2 = cursor.fetchall()
    is_a2_coid = []
    is_a2_cork = []
    is_a2_date = []
    for r2i in r2:
        if r2i['author1']:
            is_a2_coid.append(r2i['author1'])
            is_a2_cork.append(1)
            is_a2_date.append(r2i['date'])
        if r2i['author3']:
            is_a2_coid.append(r2i['author3'])
            is_a2_cork.append(3)
            is_a2_date.append(r2i['date'])
        if r2i['author4']:
            is_a2_coid.append(r2i['author4'])
            is_a2_cork.append(4)
            is_a2_date.append(r2i['date'])
        if r2i['author5']:
            is_a2_coid.append(r2i['author5'])
            is_a2_cork.append(5)
            is_a2_date.append(r2i['date'])
        # print(r2i)
    # print(is_a2_coid)
    # print(is_a2_cork)
    # print(is_a2_date)

    ## 查找三作
    sql3 = 'SELECT date, author1, author2, author4, author5 FROM paper_info WHERE author3 = %s'
    cursor.execute(sql3, arg['id'])
    r3 = cursor.fetchall()
    is_a3_coid = []
    is_a3_cork = []
    is_a3_date = []
    for r3i in r3:
        if r3i['author1']:
            is_a3_coid.append(r3i['author1'])
            is_a3_cork.append(1)
            is_a3_date.append(r3i['date'])
        if r3i['author2']:
            is_a3_coid.append(r3i['author2'])
            is_a3_cork.append(2)
            is_a3_date.append(r3i['date'])
        if r3i['author4']:
            is_a3_coid.append(r3i['author4'])
            is_a3_cork.append(4)
            is_a3_date.append(r3i['date'])
        if r3i['author5']:
            is_a3_coid.append(r3i['author5'])
            is_a3_cork.append(5)
            is_a3_date.append(r3i['date'])
        # print(r3i)
    # print(is_a3_coid)
    # print(is_a3_cork)
    # print(is_a3_date)

    ## 查找四作
    sql4 = 'SELECT date, author1, author2, author3, author5 FROM paper_info WHERE author4 = %s'
    cursor.execute(sql4, arg['id'])
    r4 = cursor.fetchall()
    is_a4_coid = []
    is_a4_cork = []
    is_a4_date = []
    for r4i in r4:
        if r4i['author1']:
            is_a4_coid.append(r4i['author1'])
            is_a4_cork.append(1)
            is_a4_date.append(r4i['date'])
        if r4i['author2']:
            is_a4_coid.append(r4i['author2'])
            is_a4_cork.append(2)
            is_a4_date.append(r4i['date'])
        if r4i['author3']:
            is_a4_coid.append(r4i['author3'])
            is_a4_cork.append(3)
            is_a4_date.append(r4i['date'])
        if r4i['author5']:
            is_a4_coid.append(r4i['author5'])
            is_a4_cork.append(5)
            is_a4_date.append(r4i['date'])
        # print(r4i)
    # print(is_a4_coid)
    # print(is_a4_cork)
    # print(is_a4_date)

    ## 查找五作
    sql5 = 'SELECT date, author1, author2, author3, author4 FROM paper_info WHERE author5 = %s'
    cursor.execute(sql5, arg['id'])
    r5 = cursor.fetchall()
    is_a5_coid = []
    is_a5_cork = []
    is_a5_date = []
    for r5i in r5:
        if r5i['author1']:
            is_a5_coid.append(r5i['author1'])
            is_a5_cork.append(1)
            is_a5_date.append(r5i['date'])
        if r5i['author2']:
            is_a5_coid.append(r5i['author2'])
            is_a5_cork.append(2)
            is_a5_date.append(r5i['date'])
        if r5i['author3']:
            is_a5_coid.append(r5i['author3'])
            is_a5_cork.append(3)
            is_a5_date.append(r5i['date'])
        if r5i['author4']:
            is_a5_coid.append(r5i['author4'])
            is_a5_cork.append(4)
            is_a5_date.append(r5i['date'])
        # print(r5i)
    # print(is_a5_coid)
    # print(is_a5_cork)
    # print(is_a5_date)

    sql = "INSERT INTO paper_relation VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
        ON DUPLICATE KEY UPDATE id = %s"
    cursor.execute(sql, (arg['id'],
                         str(is_a1_coid), str(is_a1_cork), str(is_a1_date),
                         str(is_a2_coid), str(is_a2_cork), str(is_a2_date),
                         str(is_a3_coid), str(is_a3_cork), str(is_a3_date),
                         str(is_a4_coid), str(is_a4_cork), str(is_a4_date),
                         str(is_a5_coid), str(is_a5_cork), str(is_a5_date),
                         arg['id']
                         ))


if __name__ == "__main__":
    do_select_info()