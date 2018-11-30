# -*- encoding: utf-8 -*-

import scrapy
import MySQLdb
# import pandas as pd
from pandas import DataFrame
from urllib.parse import unquote
from datetime import datetime
import re


# 爬取每个学者在百度咨询页查询结果第一页中的所有百度快照链接，存储于数据库
# 用百度资讯查basic_info表中的专家，并把结果写到opinion_raw表中.
class BaiduNewsSpider(scrapy.Spider):
    # 继承scrapy.Spider类
    """
    scrapy运行的流程：
    1.定义链接；
    2.start_requests方法:通过链接爬取(下载)页面，简单地把页面做了一个保存；
    3.parse方法:定义规则，然后用xpath、正则或是css选择器提取数据。
    """

    # init
    def __init__(self):
        super().__init__()
        # 定义爬虫名,在命令行通过"scrapy crawl 爬虫名"来运行爬虫
        self.name = 'baidu_news_spider'
        self.data = []
        self.df = DataFrame(data=self.data)
        self.current_expert_id = 0
    
    # 初始化,接收命令行参数"scrapy crawl 爬虫名 -a 参数名=参数值"
    def start_requests(self):
        print("\n### Method ### Enter Method: start_requests\n")
        # 计时
        start_time = datetime.now()

        # 数据库连接
        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
        cur = conn.cursor()

        # 爬虫入口URL
        # https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&tn=news&word=学者名+学校名+学院名（或者是学者名+机构名）
        source_url = 'https://www.baidu.com/s?ie=utf-8&rtt=1&bsst=1&tn=news&pn=0&word='

        # 获取opinion_raw表里的专家id数据，为了不爬取已存在的数据
        sql = cur.execute('select `expert_id` from edms.opinion_raw')
        conn.commit()

        # 将查询结果存储于data变量中
        db_data_opinion = cur.fetchall()
        data_opinion = list(db_data_opinion)
        data_opinion = [list(i) for i in data_opinion]
        df_opinion = DataFrame(data_opinion, columns=["expert_id"])

        # 获得已存在的专家的list
        exist_expert_list = df_opinion['expert_id'].tolist()
        
        # 获取数据库edms.basic_info中所有的学者名、学校名、学院名
        sql = cur.execute('select  `id`, `name`, `university`, `college` from edms.basic_info')
        conn.commit()
        db_data_all_expert = cur.fetchall()
        all_expert_list = list(db_data_all_expert)
        all_expert_list = [list(i) for i in all_expert_list]

        # 数据库断开连接
        cur.close()
        conn.close()

        # 构造未爬取学者集的数据框
        print('### Loop Start ### 开始构造not_exist_expert_list')
        not_exist_expert_list = []
        loop_count = 0
        for expert in all_expert_list:
            print(loop_count)
            loop_count += 1
            if expert[0] not in exist_expert_list:
                # 若不存在，则添加到not_exist_expert_list
                print('添加未爬取专家: ' + expert[0] + ' ' + expert[1] + ' ' + expert[2] + ' ' + expert[3])
                not_exist_expert_list.append(expert)
            else:
                pass

        print('### Loop End ### 构造not_exist_expert_list完毕')
        print(len(not_exist_expert_list))
        end_time1 = datetime.now()
        """
            后面为了对数据进行处理，把数据存在DataFrame中，
            但是如果直接把data放入DataFrame的初始化，会提示初始化失败。
            需要将data的每一维都转换为list类型才能成功。
        """
        self.data = not_exist_expert_list
        self.df = DataFrame(self.data, columns=["expert_id", "expert_name", "expert_university", "expert_college"])
        print(len(self.df))

        # 拼接URL，给数据框增添source_url列
        print('### Loop Start ### 开始构造source_url列')
        self.df['source_url'] = self.df.apply(lambda r: (source_url + r['expert_name'] + "+" + r['expert_university'] +
                                                         "+" + r['expert_college']), axis=1)
        print('### Loop End ### 构造source_url列完毕')
        end_time2 = datetime.now()

        # 对每个url进行爬取，并将爬取到的页面交由self.parse方法处理
        for url in self.df['source_url']:
            self.current_expert_id = self.df['expert_id']
            yield scrapy.Request(url=url, callback=self.parse)

        # HINT
        end_time3 = datetime.now()
        print('\n构造not_exist_expert_list耗时:')
        print(end_time1 - start_time)
        
        print('\n构造source_url耗时:')
        print(end_time2 - start_time)

        print('\n爬虫程序总耗时:')
        print(end_time3 - start_time)

    # 处理页面的parse方法
    def parse(self, response):
        print("\n### Method ### Enter Method: parse")

        # 数据库连接
        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
        cur = conn.cursor()

        r = response
        # 解URL编码
        url_utf8 = unquote(r.url, 'utf-8')
        # print("\n source_url")
        # print(r.url)
        # print(url_utf8)

        this_expert = self.df[self.df['source_url'] == url_utf8]
        # print(len(this_expert))
        expert_id = list(this_expert['expert_id'])[0]
        expert_name = list(this_expert['expert_name'])[0]
        expert_university = list(this_expert['expert_university'])[0]
        expert_college = list(this_expert['expert_college'])[0]
        source_url = list(this_expert['source_url'])[0]

        # print(expert_id)
        # print(expert_name)
        # print(expert_university)
        # print(expert_college)
        # print(source_url)

        # 确保不爬取已存在的数据：判断该学者是否已经存在，若存在则不爬取
        print('### Database ### ready to pull data from Database')
        sql = cur.execute('select `expert_id` from edms.opinion_raw where expert_id="' + expert_id + '"')
        conn.commit()
        db_data = cur.fetchall()

        if len(db_data) > 0:
            print("*** 数据已存在 ***")
        else:
            # 从搜索结果的第一页取得该页数据
            # 文章源网页URL列表
            article_url_list = r.css('div.result > h3.c-title > a::attr(href)').extract()
            # 文章标题列表
            article_title_list = []
            article_title_a_list = r.css('div.result > h3.c-title > a').extract()
            for article in article_title_a_list:
                article_title_list.append(article.split('"_blank">')[len(article.split('"_blank">'))-1].
                                          replace('\t', '').replace('\n', '').replace(' ', '').replace('<em>', '').
                                          replace('</em>', '').replace('</a>', ''))
            # 文章来源机构列表
            source_list = r.css('div.result > div.c-summary > p.c-author::text').extract()
            article_source_list = []
            for source in source_list:
                article_source_list.append(source.split('\xa0')[0].replace('\t', '').replace('\n', '').replace(' ', ''))
            # 文章发表时间列表
            article_time_list = []
            for source in source_list:
                if len(source.split('\xa0')) >= 3:
                    article_time_list.append(source.split('\xa0')[2].replace('\t', '').replace('\n', '')
                                             .replace(' ', ''))
                else:
                    article_time_list.append(source.replace('\xa0', '').replace('\t', '').replace('\n', '')
                                             .replace(' ', ''))
            # 文章概要列表
            brief_list = r.css('div.c-summary').extract()
            article_brief_list = []
            for brief in brief_list:
                if len(brief.split('</p>')) >= 2:
                    article_brief_list.append(brief.split('</p>')[1].split('<span class')[0].replace('\t', '')
                                              .replace('\n', '').replace(' ', '').replace('<em>', '')
                                              .replace('</em>', '').replace('</a>', ''))
                else:
                    article_brief_list.append(brief.split('<span class')[0].replace('\t', '')
                                              .replace('\n', '').replace(' ', '').replace('<em>', '')
                                              .replace('</em>', '').replace('</a>', ''))
            # 百度快照URL列表
            snapshot_url_list = r.css('div.result > div.c-summary > span.c-info a.c-cache::attr(href)').extract()

            # 取各个list的最短和最长长度
            min_list_len = min(len(article_url_list), len(article_title_list), len(article_source_list),
                               len(article_time_list), len(article_brief_list), len(snapshot_url_list))
            max_list_len = max(len(article_url_list), len(article_title_list), len(article_source_list),
                               len(article_time_list), len(article_brief_list), len(snapshot_url_list))

            # 存储该行入数据库
            if (min_list_len > 0) & (min_list_len == max_list_len):
                # 保证摘取的list长度一致
                article_url_str = ','.join(article_url_list)
                article_title_str = '<edms/>'.join(article_title_list)
                article_source_str = '<edms/>'.join(article_source_list)
                article_time_str = '<edms/>'.join(article_time_list)
                article_brief_str = '<edms/>'.join(article_brief_list)
                snapshot_url_str = ','.join(snapshot_url_list)

                # 去除brief里的单引号、双引号、转义符号、换行符、制表符
                article_title_str = article_title_str.replace('\\', '').replace('\'', '').replace('\"', '').\
                    replace('\n', '').replace('\t', '')
                article_brief_str = article_brief_str.replace('\\', '').replace('\'', '').replace('\"', '').\
                    replace('\n', '').replace('\t', '')
                
                print('### Database ### ready to store into Database: ' + expert_id + " - " + expert_name)
                sql = cur.execute('insert into edms.opinion_raw(`expert_id`, `expert_name`, `expert_university`, ' +
                                  '`expert_college`, `source_url`, `article_url`, `article_title`, `article_source`, ' +
                                  '`article_time`, `article_brief`, `snapshot_url`, `analysis_tag`) values("' +
                                  expert_id + '", "' + expert_name + '", "' + expert_university + '", "' +
                                  expert_college + '", "' + source_url + '", "' + article_url_str + '", "' +
                                  article_title_str + '", "' + article_source_str + '", "' + article_time_str +
                                  '", "' + article_brief_str + '", "' +  snapshot_url_str + '", "False")')
                conn.commit()
            else:
                # 若无搜索结果，则暂定该专家无观点
                print("no snapshot_url_list")
                print('### Database ### ready to store into Database: ' + expert_id + " - " + expert_name)
                sql = cur.execute('insert into edms.opinion_raw(`expert_id`, `expert_name`, `expert_university`, ' +
                                  '`expert_college`, `source_url`, `analysis_tag`) values("' +
                                  expert_id + '", "' + expert_name + '", "' + expert_university + '", "' +
                                  expert_college + '", "' + source_url + '", "No")')
                conn.commit()

        # 数据库断开连接
        cur.close()
        conn.close()
        
        # 处理下一页:1.获取找到下一页链接URL;2.判断如果下一页非空,则爬取之.
        # next_page = response.css('li.next a::attr(href)')[0].extract()
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


# 爬取每个学者在百度咨询页查询结果第一页中的所有百度快照链接，存储于数据库
# 用百度资讯查opinion_raw表中没有获得资讯的专家，并把结果更新到opinion_raw表中.
class BaiduNewsSupplementSpider(scrapy.Spider):
    # 继承scrapy.Spider类
    """
    scrapy运行的流程：
    1.定义链接；
    2.start_requests方法:通过链接爬取(下载)页面，简单地把页面做了一个保存；
    3.parse方法:定义规则，然后用xpath、正则或是css选择器提取数据。
    """

    # init
    def __init__(self):
        super().__init__()
        # 定义爬虫名,在命令行通过"scrapy crawl 爬虫名"来运行爬虫
        self.name = 'baidu_news_supplement_spider'
        self.data = []
        self.df = DataFrame(data=self.data)
        self.current_expert_id = 0
    
    # 初始化,接收命令行参数"scrapy crawl 爬虫名 -a 参数名=参数值"
    def start_requests(self):
        print("\n### Method ### Enter Method: start_requests\n")

        # 数据库连接
        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
        cur = conn.cursor()

        # 爬虫入口URL
        # https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&tn=news&word=学者名+学校名+学院名（或者是学者名+机构名）
        # source_url = 'https://www.baidu.com/s?ie=utf-8&rtt=1&bsst=1&tn=news&pn=0&word='

        # 获取opinion_raw表里的专家id数据，为了不爬取已存在的数据
        sql = cur.execute('select `expert_id`, `source_url` from edms.opinion_raw ' +
                          'where `article_url` is null and `analysis_tag`!="No"')
        conn.commit()

        # 将查询结果存储于data变量中
        db_data_opinion = cur.fetchall()
        data_opinion = list(db_data_opinion)
        data_opinion = [list(i) for i in data_opinion]
        df_opinion = DataFrame(data_opinion, columns=["expert_id", "source_url"])
        self.df = df_opinion
        print('循环总次数:')
        loop_count_desc = len(self.df)
        print(loop_count_desc)

        # 获得专家的list
        expert_list = df_opinion['expert_id'].tolist()
        self.data = expert_list

        # 数据库断开连接
        cur.close()
        conn.close()

        # 对每个url进行爬取，并将爬取到的页面交由self.parse方法处理
        for url in self.df['source_url']:
            print('还剩 ' + str(loop_count_desc) + ' 次循环')
            loop_count_desc -= 1
            self.current_expert_id = self.df['expert_id']
            yield scrapy.Request(url=url, callback=self.parse)

    # 处理页面的parse方法
    def parse(self, response):
        print("\n### Method ### Enter Method: parse")

        # 数据库连接
        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
        cur = conn.cursor()

        r = response
        # 解URL编码
        url_utf8 = unquote(r.url, 'utf-8')
        # print("\n source_url")
        # print(r.url)
        # print(url_utf8)

        this_expert = self.df[self.df['source_url'] == url_utf8]
        if this_expert is None:
            cur.close()
            conn.close()
            return

        # print(len(this_expert))
        expert_id = list(this_expert['expert_id'])[0]
        source_url = list(this_expert['source_url'])[0]

        print(expert_id)
        # print(expert_name)
        # print(expert_university)
        # print(expert_college)
        print(source_url)

        # 确保不爬取已存在的数据：判断该学者的资讯是否已经存在，若存在则不爬取
        print('### Database ### ready to pull data from Database')
        sql = cur.execute('select content from edms.opinion_raw where `expert_id`="' + expert_id +
                          '" and `article_url` is not null')
        conn.commit()
        db_data = cur.fetchall()

        if len(db_data) > 0:
            print("*** 数据已存在 *** expert_id = " + expert_id)
        else:
            # 从搜索结果的第一页取得该页数据
            # 文章源网页URL列表
            article_url_list = r.css('div.result > h3.c-title > a::attr(href)').extract()
            # 文章标题列表
            article_title_list = []
            article_title_a_list = r.css('div.result > h3.c-title > a').extract()
            for article in article_title_a_list:
                article_title_list.append(article.split('"_blank">')[len(article.split('"_blank">'))-1]
                                          .replace('\t', '').replace('\n', '').replace(' ', '').replace('<em>', '')
                                          .replace('</em>', '').replace('</a>', ''))
            # 文章来源机构列表
            source_list = r.css('div.result > div.c-summary > p.c-author::text').extract()
            article_source_list = []
            for source in source_list:
                article_source_list.append(source.split('\xa0')[0].replace('\t', '').replace('\n', '').replace(' ', ''))
            # 文章发表时间列表
            article_time_list = []
            for source in source_list:
                if len(source.split('\xa0')) >= 3:
                    article_time_list.append(source.split('\xa0')[2].replace('\t', '').replace('\n', '')
                                             .replace(' ', ''))
                else:
                    article_time_list.append(source.replace('\xa0', '').replace('\t', '').replace('\n', '')
                                             .replace(' ', ''))
            # 文章概要列表
            brief_list = r.css('div.c-summary').extract()
            article_brief_list = []
            for brief in brief_list:
                if len(brief.split('</p>')) >= 2:
                    article_brief_list.append(brief.split('</p>')[1].split('<span class')[0].replace('\t', '')
                                              .replace('\n', '').replace(' ', '').replace('<em>', '')
                                              .replace('</em>', '').replace('</a>', ''))
                else:
                    article_brief_list.append(brief.split('<span class')[0].replace('\t', '').replace('\n', '')
                                              .replace(' ', '').replace('<em>', '').replace('</em>', '')
                                              .replace('</a>', ''))
            # 百度快照URL列表
            snapshot_url_list = r.css('div.result > div.c-summary > span.c-info a.c-cache::attr(href)').extract()

            # 取各个list的最短和最长长度
            min_list_len = min(len(article_url_list), len(article_title_list), len(article_source_list),
                               len(article_time_list), len(article_brief_list), len(snapshot_url_list))
            max_list_len = max(len(article_url_list), len(article_title_list), len(article_source_list),
                               len(article_time_list), len(article_brief_list), len(snapshot_url_list))

            # 存储该行入数据库
            if (min_list_len > 0) & (min_list_len == max_list_len):
                # 保证摘取的list长度一致
                article_url_str = ','.join(article_url_list)
                article_title_str = '<edms/>'.join(article_title_list)
                article_source_str = '<edms/>'.join(article_source_list)
                article_time_str = '<edms/>'.join(article_time_list)
                article_brief_str = '<edms/>'.join(article_brief_list)
                snapshot_url_str = ','.join(snapshot_url_list)
                
                # 去除单引号、双引号、转义符号、换行符、制表符
                article_title_str = article_title_str.replace('\\', '').replace('\'', '').replace('\"', '')\
                    .replace('\n', '').replace('\t', '')
                article_brief_str = article_brief_str.replace('\\', '').replace('\'', '').replace('\"', '')\
                    .replace('\n', '').replace('\t', '')

                try:
                    print('### Database ### ready to update Database: ' + expert_id)
                    sql_sentence = 'update edms.opinion_raw set `article_url`="' + article_url_str + \
                                   '", `article_title`="' + article_title_str + '", `article_source`="' + \
                                   article_source_str + '", `article_time`="' + article_time_str + \
                                   '", `article_brief`="' + article_brief_str + '", `snapshot_url`="' + \
                                   snapshot_url_str + '" where `expert_id`="' + expert_id + '" limit 1'
                    # print(sql_sentence)
                    sql = cur.execute(sql_sentence)
                    # print(sql)
                    if sql == 1:
                        print("~~~~~ Update Success ~~~~~")
                        cur.close()
                        conn.commit()
                    else:
                        print("!!!!!!!!!!!!!!! Error  rollback !!!!!!!!!!!!!!!")
                        cur.close()
                        conn.rollback()
                except Exception as e:
                    print("!!!!!!!!!!!!!!! Exception  rollback !!!!!!!!!!!!!!!")
                    print(e.message)
                    cur.close()
                    conn.rollback()
                
            else:
                # 若无搜索结果，则暂定该专家无观点
                print("***** no snapshot_url_list *****")
                try:
                    print('### Database ### ready to update Database: ' + expert_id)
                    sql_sentence = 'update edms.opinion_raw set `analysis_tag`="No" where `expert_id`="' + \
                                   expert_id + '" limit 1'
                    # print(sql_sentence)
                    sql = cur.execute(sql_sentence)
                    # print(sql)
                    if sql == 1:
                        print("~~~~~ Update Success ~~~~~")
                        cur.close()
                        conn.commit()
                    else:
                        print("!!!!!!!!!!!!!!! Error  rollback !!!!!!!!!!!!!!!")
                        cur.close()
                        conn.rollback()
                except Exception as e:
                    print("!!!!!!!!!!!!!!! Exception  rollback !!!!!!!!!!!!!!!")
                    print(e.message)
                    cur.close()
                    conn.rollback()
            
        # 数据库断开连接
        conn.close()


# 爬取每个学者在百度咨询页查询结果第一页中的所有百度快照链接，存储于数据库
class BaiduContentSpider(scrapy.Spider):
    # 继承scrapy.Spider类
    """
    scrapy运行的流程：
    1.定义链接；
    2.start_requests方法:通过链接爬取(下载)页面，简单地把页面做了一个保存；
    3.parse方法:定义规则，然后用xpath、正则或是css选择器提取数据。
    """
    # 定义爬虫名,在命令行通过"scrapy crawl 爬虫名"来运行爬虫
    name = 'baidu_content_spider'
    data = []
    df = DataFrame(data=data)

    # 初始化,接收命令行参数"scrapy crawl 爬虫名 -a 参数名=参数值"
    def start_requests(self):
        print("\n### Method ### Enter Method: start_requests\n")

        # 数据库连接
        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
        cur = conn.cursor()

        # 获取opinion_raw表里的专家id数据，为了不爬取已存在的数据（爬过一次的暂时不重新爬取）
        sql = cur.execute('select `expert_id`, `article_source`, `article_url` from edms.opinion_raw ' +
                          'where `article_url` is not null and `analysis_tag`!="ing"')
        conn.commit()

        # 将查询结果存储于data变量中
        db_data_opinion_raw = cur.fetchall()
        data_opinion_raw = list(db_data_opinion_raw)
        data_opinion_raw = [list(i) for i in data_opinion_raw]
        df_opinion_raw = DataFrame(data_opinion_raw, columns=["expert_id", "article_source", "article_url"])
        self.df = df_opinion_raw

        expert_id_list = df_opinion_raw['expert_id'].tolist()
        article_source_list = df_opinion_raw['article_source'].tolist()
        article_url_list = df_opinion_raw['article_url'].tolist()
        
        # 数据库断开连接
        cur.close()
        conn.close()

        # 对每个url进行爬取，并将爬取到的页面交由self.parse方法处理
        # 对于整个url列表
        # for index in range(0,3):
        for index in range(0, len(expert_id_list)):
            print('\nindex：')
            print(index)
            # self.current_expert_id = expert_id_list[index]
            # print(self.current_expert_id)
            article_sources_list = article_source_list[index].split('<edms/>')
            article_urls_list = article_url_list[index].split(',http')
            # 对于每个专家的url列表
            if len(article_urls_list) > 0:
                for url_index in range(0, len(article_urls_list)):
                    # print(url_index)
                    if url_index > 0:
                        article_urls_list[url_index] = 'http' + article_urls_list[url_index]
                    if url_index < len(article_sources_list):
                        current_expert_id = expert_id_list[index]
                        current_article_source = article_sources_list[url_index]
                        # print(current_expert_id)
                        # print(current_article_source)
                        yield scrapy.Request(url=article_urls_list[url_index], callback=self.parse,
                                             meta={"current_expert_id": current_expert_id,
                                                   "current_article_source": current_article_source})
            else:
                print('\n该专家无资讯快照')

    # 初步清洗源数据
    def clean_original_content(self, content_list):
        # 正则表达式,去除'<'与'>'之间的值
        re_pattern = re.compile(r'<(.*?)>', re.S)

        content = ''
        if len(content_list) > 0:
            content_raw = ''.join(content_list)
            content = re_pattern.sub('', content_raw)
            content = content.replace('\\', '').replace('\'', '').replace('\"', '').replace('\n', '').replace('\t', '')
            content += '<edms/>'

        return content

    # 处理页面的parse方法
    def parse(self, response):
        print("\n### Method ### Enter Method: parse")

        # 数据库连接
        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='yinyuwei', db='edms', charset='utf8')
        cur = conn.cursor()

        r = response
        # 解URL编码
        #  url_utf8 = unquote(r.url, 'utf-8')
        # print("\n source_url")
        # print(r.url)
        # print(url_utf8)

        expert_id = r.meta["current_expert_id"]
        article_source = r.meta["current_article_source"]
        print(expert_id)
        print(article_source)
        
        # 确保不爬取已存在的数据：判断该学者的资讯是否已经存在，若存在则不爬取
        print('### Database ### ready to pull data from Database')
        sql = cur.execute('select content, analysis_tag from edms.opinion_raw where `expert_id`="' + expert_id + '"')
        conn.commit()
        db_data = cur.fetchall()

        origin_content = db_data[0][0]
        origin_analysis_tag = db_data[0][1]

        # print(origin_content)
        # print(origin_analysis_tag)

        # 正则表达式,去除'<'与'>'之间的值
        re_pattern = re.compile(r'<(.*?)>', re.S)

        if origin_analysis_tag == 'End':
            print("该专家已获得所有content数据: " + expert_id)
        else:
            if origin_content is None:
                origin_content = ''
            this_content = ''
            # 根据不同的网站结构提取新闻正文
            if article_source == '网易':
                content_list = r.css('div.post_text').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div.content').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '百家号':
                content_list = r.css('div.article-content p').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
            
            elif article_source == '凤凰网':
                content_list = r.css('div#artical_real').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '仪器信息网':
                # 几乎全是长列表
                content_list = r.css('div#newContent').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '中国教育':
                content_list = r.css('div.TRS_Editor').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('table#tabletext').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '搜狐':
                content_list = r.css('div.main').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div.article-main').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '中国教育在线':
                content_list = r.css('div#mcontent').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '科学网':
                content_list = r.css('div#content1').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '中国高校之窗':
                content_list = r.css('div.content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '陕西省教育厅':
                # 几乎全是长列表
                content_list = r.css('div.content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '中国考研网':
                pass

            elif article_source == '人民网':
                content_list = r.css('div#p_content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('FONT').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == 'MBA中国网':
                content_list = r.css('div.cont ').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '新浪新闻':
                content_list = r.css('div#artibody').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div#article').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '搜狐教育':
                content_list = r.css('div#contentText').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('article.article').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)
                    else:
                        content_list = r.css('div.article').extract()
                        if len(content_list) > 0:
                            this_content += self.clean_original_content(content_list)

            elif article_source == '腾讯网':
                content_list = r.css('div#Cnt-Main-Article-QQ').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div#ArticleCnt').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '新浪':
                content_list = r.css('div#artibody').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '新东方':
                content_list = r.css('div.air_con').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '网易财经':
                content_list = r.css('div.post_text').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '好买基金网':
                content_list = r.css('div.content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div.post_text').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '中国网':
                # 几乎全是长列表
                content_list = r.css('div.content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '教育部':
                # 全是长列表
                pass

            elif article_source == '腾讯新闻':
                content_list = r.css('div#Cnt-Main-Article-QQ').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div#ArticleCnt').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '搜狐新闻':
                content_list = r.css('div#contentText').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('td.content').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '道客巴巴':
                # 多为网页pdf文件或word文件,难以提取
                pass

            elif article_source == '中国教育新闻网':
                content_list = r.css('div#body').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div.contentdiv').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '中国社会科学网':
                content_list = r.css('div.f-main-leftMain-content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '知网空间':
                # 基本上是论文摘要
                pass

            elif article_source == '中国青年网':
                # 无法进入该网站
                pass

            elif article_source == '中国教育装备采购网':
                content_list = r.css('div.main').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '高考网':
                # 大多为长表格
                pass

            elif article_source == '中国教育在线考研':
                # 少有专家观点
                pass

            elif article_source == '铜川市人民政府网':
                # 大多为长表格
                pass

            elif article_source == '慧聪网':
                content_list = r.css('div.endInfoContent').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '清华大学新闻网':
                content_list = r.css('article.article').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '大众网':
                content_list = r.css('div.news-con').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '南开大学新闻网':
                content_list = r.css('span.main').extract()
                if len(content_list) > 0:
                    # 只取第一段内容
                    content_raw = content_list[0]
                    content = re_pattern.sub('', content_raw)
                    content = content.replace('\\', '').replace('\'', '').replace('\"', '').replace('\n', '')\
                        .replace('\t', '')
                    content += '<edms/>'
                    this_content += content

            elif article_source == '新华网':
                content_list = r.css('div#content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '中国建筑学会':
                # 大多是长表格
                pass

            elif article_source == '豆丁网':
                # 大多是pdf,难以爬取
                pass

            elif article_source == '中国财经信息网':
                content_list = r.css('div#tdcontent').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '环球网':
                content_list = r.css('div#text').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '中国广播网':
                content_list = r.css('div.TRS_Editor').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '荆楚网':
                # 502 Bad Gateway
                pass

            elif article_source == '视觉同盟':
                content_list = r.css('td.content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)

            elif article_source == '和讯网':
                content_list = r.css('div#artibody').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div.art_context').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == 'e书联盟':
                # 大多是pdf,难以爬取
                pass

            elif article_source == '浙江在线':
                content_list = r.css('article.content').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div.contentContent').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            elif article_source == '北方网':
                content_list = r.css('div#article').extract()
                if len(content_list) > 0:
                    this_content += self.clean_original_content(content_list)
                else:
                    content_list = r.css('div#Content').extract()
                    if len(content_list) > 0:
                        this_content += self.clean_original_content(content_list)

            else:
                pass
            
            if this_content == '':
                print('该网站未爬取内容')
            else:
                # 存储该行入数据库
                try:
                    print('### Database ### ready to update Database: ' + expert_id)
                    sql_sentence = 'update edms.opinion_raw set `content`="' + (origin_content + this_content) + \
                                   '", analysis_tag="ing" where expert_id="' + expert_id + '" limit 1'
                    # print(sql_sentence)
                    sql = cur.execute(sql_sentence)
                    if sql == 1:
                        print("~~~~~ Update Success ~~~~~")
                        cur.close()
                        conn.commit()
                    else:
                        print("!!!!!!!!!!!!!!! Error  rollback !!!!!!!!!!!!!!!")
                        cur.close()
                        conn.rollback()
                except Exception as e:
                    print("!!!!!!!!!!!!!!! Exception  rollback !!!!!!!!!!!!!!!")
                    print(e.message)
                    cur.close()
                    conn.rollback()

        # 数据库断开连接
        conn.close()
