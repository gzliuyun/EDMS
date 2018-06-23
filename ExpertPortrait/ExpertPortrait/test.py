import urllib.request
from lxml import etree

urlset = []

class XueshuSpider:
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def __init__(self, url):
        self.url = url
        self.request = urllib.request.Request(self.url, headers=self.headers)
        self.response = urllib.request.urlopen(self.request)
        # print(self.response.getcode()) # 获取HTTP状态码
        self.wb_data = self.response.read()
        self.html = etree.HTML(self.wb_data)
        self.result = etree.tostring(self.html)
        self.checkkey = self.result.decode("utf-8")[6] #ckkey为'&'时，该url不存在；为'l'时存在
        # print("###"+self.checkkey+"###")

    def getcheckkey(self): # 检查url合法性
        return self.checkkey

    def getname(self): # 获取专家姓名
        self.name = self.html.xpath('//*[@class="p_name"]/text()')[0]
        return self.name

    def getscholarid(self): # 获取专家的scholarID
        self.sid = self.html.xpath('//*[@class="p_scholarID_id"]/text()')[0]
        return self.sid

    def getimgurl(self):
        self.imgurl = self.html.xpath('//*[@id="author_intro_wr"]//img/@src')
        if self.imgurl == "/lib/static/scholar/cache/homepage/img/default_a139b75.png":
            self.imgurl = ""
        return self.imgurl

    # def get


def deal(url):
    sp = XueshuSpider(url)

    if sp.checkkey == 'l':
        urlset.append(url)
        print(url)

if __name__ == "__main__":


    """ TEST """
    testurl = "http://xueshu.baidu.com/scholarID/CN-BP74MGXJ"
    deal(testurl)



    # ScholarID规律：
    # 前4位必为'CN-B'，
    # 第5位为大写英文字母，
    # 第6位为数字'7'，
    # 第7位为数字，
    # 第8、9、10位为数字或大写字母，
    # 第11位为大写字母'J'

    # letter_list = "QWERTYUIOPASDFGHJKLZXCVBNM"
    # digit_list = "1234567890"
    # merge_list = letter_list + digit_list
    #
    # head = "http://xueshu.baidu.com/scholarID/CN-B"
    #
    # for letter5 in letter_list:
    #     for digit7 in digit_list:
    #         for ch8 in merge_list:
    #             for ch9 in merge_list:
    #                 for ch10 in merge_list:
    #                     url = head + letter5 + '7' + digit7 + ch8 + ch9 + ch10 + 'J'
    #                     deal(url)
    #
    # with open('allurl.txt', 'w') as f:
    #     for url in urlset:
    #         f.write(url)
    #         f.write('\n')
    # f.close()

