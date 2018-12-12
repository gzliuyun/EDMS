# -*- coding: utf-8 -*-

from school_list import school_list
from school_list import MAX_NUM
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

def cluster(st, ed):
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
                        # print(res['id'])
                        extract(res['id'], res['school_list'], cursor)
                    cnt += 1
                    print("extract:",cur + cnt)
                cur += p + 1
            store(cursor)
        connection.commit()
    finally:
        connection.close();

cluster_set = [set() for i in range(MAX_NUM)]

def extract(id, school_list, cursor):
    # print(id)
    s_list = school_list.lstrip('{').rstrip('}').split(',')
    # print(s_list)
    for s in s_list:
        index = int(s)
        cluster_set[index].add(id)

def store(cursor):
    sql = "INSERT INTO cluster_by_school(id, name, list) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE id = %s"
    for i in range(MAX_NUM):
        name = school_list[i]
        smate_list = cluster_set[i]
        cursor.execute(sql, (i, name, str(smate_list), i))

if __name__ == "__main__":
    st = 0
    ed = 12326
    cluster(st, ed)

    # for i in range(MAX_NUM):
    #     print(cluster_set[i])