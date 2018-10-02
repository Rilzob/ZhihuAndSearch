# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topic/19552832/top-answers']

    def parse(self, response):
        print("进入parse函数")
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/topic/19552832/top-answers', dont_filter=True,
                                 callback=self.parse)]

    def check_login(self, response):
        print("进入login函数")
        pass