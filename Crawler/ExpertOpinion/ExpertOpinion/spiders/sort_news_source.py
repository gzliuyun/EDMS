# -*- encoding: utf-8 -*-

import scrapy
import MySQLdb
import pandas as pd
from pandas import DataFrame
from urllib.parse import unquote
from datetime import datetime

# 数据库连接
conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
cur = conn.cursor()

# 获取opinion_raw表里的专家id数据，为了不爬取已存在的数据
sql = cur.execute('select `expert_id`, `expert_name`, `article_source` from edms.opinion_raw where `article_url` is not null')
conn.commit()

# 将查询结果存储于data变量中
db_data_opinion_raw = cur.fetchall()
data_opinion_raw = list(db_data_opinion_raw)
data_opinion_raw = [list(i) for i in data_opinion_raw]
df_opinion_raw = DataFrame(data_opinion_raw, columns=["expert_id", "expert_name", "article_source"])

expert_id_list = df_opinion_raw['expert_id'].tolist()
expert_name_list = df_opinion_raw['expert_name'].tolist()
article_source_list = df_opinion_raw['article_source'].tolist()

# 数据库断开连接
cur.close()
conn.close()

source_count = {}
for article_source in article_source_list:
	article_source_item_list = article_source.split('<edms/>')
	for article_source_item in article_source_item_list:
		# print(article_source_item)
		if(article_source_item in source_count.keys()):
			source_count[article_source_item] += 1
			# print(source_count[article_source_item])
		else:
			source_count[article_source_item] = 1
			# print(source_count[article_source_item])

source_count_sort = sorted(source_count.items(),key = lambda x:x[1],reverse = True)
print(len(source_count_sort))
for source_count_sort_item in source_count_sort[:50]:
	print(source_count_sort_item)
