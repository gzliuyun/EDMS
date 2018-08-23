# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import Request
import re
from teacher.items import TeacherItem

schools = ['海口经济学院', '香港科技大学', '兰州商学院陇桥学院', '武威职业学院', '兰州资源环境职业技术学院', '新疆财经大学商务学院', '塔里木大学', '重庆三峡医药高等专科学校', '重庆医药高等专科学校', '重庆工商大学融智学院', '重庆正大软件职业技术学院', '重庆财经职业学院', '西南大学', '重庆邮电大学', '重庆三峡学院', '重庆工程职业技术学院', '重庆大学', '西南政法大学', '重庆交通大学', '重庆理工大学', '重庆工业职业技术学院', '重庆三峡职业学院', '重庆机电职业技术学院', '西南大学育才学院', '重庆大学城市科技学院', '重庆水利电力职业技术学院', '重庆邮电大学移通学院', '重庆科技学院', '重庆航天职业技术学院', '电子科技大学成都学院', '四川交通职业技术学院', '四川师范大学成都学院', '四川师范大学文理学院', '四川司法警官职业学院', '四川工商职业技术学院', '乐山职业技术学院', '宜宾职业技术学院', '四川中医药高等专科学校', '四川幼儿师范高等专科学校', '四川水利职业技术学院', '四川信息职业技术学院', '南充职业技术学院', '四川航天职业技术学院', '四川外语学院成都学院', '成都理工大学工程技术学院', '四川机电职业技术学院', '四川职业技术学院', '四川财经职业学院', '四川大学锦江学院', '四川音乐学院绵阳艺术学院', '四川艺术职业学院', '四川城市职业学院', '成都艺术职业学院', '四川托普信息技术职业学院', '四川教育学院', '成都理工大学广播影视学院', '四川文化产业职业学院', '首都医科大学', '黑龙江交通职业技术学院', '哈尔滨商业大学广厦学院', '黑龙江工程学院昆仑旅游学院', '黑龙江工商职业技术学院', '黑龙江生态工程职业学院', '黑龙江生物科技职业学院', '哈尔滨工业大学', '沈阳师范大学', '上海商学院', '上海工艺美术职业学院', '上海电子信息职业技术学院', '上海理工大学', '上海海事大学', '上海海洋大学', '上海师范大学', '上海电力学院', '上海金融学院', '上海行健职业学院', '上海交通大学', '上海政法学院', '上海音乐学院', '上海医疗器械高等专科学校', '上海出版印刷高等专科学校', '上海农林职业技术学院', '上海城市管理职业技术学院', '上海海事职业技术学院', '东南大学', '郑州澍青医学高等专科学校', '平顶山教育学院', '河南科技大学', '河南城建学院', '中原工学院', '安阳工学院', '湖北工业大学', '武汉工程大学', '湖北医药学院', '湖北师范学院', '湖北经济学院', '湖北美术学院', '咸宁学院', '黄石理工学院', '武汉商业服务学院', '沙市职业大学', '湖北轻工职业技术学院', '荆州职业技术学院', '长江大学文理学院', '湖北大学知行学院', '湖北师范学院文理学院', '湖北艺术职业学院', '武汉工业职业技术学院', '中南民族大学工商学院', '南昌大学']

class CucdcSpider(scrapy.Spider):
    name = 'cucdc'
    # allowed_domains = ['http://teacher.cucdc.com/school/province/11.html']
    start_urls = ['http://teacher.cucdc.com/laoshi/school/10001.html']

    def parse(self, response):
        sel = Selector(response)
        pro_urls = sel.xpath('//*[@id="searchnav"]/div[1]/a/@href').extract()
        for url in pro_urls:
            pro_url = 'http://teacher.cucdc.com'+url
            yield Request(pro_url, callback=self.get_pros)

    def get_pros(self, response):
        sel = Selector(response)
        pros_urls = sel.xpath('//*[@id="searchrlsn"]/div[1]/div[3]/a/@href').extract()
        for url in pros_urls:
            pros_url = 'http://teacher.cucdc.com'+url
            yield Request(pros_url, callback=self.get_schools, dont_filter=True)

    def get_schools(self, response):
        sel = Selector(response)
        sch_urls = sel.xpath('//table[@width="100%"]/tr')
        for url in sch_urls[1:]:
            sch_url = 'http://teacher.cucdc.com'+url.xpath('./td[1]/a/@href').extract_first()
            sch_name = url.xpath('./td[1]/a/text()').extract_first()
            # sch_total = url.xpath('./td[3]/text()').extract_first()
            if sch_name in schools:
                yield Request(sch_url, callback=self.get_pages)

    def get_pages(self, response):
        print(response.url)
        sel = Selector(response)
        teacher_urls = sel.xpath('//*[@id="panelList"]/table/tr/td[2]/p/a/@href').extract()
        for url in teacher_urls:
            teacher_url = 'http://teacher.cucdc.com' + url
            yield Request(teacher_url, callback=self.parse_pages, dont_filter=True)

        tmp = sel.xpath('//*[@id="panelList"]/div[2]/a')
        for t in tmp:
            t_text = t.xpath('./text()').extract_first()
            if t_text == '下页':
                t_url = t.xpath('./@href').extract_first()
                next_page = 'http://teacher.cucdc.com' + t_url
        if next_page:
            yield Request(next_page, callback=self.get_pages)

    def parse_pages(self, response):
        info_url = response.url
        id = re.search('laoshi/(.*?).html',info_url).group(1)
        sel = Selector(response)
        name = sel.xpath('//*[@id="tmain"]/div[1]/div[1]/div[3]/span/text()').extract_first()
        uni = sel.xpath('//*[@id="tmain"]/div[1]/div[1]/div[3]/div/a[1]/text()').extract_first()
        dep = sel.xpath('//*[@id="tmain"]/div[1]/div[1]/div[3]/div/a[2]/text()').extract_first()
        cons = sel.xpath('//*[@id="tmain"]/div[1]/div[2]/div//text()').extract()
        # if not con:
        tmp = ''
        #     cons = sel.xpath('//*[@id="tmain"]/div[1]/div[2]/div/p/text()').extract()
        for c in cons:
            tmp += c
        con = ' '.join(tmp.split())

        tmp = sel.xpath('//*[@id="tmain"]/div[1]/div[1]/div[2]/img/@src').extract_first()
        if tmp != 'http://passport.cucdc.com/images/user/userdefaultpic.gif':
            img_url = tmp
        else:
            img_url = ''
        item = TeacherItem()
        item['id'] = id
        item['name'] = name
        item['uni'] = uni
        item['dep'] = dep
        item['pro'] = con
        item['img_url'] = img_url
        item['info_url'] = info_url
        yield item







