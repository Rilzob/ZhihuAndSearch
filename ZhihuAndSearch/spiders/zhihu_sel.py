# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topic/19552832/top-answers']

    custom_settings = {
        "COOKIE_ENABLED": True,
        "DOWNLOAD_DELAY": 1.5
    }

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
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/topic/19552832/top-answers', dont_filter=True,)]
