# -*- coding: utf-8 -*-

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

p = 1
st = 0
ed = 1


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
    print(cntid, arg)

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
        print(r1i)
    print(is_a1_coid)
    print(is_a1_cork)
    print(is_a1_date)

    ## 查找二作


def do_insert_relation(cursor):

    pass


if __name__ == "__main__":
    do_select_info()