#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 17:28
# @Author  : zyk

import requests
from pyquery import PyQuery as pq

base_url = 'http://www.irtree.com/organ/organsearch.aspx?rf=OHC%3D211工程&page='
school_names = []
school_ids = []

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
        school_names.append(school_name)
        school_ids.append(school_id)

        write_to_file(school_name,school_id)


def write_to_file(name,id):
    with open('start_urls.txt','a',encoding='utf-8') as file:
        file.write('http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id='+id)
        file.write('\n')


def main():
    for i in range(6):
        html  =  get_html(str(i+1))
        parse(html)
    print(school_names)
    print(school_ids)

if __name__ =='__main__':
    main()