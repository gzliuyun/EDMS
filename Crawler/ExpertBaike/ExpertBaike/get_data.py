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

def get_school_name_id_college(st, p):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT university, name, id FROM basic_info LIMIT %s, %s'
            cursor.execute(sql, (st, p))
            result = cursor.fetchall()
            write_data(result)
            print(st+p)
        connection.commit()
    finally:
        connection.close()

def write_data(res):
    with open("data1.txt", "w+", encoding='utf-8') as f:
        for ri in res:
            str = ri['university'] + " " + \
                  ri['name'] + " " + \
                  ri['id'] + "\n"
            # print(str)
            f.write(str)
    f.close()

st = 0       # 起始位置
p = 10000    # 偏移量

if __name__ == "__main__":
    get_school_name_id_college(st, p)