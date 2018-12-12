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

def get_school_list():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT col FROM organization_info'
            cursor.execute(sql)
            result = cursor.fetchall()
            for res in result:
                print("\'"+res['col']+"\',")
    finally:
        connection.close();

if __name__ == "__main__":
    get_school_list()