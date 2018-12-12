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

p = 1000

def restore(st, ed):
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT id, school_list FROM schoolmate_relation LIMIT %s, %s'
                cursor.execute(sql, (cur, cur+p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    if (res['school_list'] != None):
                        get_schoolmate(res['id'], res['school_list'], cursor)
                    cnt += 1
                    print("extract:",cur + cnt)
                cur += p + 1
        connection.commit()
    finally:
        connection.close()

def get_schoolmate(id, school_list, cursor):
    pass

if __name__ == "__main__":
    pass