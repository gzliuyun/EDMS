# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import re
from ExpertPortrait.items import person,paper
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



class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['www.irtree.cn']
    # 需要手动输入学院链接
    #start_urls = ['http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id=2507']
    start_urls = []
    traveled = []
<<<<<<< HEAD
    #
    def __init__(self):
        head = 'http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id='
        for id in school_ids[60:]:
            tmp = head + str(id)
            self.start_urls.append(tmp)
=======

    def __init__(self):
        head = 'http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id='
        for id in school_ids:
                tmp = head + str(id)
                self.start_urls.append(tmp)

        # 载入已经爬过的学院ID
        with open("traveled.txt", "r", encoding='utf-8') as f:
            tmp = f.readlines()
            for t in tmp:
                self.traveled.append(t.rstrip('\n').split(' '))
>>>>>>> master

        # 载入已经爬过的学院ID
        with open("traveled.txt", "r") as f:
            tmp = f.readlines()
            for t in tmp:
                self.traveled.append(t.rstrip('\n').split(' '))

    # 得到每个学校里院系所导航页面的页数
    def parse(self, response):
        item = person()
        url = response.url
        id = url.split('=')[-1]
        id_index = school_ids.index(id)
        school_name = school_names[id_index]
        # print(school_name+str(id_index)+' :'+id)
        item['university'] = school_name
        #print(url + item['university'])
        sel =Selector(response)
        col_pages = sel.xpath('/html/body/div/div/span/text()').extract_first()
        col_pages = col_pages.split('/')[-1].strip()
        if int(col_pages):
            for x in range(int(col_pages)):
            # x = 1
                col_page = str(x+1)
                col_page_url = (url+'&pageIndex='+col_page)
                yield Request(col_page_url, callback=self.parse_getcol, meta={'item_l': item})

    # 进入每个学院
    def parse_getcol(self, response):
        item_l = response.meta['item_l']
        # print(response.url+item_l['university'])
        items = []
        sel = Selector(response)
        cols = sel.xpath('/html/body/div/ul/li/a')
        for col in cols[1:]:
            url = col.xpath('./@href').extract_first()
            col_name_code = re.search('organname=(.*?)&cpage',url).group(1)
            col_name = unquote(col_name_code)
            # 检测是否爬过该学院
            sid = url.split("/author.aspx?idlevel=")[0].lstrip('/')
            traveled_flag = False
            for t in self.traveled:
                if sid == t[0] and col_name == t[1]:
                    traveled_flag = True
                    break
            if traveled_flag:
                return
            item = person()
            item['university'] = item_l['university']
            item['college'] = col_name
            item['col_url'] = 'http://www.irtree.cn' + url
            items.append(item)
        for item in items:
            yield Request(item['col_url'], callback=self.parse_college, meta={'item_l': item}, dont_filter=False)

    # 获取每个专家的url
    def parse_college(self, response):
        item_l = response.meta['item_l']
        page_url = response.url
        if page_url == 'http://www.irtree.cn/tootip.html':
            university = item_l['university']
            index = school_names.index(university)
            id = school_ids[index]
            for_url = 'http://www.irtree.cn/Template/t5/UserControls/CollegeNavigator.ascx?id=' + id
            with open('forbidden.txt', 'a', encoding='utf-8') as file:
                tmp = '没有权限:' + university + '\n'+for_url + '\n'
                file.write(tmp)
        else:
            print(page_url)

            # 检测是否爬过该学院
            h1 = page_url.split("&organname=")[0]
            h2 = h1.lstrip("http://www.irtree.cn/")
            sid = h2.split("/author.aspx?idlevel=")[0]
            cid = h2.split("/author.aspx?idlevel=")[1]
            traveled_flag = False
            for t in self.traveled:
                if sid == t[0] and cid == t[1]:
                    traveled_flag = True
                    break
            if traveled_flag:
                return

            items = []
            sel = Selector(response)
            urls = sel.xpath('//*[@id="author"]/div[1]/dl/dt/a[1]/@href').extract()
            if not urls:
                urls = urls = sel.xpath('//*[@id="author"]/div/div[1]/dl/dt/a[1]/@href').extract()
            for url in urls:
                #print(url)
                item = person()
                item['university'] = item_l['university']
                item['college'] = item_l['college']
                item['expert_url'] = 'http://www.irtree.cn'+url
                item['expert_id'] = re.search('writer/(.*?)/rw_zp.aspx',url).group(1)

                # print(item)
                items.append(item)
            for item in items:
                # print(item['university']+' '+item['college']+' '+item['expert_url'])
                yield Request(url=item['expert_url'], callback=self.parse_content, meta={'item_l': item})
            #翻页
            next_page = sel.xpath('//*[@id="author"]/div[2]/div[2]/span[2]/a[3]/@href').extract_first()
            if next_page:
                next_page = re.search(r"g_GetGotoPage\('(.*?)'\)", next_page).group(1)
                next_url = page_url.split('&q=%7B%22page')[0]+'&q=%7B"page"%3A"'+next_page+'"%7D'
                yield Request(next_url, callback=self.parse_college,  meta={'item_l':item_l})
<<<<<<< HEAD

            # 该学院已爬完，添加至traveled.txt中
            with open("traveled.txt", "a") as f:
                tmp = sid + " " + cid + "\n"
                f.write(tmp)

=======
            else:
                # 该学院已爬完，添加至traveled.txt中
                with open("traveled.txt", "a", encoding='utf-8') as f:
                    sid = page_url.split("/author.aspx?idlevel=")[0].lstrip('http://www.irtree.cn/')
                    cid = item_l['college']
                    tmp = sid + " " + cid + "\n"
                    f.write(tmp)
>>>>>>> master
    # 分析每个专家主页（发文量需要大于等于3）
    def parse_content(self, response):
        item_l = response.meta['item_l']
        item = person()
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
            amount2 = sel.xpath('//span[@class="zps"]/i/a/text()').extract_first()
            if amount2:
                amount2 = amount2.replace(',', '')
                #print(amount2)
            else:
                amount2 = sel.xpath('//span[@class="zps"]/i/text()').extract_first()
                amount2 = amount2.replace(',', '')
            item['amount2'] = amount2

            ## H指数
            h_index = sel.xpath('//span[@class="hzs"]/i/text()').extract_first()
            #print(h_index)
            item['h_index'] = h_index

            tags = sel.xpath('//p[@class="data"]/span')
            #nums = sel.xpath('//p[@class="data"]/span/i/a/text()').extract()[1:]

            item['core'] = ''
            item['cssci'] = ''
            item['rdfybkzl'] = ''
            for tag in tags:
                tag_text = tag.xpath('./text()').extract_first()
                if tag_text == '北大核心: ':
                    core = tag.xpath('./i/a/text()').extract_first()
                    item['core'] = core
                if tag_text ==  'CSSCI: ':
                    cssci = tag.xpath('./i/a/text()').extract_first()
                    item['cssci'] = cssci
                if tag_text == 'RDFYBKZL: ':
                    rdf = tag.xpath('./i/a/text()').extract_first()
                    item['rdfybkzl'] = rdf

            #print(item['university'] + ' ' + item['college'] + ' ' + item['expert_url']+' '+item['amount1']+' '+item['h_index'])
            # 总页数
            tpagenum = sel.xpath('//*[@class="pages"]/span[1]/text()').extract_first()
            if tpagenum:
                pagenum = int(tpagenum.lstrip('共').rstrip('页'))
            #print(pagenum)
            for i in range(1, pagenum+1):
                paper_url = item['expert_url'] + '?q=%7B%22page%22%3A%22' + str(i) + '%22%7D'
                yield Request(paper_url, callback=self.get_papers, meta={'expert_name': item['expert_name'],
                                                             'expert_id': item['expert_id']})


            tp_url = item['expert_url'].rstrip("zp.aspx") + "tp.aspx"
            #print(tp_url)
            yield Request(url=tp_url,  callback=self.parse_tp, meta = {'item_l': item})

    def get_papers(self, response):
        sel = Selector(response)
        expert_name = response.meta['expert_name']
        expert_id = response.meta['expert_id']
        urls = sel.xpath('//a[@class="title"]/@href').extract()

        # ## 所有论文链接
        #url_list = []
        for url in urls:
            if 'article_detail.aspx' in url:
                tmp = "http://www.irtree.cn" + url
                #url_list.append(tmp)
                yield Request(tmp, callback=self.parse_paper, meta={'expert_name': expert_name,
                                                                     'expert_id': expert_id}, dont_filter=True)


    def parse_paper(self, response):
        sel = Selector(response)
        expert_name = response.meta['expert_name']
        expert_id = response.meta['expert_id']
        #print(expert_name)
        #print(expert_id)
        url = response.url
        #print(url)

        it = paper()
        ## 论文ID
        paper_id = url.lstrip("http://www.irtree.cn/").rstrip("/article_detail.aspx").split("/articles/")[1].strip()
        it['paper_id'] = paper_id
        title = sel.xpath('//*[@class="summary"]/h1/text()').extract_first().strip()
        it['paper_title'] = title
        ## 文献类型
        paper_type = sel.xpath('//p[@class="class"]/text()').extract_first().strip()
        it['paper_type']=paper_type
        ## 出处
        source = 'Null'
        date = 'Null'
        p_list = sel.xpath('//div[@class="m"]/div[2]/p')
        #text_list = sel.xpath('//div[@class="m"]/div[2]/p/text()').extract()
        for p in p_list:
            p_text = p.xpath('./strong/text()').extract_first()
            if p_text == '会议名称：':
                tmp = p.xpath('./text()').extract_first()
                if tmp:
                    source = tmp.strip()
            if p_text == '出　　处：':
                tmp = p.xpath('./text()').extract_first()
                if tmp:
                    source = tmp.strip()
            if p_text in ['出版日期：', '年　　份：', '会议日期：', '发布日期：', '学位年度：', '公布年份：', '申 请 日：']:
                tmp = p.xpath('./text()').extract_first()
                if tmp:
                    datet = tmp.strip()
                    if datet != '0':
                        date = datet

        # tmp = sel.xpath('//p[@class="from"]/text()').extract_first()
        # if tmp:
        #     tmp = tmp.strip()
        #     source = tmp
        it['source'] = source
        it['date'] = date
        #print(paper_id+' '+title+' '+type+' '+source)

        ## 摘要
        abstract = ''
        abstrack = sel.xpath('//p[@class="abstrack"]/text()').extract_first()
        if abstrack:
            abstract = abstrack.strip()
        else:
            abstrack2 = sel.xpath('//p[@class="abstrack cboth"]/text()').extract_first()
            if abstrack2:
                abstract = abstrack2.strip()
        it['abstract'] = abstract
        ## 关键词
        keywords = ''
        tmp = sel.xpath('//p[@class="subject"]/text()').extract()
        if tmp:
            keywords = ' '.join(tmp)
            keywords = re.sub(r"\s{2,}", " ", keywords).strip()
        it['keyword'] = keywords
        ## 作者
        it['p_author1'] = ''
        it['p_author2'] = ''
        it['p_author3'] = ''
        it['p_author4'] = ''
        it['p_author5'] = ''
        tmp = sel.xpath('//p[@class="author"]/text()').extract()
        authors = ' '.join(tmp)
        authors = re.sub(r'\[.*?\]','',authors)
        authors = re.sub(r"\s{2,}", " ", authors).strip()
        it['p_authors'] = authors
        #authors = authors.split()
        authors_list = authors.split()
        for a in authors_list:
            if a == expert_name:
                num = authors_list.index(a)
        if num == 0:
            it['p_author1'] = expert_id
            #print('author1='+author1)
        elif num == 1:
            it['p_author2'] = expert_id
            #print('author2='+author2)
        elif num == 2:
            it['p_author3'] = expert_id
            #print('author3='+author3)
        elif num == 3:
            it['p_author4'] = expert_id
            #print('author4='+author4)
        elif num == 4:
            it['p_author5'] = expert_id
            #print('author5='+author5)
        yield it
        # print(expert_name+':'+it['paper_id']+'--'+it['p_author1']+' '+it['p_author2'])
        #print('-------------------------------------------------------')


    def parse_tp(self, response):
        item_l = response.meta['item_l']
        item = person()
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
        #print(item)
        yield item
