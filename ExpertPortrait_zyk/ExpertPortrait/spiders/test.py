# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import requests
import re
from ExpertPortrait.items import ExpertportraitItem
from urllib.parse import unquote

school_names = ['清华大学', '浙江大学', '北京大学', '吉林大学', '上海交通大学', '华中科技大学', '武汉大学', '四川大学',
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
school_ids = ['1710', '2507', '426', '1194', '1965', '996', '2054', '2006', '1112', '1923', '2151', '325', '2434', '732',
              '3112', '2418', '497', '3627', '434', '287', '2525', '3078', '2066', '1122', '990', '2012', '2982', '3120',
              '1310', '969', '4020', '3323', '86', '1553', '843', '1403', '1890', '2076', '1204', '2826', '2945', '1264',
              '535', '1559', '1556', '745', '3193', '2558', '1508', '3722', '1397', '612', '1520', '2890', '199', '1170',
              '2925', '2078', '1549', '3412', '257', '1522', '1304', '1177', '168', '846', '4109', '203', '3589', '1423',
              '150', '2489', '2074', '514', '998', '494', '1578', '614', '490', '1888', '1474', '607', '4146', '2337',
              '666', '2098', '1291', '2991', '3937', '286', '850', '42', '2874', '3107', '1327', '3119', '3634', '3265',
              '4139', '2903', '2541', '3213', '4113', '1674', '63537', '1565', '3432', '3875', '2942', '621', '2587', '92945']
keywords = ['经济', '文', '医', '法', '政治', '美术', '管理', '新闻与传播', '马克思']

class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['www.irtree.cn']
    # 需要手动输入学院链接
    start_urls = ['http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id=1710']

    # 得到每个学校里院系所导航页面的页数
    def parse(self, response):
        item = ExpertportraitItem()
        id = TestSpider.start_urls[0].split('=')[-1]
        id_index = school_ids.index(id)
        school_name = school_names[id_index]
        item['university'] = school_name
        sel =Selector(response)
        col_pages = sel.xpath('/html/body/div/div/span/text()').extract_first()
        col_pages = col_pages.split('/')[-1].strip()
        if int(col_pages):
            x = 0
        #for x in range(int(col_pages)):
            col_page = str(x+1)
            col_page_url=(TestSpider.start_urls[0]+'&pageIndex='+col_page)
            yield Request(col_page_url, callback=self.parse_getcol, meta = {'item_l':item})

    # 进入每个学院
    def parse_getcol(self, response):
        item_l = response.meta['item_l']
        items = []
        sel = Selector(response)
        cols = sel.xpath('/html/body/div/ul/li/a')
        for col in cols[1:]:
            url = col.xpath('./@href').extract_first()
            col_name_code = re.search('organname=(.*?)&cpage',url).group(1)
            col_name = unquote(col_name_code)
            for keyword in keywords:
                if keyword in col_name:
                    item = ExpertportraitItem()
                    item['university'] = item_l['university']
                    item['college'] = col_name
                    item['col_url'] = 'http://www.irtree.cn' + url
                    items.append(item)
                    break
        for item in items:
            yield Request(item['col_url'], callback=self.parse_college, meta = {'item_l':item})

    # 获取每个专家的url
    def parse_college(self, response):
        page_url = response.url
        item_l = response.meta['item_l']
        items = []
        sel = Selector(response)
        urls = sel.xpath('//*[@id="author"]/div[1]/dl/dt/a[1]/@href').extract()
        for url in urls:
            item = ExpertportraitItem()
            item['university'] = item_l['university']
            item['college'] = item_l['college']
            item['expert_url'] = 'http://www.irtree.cn'+url
            item['expert_id'] = re.search('writer/(.*?)/rw_zp.aspx',url).group(1)
            items.append(item)
        for item in items:
            #print(item['university']+' '+item['college']+' '+item['expert_url'])
            yield Request(url=item['expert_url'], callback=self.parse_content, meta={'item_l': item})
        #翻页
        # next_page = sel.xpath('//*[@id="author"]/div[2]/div[2]/span[2]/a[3]/@href').extract_first()
        # if next_page:
        #     next_page = re.search(r"g_GetGotoPage\('(.*?)'\)", next_page).group(1)
        #     next_url = page_url.split('&q=%7B%22page')[0]+'&q=%7B"page"%3A"'+next_page+'"%7D'
        #     yield Request(next_url, callback=self.parse_college,meta = {'item':item})

    # 分析每个专家主页（发文量需要大于等于3）
    def parse_content(self, response):
        item_l = response.meta['item_l']
        item = ExpertportraitItem()
        item = item_l
        sel = Selector(response)
        paper_count = sel.xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[3]/p/i/text()').extract_first()
        paper_count = int(paper_count.strip())
        if paper_count >= 3:
            name = sel.xpath('/html/body/div[2]/div/div[1]/h1/text()').extract_first()
            item['expert_name'] = name.strip()
            item['amount1'] = str(paper_count)

            ## 研究主题
            themes = sel.xpath('//*[@class="summary"]/p[4]/text()').extract_first()
            if themes:
                tmp = themes.strip().lstrip(" 研究主题：").split()
                theme_list ='、'.join(tmp)
                #print(theme_list)
                item['theme_list'] = theme_list

            ## 研究学科
            subs = sel.xpath('//*[@class="summary"]/p[5]/text()').extract_first()
            if subs:
                tmp = subs.lstrip(" 研究学科：").rstrip("    ").split()
                sub_list ='、'.join(tmp)
                #print(sub_list)
                item['sub_list'] = sub_list

            # ## 发文量
            # amount1 = sel.xpath('//*[@class="search_count"]/p/i/text()').extract_first().replace(' ', '').replace('\n',
            #                                                                                                       '')
            # amount1 = amount1.lstrip('\r')
            # # print(amount1)
            # item['amount1'] = amount1

            ## 被引量
            amount2 = sel.xpath('//*[@class="summary"]/p[6]/span[2]/i/a/text()').extract_first()
            if amount2:
                amount2 = amount2.replace(',', '')
            # print(amount2)
                item['amount2'] = amount2

            ## H指数
            h_index = sel.xpath('//span[@class="hzs"]/i/text()').extract_first()
            #print(h_index)
            item['h_index'] = h_index

            tags = sel.xpath('//p[@class="data"]/span/text()').extract()[2:]
            nums = sel.xpath('//p[@class="data"]/span/i/a/text()').extract()[1:]

            item['core'] = ''
            item['cssci'] = ''
            item['rdfybkzl'] = ''
            for tag in tags:
                if tag == '北大核心: ':
                    n = tags.index(tag)
                    item['core'] = nums[n].strip()
                if tag ==  'CSSCI: ':
                    m = tags.index(tag)
                    item['cssci'] = nums[m].strip()
                if  tag == 'RDFYBKZL: ':
                    l = tags.index(tag)
                    item['rdfybkzl'] = nums[l].strip()

            #print(item['university'] + ' ' + item['college'] + ' ' + item['expert_url']+' '+item['amount1']+' '+item['h_index'])
            # 总页数
            tpagenum = sel.xpath('//*[@class="pages"]/span[1]/text()').extract_first()
            if tpagenum:
                pagenum = int(tpagenum.lstrip('共').rstrip('页'))
            #print(pagenum)
            # for i in range(1, pagenum+1):
            ## TEST ###
            # for i in range(1, 2):
            #     paper_url = item['expert_url'] + '?q=%7B%22page%22%3A%22' + str(i) + '%22%7D'
            #     #print(paper_url)
            #     yield Request(paper_url, callback=self.get_papers, meta={'expert_name': item['expert_name'],
            #                                                  'expert_id': item['expert_id']})


            tp_url = item['expert_url'].rstrip("zp.aspx") + "tp.aspx"
            #print(tp_url)
            yield Request(url=tp_url,  callback=self.parse_tp, meta = {'item_l': item})

    def get_papers(self, response):
        sel = Selector(response)
        expert_name = response.meta['expert_name']
        expert_id = response.meta['expert_id']
        urls = sel.xpath('//*[@class="search_list"]//dt//@href').extract()

        ## 所有论文链接
        url_list = []
        # for url in urls:
        #     tmp = "http://www.irtree.cn" + url
        #     url_list.append(tmp)
            #yield Request(tmp, callback=lambda response, id=id: self.parse3(response, id))

        ### TEST ###
        tmp = "http://www.irtree.cn" + urls[0]
        yield Request(tmp, callback=self.parse_paper ,meta= {'expert_name': expert_name,
                                                             'expert_id': expert_id})
        ## TEST ###

        #print(url_list)

    def parse_paper(self, response):
        sel = Selector(response)
        expert_name = response.meta['expert_name']
        expert_id = response.meta['expert_id']
        print(expert_name)
        print(expert_id)
        url = response.url
        print(url)
        ## 论文ID
        paper_id = url.lstrip("http://www.irtree.cn/").rstrip("/article_detail.aspx").split("/articles/")[1].strip()
        #print(paper_id)
        title = sel.xpath('//*[@class="summary"]/h1/text()').extract_first().strip()
        #print(title)
        ## 文献类型
        paper_type = sel.xpath('//p[@class="class"]/text()').extract_first().strip()
        ## 出处
        source = 'Null'
        tmp = sel.xpath('//*[@class="article_detail "]/p[5]/text()').extract_first()
        if tmp:
            tmp = tmp.strip()
            source = tmp
        #print(paper_id+' '+title+' '+type+' '+source)
        ## 收录情况
        cover_info = ''
        # tmp = sel.xpath('//*[@class="article_detail "]/p[12]/text()').extract_first()
        # if tmp:
        #     tmp = tmp.strip()
        #     cover_info = tmp
        print(paper_id+' '+title+' '+paper_type+' '+source)
        ## 摘要
        abstract = sel.xpath('//p[@class="abstrack"]/text()').extract_first()
        if abstract:
            abstract = abstract.strip()
        print(abstract)
        ## 关键词
        tmp = sel.xpath('//p[@class="subject"]/text()').extract()
        if tmp:
            keywords = ' '.join(tmp)
            keywords = re.sub(r"\s{2,}", " ", keywords).strip()
        print(keywords)
        ## 作者
        tmp = sel.xpath('//p[@class="author"]/text()').extract()
        authors = ' '.join(tmp)
        authors = re.sub(r'\[.*?\]','',authors)
        authors = re.sub(r"\s{2,}", " ", authors).strip()
        #authors = authors.split()
        print(authors)
        authors_list = authors.split()
        for a in authors_list:
            if a == expert_name:
                num = authors_list.index(a)
        if num == 0:
            author1 = expert_id
            print('author1='+author1)
        elif num == 1:
            author2 = expert_id
            print('author2='+author2)
        elif num == 2:
            author3 = expert_id
            print('author3='+author3)
        elif num == 3:
            author4 = expert_id
            print('author4='+author4)
        elif num == 4:
            author5 = expert_id
            print('author5='+author5)
        print('-------------------------------------------------------')

    def parse_tp(self, response):
        item_l = response.meta['item_l']
        item = ExpertportraitItem()
        item = item_l
        sel = Selector(response)
        url = response.url
        ## 合作学者
        co_experts_urls = sel.xpath('//*[@class="list_writer"]//dt//@href').extract()
        co_experts_list = []
        for url in co_experts_urls:
            tmp = url.rstrip("/rw.aspx").split("/writer/")[1]
            co_experts_list.append(tmp)

        item['co_experts'] = str(co_experts_list)
        ## 合作机构
        co_agency_list = sel.xpath('//*[@class="list organ"]//li//@title').extract()
        item['co_agencies'] = str(co_agency_list)
        yield item
