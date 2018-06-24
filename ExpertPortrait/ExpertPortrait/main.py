# /usr/bin/python
# -*- coding: utf-8 -*-
from scrapy import cmdline

# cmdline.execute("scrapy crawl test".split())
cmdline.execute("scrapy crawl test --nolog".split())
# cmdline.execute("scrapy crawl test -a start_urls=['http://www.irtree.cn/426/writer/100000000760910/rw_zp.aspx']".split())