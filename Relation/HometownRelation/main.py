# -*- coding: utf-8 -*-

import pymysql.cursors
from ht_seive import ht_seive


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

def sele_resume(st, ed):
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT id, resume FROM basic_info LIMIT %s, %s'
                cursor.execute(sql, (cur, p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    if (res['resume'] != None and len(res['resume']) > 3):
                        abstract_hometown(res['id'], res['resume'], cursor)
                    cnt += 1
                    print(cur + cnt)
                cur += p + 1
        connection.commit()
    finally:
        connection.close();


def abstract_hometown(id, resume, cursor):
    ht_id = ht_seive(resume)
    sql = "INSERT INTO hometown_relation(id, hometown_id) VALUES(%s, %s) ON DUPLICATE KEY UPDATE id = %s"
    if (len(ht_id) > 0):
        cursor.execute(sql, (id, ht_id, id))
        # print("---" * 20)
        # print(ht_id)

if __name__ == "__main__":
    st = 0
    ed = 1093249
    sele_resume(st, ed)