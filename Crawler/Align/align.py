# -*- coding: utf-8 -*-
import re
import json

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

noise = [
    '学院',
    '重点',
    '实验室',
    '国家',
    '院',
    '系',
    '校区',
    '中心',
    '省',
    '市',
    '区',
    '级',
    '研究所',
    '与',
    '[\s+\.\!\/_,$%^*()+\"\']+|[+——！，。？、~@#￥%……&*（）]+'
]


def do_cal_similarity(str1, str2):
    news1 = do_remove_noise(str1)
    news2 = do_remove_noise(str2)

    len1 = len(news1)
    len2 = len(news2)

    # print(news1, news2)

    ans = [([0] * (len2 + 1)) for i in range(len1 + 1)]
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if news1[i - 1] == news2[j - 1]:
                ans[i][j] = ans[i - 1][j - 1] + 1
            else:
                ans[i][j] = max(ans[i][j - 1], ans[i - 1][j])
    lcs = ans[len1][len2]
    return lcs / min(len1, len2)


def do_remove_noise(str):
    ret = str
    for n in noise:
        ret = re.sub(n, "", ret)
    return ret

def do_ck_profile(str):
    if len(str) == 0:
        return False
    if len(str) == 4:
        if str[0] == '暂' and str[1] == '无':
            return False
        else:
            return True
    return True

teststr = u'{"a":"b", "c":"d"}'

def do_align():
    with open("new_recode.txt", 'r', encoding="utf-8") as f:
        txt = f.readlines()
        cnt = 1
        try:
            with connection.cursor() as cursor:
                for t in txt:
                    print("----------------------------")
                    print("id: "+str(cnt))
                    cnt += 1
                    tmp = t.replace('\'', '\"')
                    try:
                        dict = json.loads(tmp)
                        p = do_cal_similarity(dict['wp_college'], dict['deparment'])
                        print(p)
                        if p >= 0.5:
                            if do_ck_profile(dict['profile']):
                                sql = "UPDATE basic_info SET resume = %s WHERE id = %s"
                                cursor.execute(sql, (dict['profile'], dict['wp_id']))
                            if len(dict['image_url']) > 0:
                                sql = "UPDATE basic_info SET img_url = %s WHERE id = %s"
                                cursor.execute(sql, (dict['image_url'], dict['wp_id']))
                            sql = "UPDATE basic_info SET url2 = %s WHERE id = %s"
                            cursor.execute(sql, (dict['info_url'], dict['wp_id']))
                    except:
                        pass
            connection.commit()
        finally:
            connection.close();



            # wp_id = tmp[0].strip().split(": ")[1]
            # print(wp_id)
            #
            # wp_college = tmp[1].strip().split(': ')[1]
            # print(wp_college)
            #
            # js_department = tmp[2].strip().split(': ')[1]
            # print(js_department)
            #
            # js_profile = tmp[3].strip().split(': ')[1]
            # if do_ck_profile(js_profile):
            #     js_profile = ''
            # print(js_profile)
            #
            # tmp = tmp[4].strip().split(': ')
            # print(tmp, len(tmp))
            # js_imageurl =
            # print(js_imageurl)
            # js_infourl = tmp[5].strip().split(': ')[1].rstrip('}')
            # print(js_infourl)




if __name__ == "__main__":
    do_align()
    # try:
    #     with connection.cursor() as cursor:
    #         sql = "select resume from basic_info where id = '100000012429036'"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         print(result)
    #     connection.commit()
    # finally:
    #     connection.close();