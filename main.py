# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/9/29 下午5:24

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'zhihu'])
execute(['scrapy', 'crawl', 'zhihu_sel'])
