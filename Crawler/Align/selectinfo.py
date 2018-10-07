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
st = 482105
ed = 907916
cur = st

# ed_id = 2533689

def do_align():
    try:
        with connection.cursor() as cursor:

            cur = st
            while cur < ed:
                sql = 'SELECT id, name, university, department, profile, image_url, info_url FROM expert_intro LIMIT %s, %s'
                cursor.execute(sql, (cur, p))
                result = cursor.fetchall()
                do_add_weipu(result, cur)
                cur += p + 1
        connection.commit()
    finally:
        connection.close();


dict = {
    'wp_id': '',
    'wp_college': '',
    'deparment': '',
    'profile': '',
    'image_url': '',
    'info_url': '',
}


def do_add_weipu(result, cur):
    with connection.cursor() as cursor:
        cnt = 0
        for ret in result:
            cnt += 1
            if ret['profile'] == '暂无简介' and ret['image_url'] == '':
                continue
            wp_name = ret['name']
            wp_university = ret['university']
            wp_department = ret['department']
            sql = 'SELECT id, college FROM basic_info WHERE name = %s AND university = %s'
            cursor.execute(sql, (wp_name, wp_university))
            wp_ret = cursor.fetchall()
            print(wp_ret)
            if len(wp_ret) > 0:
                with open("align_recorde.txt", 'a', encoding="utf-8") as f:
                    for tmp in wp_ret:
                        print(tmp, ret['profile'], ret['image_url'], ret['department'])
                        normal_dict()
                        fill_dict(tmp['id'], tmp['college'], ret['department'], ret['profile'], ret['image_url'], ret['info_url'])
                        f.write(str(dict))
                        f.write(' ')
                        f.write(str(cur+cnt))
                        f.write('\n')
                f.close()



def normal_dict():
    dict['wp_id'] = ''
    dict['wp_college'] = ''
    dict['deparment'] = ''
    dict['profile'] = ''
    dict['image_url'] = ''
    dict['info_url'] = ''


def fill_dict(wp_id, wp_college, department, profile, image_url, info_url):
    dict['wp_id'] = wp_id
    dict['wp_college'] = wp_college
    dict['deparment'] = department
    dict['profile'] = profile
    dict['image_url'] = image_url
    dict['info_url'] = info_url


if __name__ == "__main__":
    do_align()