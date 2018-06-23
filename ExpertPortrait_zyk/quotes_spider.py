import json

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "peoples"

    def start_requests(self):

        urls = [
            'http://www.cnic.cas.cn/yfdw/zgj/index.html',
            'http://www.cnic.cas.cn/yfdw/zgj/index_1.html',
        ]
        # f = open('iaa.txt')
        # urls = f.readlines()
        for url in urls:
            yield scrapy.Request(url=url.strip(), callback=self.parse_cnic)

    def parse_cnic(self, response):
        # response.css('div.TRS_Editor table p font strong')
        for href in response.xpath('//div[@class="title-pic"]//h5/a/@href').extract():
            i = href.index('json=') + 5
            yield response.follow(href[i:], self.parse_cnic_detail)

    def parse_cnic_detail(self, response):
        # response.css('div.TRS_Editor table p font strong')
        r = json.loads(response.body.decode('utf-8')[9:-2])
        print(r)
        yield r
        # print(name)

    def parse_ia_detail4(self, response):
        # response.css('div.TRS_Editor table p font strong')
        name2 = response.xpath('//strong[text()="基本信息 "]').extract_first()
        name = response.xpath('//td/strong[text()="姓名"]/parent::*/following-sibling::*[1]/text()').extract_first()
        # print(name)
        if name2 is not None:
            yield {
                'url': response.url,
                # 'name': response.xpath('//td/strong[text()="姓名"]/parent::*/following-sibling::*[1]/text()').extract_first().strip(),
                # 'sex': response.xpath('//td/strong[text()="性别"]/parent::*/following-sibling::*[1]/text()').extract_first().strip(),
                #
                # 'position': ' '.join(response.xpath('//td/p/span/font[text()="职务"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'title': ' '.join(response.xpath('//td/p/span/font[text()="职称"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'brief': ' '.join(response.xpath('//td/p/span/font[text()="简历"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # #'brief2': ' '.join(response.xpath('//td/p/span[text()="研究领域"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'field': ' '.join(response.xpath('//td/p/span/font[text()="研究领域"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'acadmic': ' '.join(response.xpath('//td/p/span/font[text()="学术任职"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'achievement': ' '.join(response.xpath('//td/p/span/font[text()="学术成就"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'project': ' '.join(response.xpath('//td/p/span/font[text()="在研课题"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),

            }

    def parse_ia_detail3(self, response):
        # response.css('div.TRS_Editor table p font strong')
        name = response.xpath('//td/p/span/font[text()="姓名"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p/span//text()').extract_first()
        # print(name)
        if name is not None:
            yield {
                'name': response.xpath('//td/p/span/font[text()="姓名"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract_first().strip(),
                'sex': response.xpath('//td/p/span/font[text()="性别"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract_first().strip(),
                'url': response.url,
                'position': ' '.join(response.xpath('//td/p/span/font[text()="职务"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'title': ' '.join(response.xpath('//td/p/span/font[text()="职称"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'brief': ' '.join(response.xpath('//td/p/span/font[text()="简历"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                #'brief2': ' '.join(response.xpath('//td/p/span[text()="研究领域"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'field': ' '.join(response.xpath('//td/p/span/font[text()="研究领域"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'acadmic': ' '.join(response.xpath('//td/p/span/font[text()="学术任职"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'achievement': ' '.join(response.xpath('//td/p/span/font[text()="学术成就"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'project': ' '.join(response.xpath('//td/p/span/font[text()="在研课题"]/parent::*/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),

            }

    def parse_ia_detail2(self, response):
        # response.css('div.TRS_Editor table p font strong')
        name = response.xpath('//td/p/span[text()="姓名："]/parent::*/parent::*/following-sibling::*[1]/p/span/text()').extract_first()
        # print(name)
        if name is not None:
            yield {
                'name': response.xpath('//td/p/span[text()="姓名："]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract_first().strip(),
                'sex': response.xpath('//td/p/span[text()="性别："]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract_first().strip(),
                'url': response.url,

                'title': ' '.join(response.xpath('//td/p/span[text()="职称："]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'brief': ' '.join(response.xpath('//td/p/span[text()="个人简介"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),

                'field': ' '.join(response.xpath('//td/p/span[text()="研究方向："]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'acadmic': ' '.join(response.xpath('//td/p/span[text()="当前工作："]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                'achievement': ' '.join(response.xpath('//td/p/span[text()="个人成就："]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),

            }

    def parse_ia_detail(self, response):
        # response.css('div.TRS_Editor table p font strong')
        name = response.xpath('//td//span[text()="姓名"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract_first()
        #name = response.xpath('//td/p/span[text()="姓名"]/parent::*/parent::*/following-sibling::*[1]/p/span/text()').extract_first()
        # print(name)
        if name is not None:
            yield {
                'url': response.url,
                # 'name': name,
                # 'sex': response.xpath('//td/p/span[text()="性别"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract_first().strip(),
                #
                # 'position': ' '.join(response.xpath('//td/p/span[text()="职务"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'title': ' '.join(response.xpath('//td/p/span[text()="职称"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'brief': ' '.join(response.xpath('//td/p/span[text()="简历"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # #'brief2': ' '.join(response.xpath('//td/p/span[text()="研究领域"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'field': ' '.join(response.xpath('//td/p/span[text()="研究领域"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'acadmic': ' '.join(response.xpath('//td/p/span[text()="学术任职"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'achievement': ' '.join(response.xpath('//td/p/span[text()="学术成就"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                # 'project': ' '.join(response.xpath('//td/p/span[text()="在研课题"]/parent::*/parent::*/following-sibling::*[1]/p//text()').extract()).replace('\r', '').replace('\n', '').replace('\t', '').strip(),
            }

    def parse_ia(self, response):
        # response.css('div.TRS_Editor table p font strong')
        for href in response.xpath('//div[@class="col-sm-6 col-md-3"]//h5/a/@href').extract():
            # print(href)
            yield {"href":href}#response.follow(href, self.parse_ict_detail)
        next_page = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_ia)

    def parse_ict(self, response):

        lab = ['计算机科学国家重点实验室', '可信计算与信息保障实验室', '并行软件与计算科学实验室', '基础软件国家工程研究中心', '人机交互技术与智能信息处理实验室', '软件工程技术研究开发中心',
               '天基综合信息系统重点实验室']

        idx = -1

        # response.css('div.TRS_Editor table p font strong')
        for href in response.css('td[height="26"] a::attr(href)').extract():
            # print(href)
            yield response.follow(href, self.parse_ict_detail)

    def parse_ict_detail(self, response):
        # field = response.css('table[width="98%"] tr')[3].css('td::text').extract()[0].strip()
        # if field == '':
        #     field = response.css('table[width="98%"] tr')[3].css('td div p::text').extract_first().strip()
        def strip(str):
            return str.strip() if str is not None else None
        yield {
            'name': response.css('table[width="98%"] tr')[1].css('td::text').extract()[0].strip(),
            'sex': response.css('table[width="98%"] tr')[1].css('td::text').extract()[1].strip(),
            'contact': response.css('table[width="98%"] tr')[2].css('td::text').extract()[0].strip(),
            'title': response.css('table[width="98%"] tr')[2].css('td::text').extract()[1].strip(),
            'field': strip(''.join(response.css('td[id="td1"]').xpath('descendant-or-self::*/text()').extract())),
            'introduction': strip(''.join(response.css('td[id="td0"]').xpath('descendant-or-self::*/text()').extract())),
            'social': strip(''.join(response.css('td[id="td2"]').xpath('descendant-or-self::*/text()').extract())),
            'prize': strip(''.join(response.css('td[id="td3"]').xpath('descendant-or-self::*/text()').extract())),
            'paper': strip(''.join(response.css('td[id="td4"]').xpath('descendant-or-self::*/text()').extract())),
            'project': strip(''.join(response.css('td[id="td5"]').xpath('descendant-or-self::*/text()').extract())),
            'profession': strip(''.join(response.css('td[id="td6"]').xpath('descendant-or-self::*/text()').extract())),
            'bumen': strip(''.join(response.css('td[id="td7"]').xpath('descendant-or-self::*/text()').extract())),
        }

    def parse_is_detail(self, response):

        # response.css('div.TRS_Editor table p font strong')
        cnt = response.css('div#main-content div.container')
        name = cnt.xpath('//div[@class="bp-enty"]//font/text()').extract_first() \
               or cnt.xpath('//div[@class="bp-enty"]//b/text()').extract_first() \
               or cnt.xpath('//div[@class="bp-enty"]//strong/text()').extract_first()
        if name is None:
            name = ''
        elif '\xa0\xa0' in name:
            name = name.split('\xa0\xa0')[0]
        else:
            name = name.split(' ')[0]
        yield {
            'name': name,
            'url' : response.url,
            'edu': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="教育背景"]/parent::*/parent::*//div[1]/div/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            #'exp': ' '.join(cnt.xpath('div[@class="m-itme"][4]//h5[text()="工作简历"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t',''),
            'work': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="工作经历"]/parent::*/parent::*//h5[text()="工作简历"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            'social': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="工作经历"]/parent::*/parent::*//h5[text()="社会兼职"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            'acadmic': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="工作经历"]/parent::*/parent::*//h5[text()="学术事务"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            #'prize1': ' '.join(cnt.xpath('div[@class="m-itme"][5]//h5[text()="工作简历"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t',''),
            'prize': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="专利与奖励"]/parent::*/parent::*//h5[text()="奖励信息"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            'patent': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="专利与奖励"]/parent::*/parent::*//h5[text()="专利成果"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            'paper': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="出版信息"]/parent::*/parent::*//h5[text()="发表论文"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            'book': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="出版信息"]/parent::*/parent::*//h5[text()="发表著作"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            'project': ' '.join(cnt.xpath('div[@class="m-itme"]//span[text()="科研活动"]/parent::*/parent::*//h5[text()="科研项目"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip(),
            #'conference': ' '.join(cnt.xpath('div[@class="m-itme"][4]//h5[text()="工作简历"]/following-sibling::*/text()').extract()).replace('\r','').replace('\n','').replace('\t',''),
        }

    def parse_is(self, response):

        lab = ['计算机科学国家重点实验室', '可信计算与信息保障实验室', '并行软件与计算科学实验室', '基础软件国家工程研究中心', '人机交互技术与智能信息处理实验室', '软件工程技术研究开发中心',
               '天基综合信息系统重点实验室']

        idx = -1

        # response.css('div.TRS_Editor table p font strong')
        for row in response.css('div.TRS_Editor table tr'):
            people = row.css('td p font::text').extract()
            if len(people) == 0:
                idx += 1
                continue
            if row.css('td p font::text').extract()[0] == '导师姓名':
                continue
            peoples = []
            if len(people) == 4:
                print('***************', row.css('td p font a::text').extract_first())
                peoples = [row.css('td p font a::text').extract_first()]
            if len(people) == 6:
                name = people[0] + people[1]
                print('-------------------' + name)
                people.remove(people[0])
                people[0] = name
            peoples += people
            yield {
                'name': peoples[0],
                'title': peoples[1],
                'profession': peoples[2],
                'field': peoples[3],
                'email': peoples[4],
                'lab': lab[idx],
            }

    def parse(self, response):

        def strip(str):
            return str.strip() if str is not None else None

        def extract_id(str):
            start = str.index('(')
            end = str.index(')')
            return str[start+2: end-1]

        for people in response.css('div.card_div'):
            people = people.css('td p font::text').extract()
            yield {
                'title': people[0],
                'profession': people[1],
                'field': people[2],
                'email': people[3],
                'homepage': strip(people.xpath('div/div[2]/div[1]/div[5]/span[2]/a/@href').extract_first()),
            }

    def parse_detail_url(self, response):

        urls = [
            'http://scse.buaa.edu.cn/buaa-css-web/toCardDetailAction.action?firstSelId=CARD_TMPL_OF_FIRST_NAVI_CN&secondSelId=&thirdSelId=d699d016-4df3-4c5a-a7a1-a01c52f214e0&cardId={0}&language=0&curSelectNavId=d699d016-4df3-4c5a-a7a1-a01c52f214e0',
            'http://scse.buaa.edu.cn/buaa-css-web/toCardDetailAction.action?firstSelId=CARD_TMPL_OF_FIRST_NAVI_CN&secondSelId=&thirdSelId=2c9f1172-3adc-45dc-a053-dccf2126483e&cardId={0}&language=0&curSelectNavId=2c9f1172-3adc-45dc-a053-dccf2126483e',
            'http://scse.buaa.edu.cn/buaa-css-web/toCardDetailAction.action?firstSelId=CARD_TMPL_OF_FIRST_NAVI_CN&secondSelId=&thirdSelId=416eeeb2-1901-4730-8b4c-2fd4dd76df25&cardId={0}&language=0&curSelectNavId=416eeeb2-1901-4730-8b4c-2fd4dd76df25'
        ]

        def extract_id(str):
            start = str.index('(')
            end = str.index(')')
            return str[start+2: end-1]

        for people in response.css('div.card_div'):
            url = urls[2].format(extract_id(people.css('span.handle::attr(onclick)').extract_first()))
            yield response.follow(url, self.parse_detail)

    def parse_detail(self, response):
        def strip(str):
            return str.strip() if str is not None else None

        def extract_id(str):
            start = str.index('&cardId=')
            str = str[start+8:]
            end = str.index('&')
            return str[:end]

        for people in response.css('div.card_detail_content'):
            yield {
                'id': extract_id(response.url),
                'zipcode': strip(people.xpath('div[2]/div[4]/span[2]/text()').extract_first()),
                'workplace': strip(people.xpath('div[3]/div[1]/span[2]/text()').extract_first()),
                'introduction': strip(people.xpath('//p[@id="introduceP2"]/text()').extract_first()),
            }
