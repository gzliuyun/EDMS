# -*- coding: utf-8 -*-

import pymysql.cursors
from calc_paper_score import calc_paper_score

config = {
    'host': '111.205.121.93',
    'user': 'root',
    'password': 'root@buaa',
    'db': 'EDMS',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)

def sele_paper_relation(st, ed):
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT * FROM paper_relation LIMIT %s, %s'
                cursor.execute(sql, (cur, p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    calc_paper_score(res)
                    cnt += 1
                print("#############################")
                cur += p + 1
        connection.commit()
    finally:
        connection.close();



p = 10
st = 0
ed = 100

if __name__ == "__main__":
    sele_paper_relation(st, ed)