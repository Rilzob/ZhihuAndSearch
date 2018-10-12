# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import time
import re


class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topic/19552832/top-answers']

    custom_settings = {
        "COOKIE_ENABLED": True,
        "DOWNLOAD_DELAY": 1.5
    }

    User_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    headers = {'User-Agent': User_agent}
    # 由于无法翻墙所以无法访问fake_useragent的服务器，只能暂时使用自己的User-Agent

    def __init__(self):
        self.browser = webdriver.Chrome(
            executable_path="/Users/rilzob/PycharmProjects/ZhihuAndSearch/chromedriver")
        super(ZhihuSelSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print("spider closed")
        spider.browser.quit()

    def parse(self, response):
        print("进入parse函数")
        all_urls = response.css("div.ContentItem h2 a::attr(href)").extract()
        print(all_urls)
        question_url = []
        zhuanlan_url = []
        for url in all_urls:
            if url.startswith(r'//'):
                url = url.strip(r'//')
                zhuanlan_url.append(url)
            else:
                url_match = re.match("(/question/(\d+))(/|$).*", url)
                url = 'www.zhihu.com' + url_match.group()
                question_url.append(url)
        print('zhuanlan_url:', len(zhuanlan_url))
        print('zhuanlan_url', zhuanlan_url)
        print('question_url: %d' % len(question_url))
        print('question_url:', question_url)
        time.sleep(3)

    def start_requests(self):
        # return [scrapy.Request('https://www.zhihu.com/topic/19552832/top-answers', dont_filter=True,)]
        return [scrapy.Request('https://www.zhihu.com/topic/19552832/top-answers', headers=self.headers, dont_filter=True,)]
