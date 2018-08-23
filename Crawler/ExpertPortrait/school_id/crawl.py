#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 17:28
# @Author  : zyk

import requests
from pyquery import PyQuery as pq

base_url = 'http://www.irtree.com/organ/organsearch.aspx?rf=OHC%3D普通本科&page='
school_names = []
school_ids = []
school_211 = ['清华大学', '浙江大学', '北京大学', '吉林大学', '上海交通大学', '华中科技大学', '武汉大学', '四川大学',
                '南京大学', '山东大学', '华南理工大学', '复旦大学', '同济大学', '哈尔滨工业大学', '中山大学', '天津大学',
                '东南大学', '中南大学', '北京师范大学', '大连理工大学', '郑州大学', '中国人民大学', '西安交通大学', '南开大学',
                '华东师范大学', '苏州大学', '厦门大学', '重庆大学', '南京师范大学', '湖南大学', '武汉理工大学',
                '中国科学技术大学', '东北大学', '北京航空航天大学', '电子科技大学', '华中师范大学', '西南交通大学',
                '西北工业大学', '暨南大学', '上海大学', '西南大学', '兰州大学', '广西大学', '北京理工大学', '北京交通大学',
                '合肥工业大学', '中国农业大学', '中国矿业大学', '南昌大学', '华北电力大学', '华南师范大学', '北京科技大学',
                '南京理工大学', '太原理工大学', '河海大学', '湖南师范大学', '西安电子科技大学', '西北农林科技大学',
                '北京工业大学', '陕西师范大学', '北京邮电大学', '南京农业大学', '南京航空航天大学', '华东理工大学',
                '哈尔滨工程大学', '东北师范大学', '中国海洋大学', '安徽大学', '中国地质大学', '江南大学', '贵州大学',
                '云南大学', '西北大学', '福州大学', '华中农业大学', '东华大学', '长安大学', '北京林业大学', '东北林业大学',
                '西南财经大学', '辽宁大学', '北京化工大学', '中南财经政法大学', '上海财经大学', '东北农业大学',
                '河北工业大学', '内蒙古大学', '新疆大学', '石河子大学', '大连海事大学', '对外经济贸易大学', '北京中医药大学',
                '四川农业大学', '中国政法大学', '宁夏大学', '中央民族大学', '中央财经大学', '延边大学', '中国石油大学（北京）',
                '天津医科大学', '中国传媒大学', '中国药科大学', '中国矿业大学（北京）', '海南大学', '中国石油大学',
                '北京体育大学', '上海外国语大学', '青海大学', '西藏大学', '北京外国语大学', '中央音乐学院', '哈尔滨工业大学(威海)']

def get_html(page):
    url = base_url +page
    try:
        response = requests.get(url)
        if response.status_code == 200 :
            return response.text
        return None
    except requests.ConnectionError:
        return None

def parse(html):
    doc = pq(html)
    items = doc('.cp-add').items()
    global school_names
    global school_ids
    for item in items:
        school_name = item.attr('objname')
        school_id = item.attr('objid')
        if school_name not in school_211:
            school_names.append(school_name)
            school_ids.append(school_id)
            check_url = 'http://www.irtree.cn/'+school_id+'/default.aspx'
            response = requests.get(check_url)
            if response.url == check_url:
                write_to_file(school_name,school_id)


def write_to_file(name,id):
    with open('start_urls.txt','a',encoding='utf-8') as file:
        file.write('http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id='+id+' '+name)
        file.write('\n')


def main():
    for i in range(23):
        html  =  get_html(str(i+1))
        parse(html)
    print(school_names)
    print(school_ids)

if __name__ =='__main__':
    main()