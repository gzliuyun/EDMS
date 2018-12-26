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

def sele_theme_relation(st, ed):
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT id, theme_list FROM basic_info LIMIT %s, %s'
                cursor.execute(sql, (cur, cur+p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    insert_theme_relation(res['id'],res['theme_list'], cursor)
                    cnt += 1
                    print(cur + cnt)
                cur += p + 1
                # print(cur, p, cnt)
        connection.commit()
    finally:
        connection.close();

# 存入数据库
def insert_theme_relation(expert_id, theme_list, cursor):

    if theme_list == None:
        return

    t_list = theme_list.split('、')
    # print(t_list)
    sql = "INSERT INTO theme_relation(theme, expert_id) VALUES (%s, %s)"

    for theme in t_list:
        cursor.execute(sql, (theme, expert_id))

p = 1000
st = 0
ed = 108257

if __name__ == "__main__":
    sele_theme_relation(st, ed)