# -*- coding: utf-8 -*-
import pymysql.cursors
from findGroupAndCore import getCore

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
                sql = 'SELECT * FROM paper_relation_score LIMIT %s, %s'
                cursor.execute(sql, (cur, p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    core_ex_id = getCore(res, cursor)
                    print(core_ex_id)
                    cnt += 1
                    # print(cur + cnt)
                cur += p + 1
                # print(cur, p, cnt)
        connection.commit()
    finally:
        connection.close();

# 将每个专家的 小团体 存入数据库

p = 1
st = 0
ed = 1

if __name__ == "__main__":
    sele_paper_relation(st, ed)