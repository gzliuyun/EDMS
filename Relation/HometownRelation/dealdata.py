# -*- coding: utf-8 -*-

from ht_dict import ht_dict
from  ht_dict import  MAX_HT_NUM
from ht_list import ht_list

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

def store_ht():
    try:
        with connection.cursor() as cursor:

            for i in range(MAX_HT_NUM):
                tname = ht_list[i]
                tid = ht_dict[tname]
                tlevel = ""
                tp2id = ""
                tp1id = ""
                if (tid[2] == '0' and tid[3] == '0' and tid[4] == '0' and tid[5] == '0') :
                    tlevel = "1"
                elif (tid[4] == '0' and tid[5] == '0') :
                    tlevel = "2"
                    tp1id = tid[:2]+"0000"
                else :
                    tlevel = "3"
                    tp1id = tid[:2] + "0000"
                    tp2id = tid[:4] + "00"

                # print(tid, tname, tlevel, tp2id, tp1id)

                sql = "INSERT INTO hometown(id, name, level, p2id, p1id) VALUES(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id = %s"
                cursor.execute(sql, (tid, tname, tlevel, tp2id, tp1id, tid))
        connection.commit()
    finally:
        connection.close()

if __name__ == "__main__":

    # print(ht_list[0])
    # print(ht_dict['北京市'])

    store_ht()
