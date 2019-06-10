# -*- coding: utf-8 -*-

from ht_dict import ht_dict
from  ht_dict import  MAX_HT_NUM
from ht_list import ht_list
from ht_id_dict import get_index
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

def cluster(st, ed):
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT id, hometown_id FROM hometown_relation LIMIT %s, %s'
                cursor.execute(sql, (cur, cur+p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    if (res['hometown_id'] != None):
                        # print(res['id'])
                        extract(res['id'], res['hometown_id'], cursor)
                    cnt += 1
                    # print("extract:",cur + cnt)
                cur += p + 1
            store(cursor)
        connection.commit()
    finally:
        connection.close();

cluster_set = [set() for i in range(MAX_HT_NUM)]

def extract(id, hometown_id, cursor):
    # print(id)
    ht_id_list = set()
    ht_id_list.add(hometown_id)
    ht_id_list.add(hometown_id[:2]+"0000")
    ht_id_list.add(hometown_id[:4]+"00")

    for ht_id in ht_id_list:
        tmpid = get_index(ht_id)
        if tmpid != None:
            index = int(tmpid)
            # print(id, ht_id, index)
            cluster_set[index].add(id)

def store(cursor):
    sql = "UPDATE hometown SET list = %s WHERE id = %s"
    for i in range(MAX_HT_NUM):
        htmate_list = cluster_set[i]
        id = ht_dict[ht_list[i]]
        print("---"*20)
        print(id)
        print(htmate_list)
        cursor.execute(sql, (str(htmate_list), id))

if __name__ == "__main__":

    cluster(st, ed)

    # for i in range(MAX_NUM):
    #     print(cluster_set[i])