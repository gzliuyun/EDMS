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
                    print(res)
                    cnt += 1
                    # print(cur + cnt)
                cur += p + 1
                # print(cur, p, cnt)
        connection.commit()
    finally:
        connection.close();

# 将每个专家的 小团体 存入数据库
# def insert_prs_list(id, prs_list, cursor):
#
#
#     sql = "INSERT INTO paper_relation_score VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE id = %s"
#     cursor.execute(sql, (id, str(prs_coid_list), str(prs_year_list), str(prs_score_list), id))

p = 10
st = 0
ed = 10

if __name__ == "__main__":
    sele_paper_relation(st, ed)