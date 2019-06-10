# -*- coding: utf-8 -*-

import pymysql.cursors
from calc_paper_score import calc_paper_score

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

def sele_paper_relation(st, ed):
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT * FROM paper_relation LIMIT %s, %s'
                cursor.execute(sql, (cur, p))
                result = cursor.fetchall()
                cnt = 1
                for res in result:
                    prs_list = calc_paper_score(res)
                    insert_prs_list(res['id'], prs_list, cursor)
                    cnt += 1
                    print(cur + cnt)
                cur += p + 1
                print(cur, p, cnt)
        connection.commit()
    finally:
        connection.close();

# 将每个专家的prsl_list存入数据库
def insert_prs_list(id, prs_list, cursor):
    # print(id)
    prs_coid_list = []
    prs_year_list = []
    prs_score_list = []

    if prs_list != None:
        for prs in prs_list:
            # print(prs.coid, prs.year, prs.score)
            prs_coid_list.append(prs.coid)
            prs_year_list.append(prs.year)
            prs_score_list.append(prs.score)

    sql = "INSERT INTO paper_relation_score VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE id = %s"
    cursor.execute(sql, (id, str(prs_coid_list), str(prs_year_list), str(prs_score_list), id))

if __name__ == "__main__":
    sele_paper_relation(st, ed)