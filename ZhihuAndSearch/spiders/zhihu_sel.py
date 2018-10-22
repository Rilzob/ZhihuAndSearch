# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from pyvirtualdisplay import Display

from ZhihuAndSearch.items import ZhihuQuestionItem, ZhihuAnswerItem, ZhihuZhuanlanItem, ZhihuItemLoader
from ZhihuAndSearch.utils.common import get_md5

import re
import time


class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topic/19552832/top-answers']

    # User_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    User_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': User_agent}
    # # 由于无法翻墙所以无法访问fake_useragent的服务器，只能暂时使用自己的User-Agent

    def __init__(self):
        # display = Display(visible=0, size=(800, 600))  # chrome无界面运行
        # display.start()
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
        # print(all_urls)
        question_url = []
        zhuanlan_url = []
        for url in all_urls:
            if url.startswith(r'//'):
                url = 'https://' + url.strip(r'//')
                zhuanlan_url.append(url)
                yield scrapy.Request(url, headers=self.headers, dont_filter=True, callback=self.parse_zhuanlan)
                # yield scrapy.Request(url, dont_filter=True, callback=self.parse_zhuanlan)
            else:
                url_match = re.match("(/question/(\d+))(/|$).*", url)
                question_id = url_match.group(2)
                # print(question_id)
                url = 'https://www.zhihu.com/question/' + question_id
                question_url.append(url)
                yield scrapy.Request(url, headers=self.headers, meta={"question_id": question_id}, dont_filter=True,callback=self.parse_question)
                # yield scrapy.Request(url, meta={"question_id": question_id}, dont_filter=True, callback=self.parse_question)
                time.sleep(2)
        # print('zhuanlan_url:', len(zhuanlan_url))
        # print('zhuanlan_url', zhuanlan_url)
        # print('question_url: %d' % len(question_url))
        # print('question_url:', question_url)
        # time.sleep(3)

    def parse_zhuanlan(self, response):
        url_match = re.match("(.*com/p/(\d+))(/|$)", response.url)
        zhuanlan_id = int(url_match.group(2))
        zhuanlan_item_loader = ZhihuItemLoader(item=ZhihuZhuanlanItem(), response=response)
        zhuanlan_item_loader.add_value("zhuanlan_id", zhuanlan_id)
        zhuanlan_item_loader.add_value("zhuanlan_url", response.url)
        zhuanlan_item_loader.add_css("zhuanlan_title", "h1.Post-Title::text")
        zhuanlan_item_loader.add_css("praise_num", "span.Voters button::text")
        zhuanlan_item_loader.add_css("zhuanlan_article", "div.Post-RichText")
        # 得到的结果是一个list后面需要拼接成一整个string才能用remove_tags
        zhuanlan_item_loader.add_css("comments_num", "button.BottomActions-CommentBtn::text")
        zhuanlan_item_loader.add_value("zhuanlan_object_id", get_md5(response.url))

        zhuanlan_item = zhuanlan_item_loader.load_item()
        yield zhuanlan_item

    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item
        question_id = response.meta.get("question_id", "")
        question_item_loader = ZhihuItemLoader(item=ZhihuQuestionItem(), response=response)
        question_item_loader.add_css("question_title", "h1.QuestionHeader-title::text")
        question_item_loader.add_value("question_url", response.url)
        question_item_loader.add_css("question_descr", ".QuestionHeader-detail span::text")  # question_descr可能为空
        question_item_loader.add_value("question_id", int(question_id))
        question_item_loader.add_css("answer_num", ".List-headerText span::text")
        question_item_loader.add_css("followers", ".NumberBoard-itemValue::text")
        question_item_loader.add_css("visitors", ".NumberBoard-itemValue::text")
        question_item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
        question_item_loader.add_value("question_object_id", get_md5(response.url))
        answer_id_list = response.css("div.ContentItem::attr(name)").extract()
        question_item_loader.add_value("answer_id_list", answer_id_list)
        answer_url_list = []
        for answer_id in answer_id_list:
            answer_url = 'https://www.zhihu.com/question/' + question_id + '/answer/' + answer_id
            answer_url_list.append(answer_url)
        question_item_loader.add_value("answer_url_list", answer_url_list)

        question_item = question_item_loader.load_item()
        yield question_item
        for answer_url in answer_url_list:
            yield scrapy.Request(answer_url, headers=self.headers, dont_filter=True, callback=self.parse_answer)
            # yield scrapy.Request(answer_url, dont_filter=True, callback=self.parse_answer)
            time.sleep(1)

    def parse_answer(self, response):
        # 处理answer页面，从页面中提取出具体的answer item
        url_match = re.match("(.*/answer/(\d+))(/|$)", response.url)
        answer_id = int(url_match.group(2))
        answer_item_loader = ZhihuItemLoader(item=ZhihuAnswerItem(), response=response)
        answer_item_loader.add_value("answer_url", response.url)
        answer_item_loader.add_value("answer_id", answer_id)
        answer_item_loader.add_css("comments_num", "div.ContentItem meta[itemprop*=commentCount]::attr(content)")
        answer_item_loader.add_css("answer_article", "div.RichContent-inner span.RichText")
        answer_item_loader.add_css("praise_num", "div.ContentItem meta[itemprop*=upvoteCount]::attr(content)")
        answer_item_loader.add_value("answer_object_id", get_md5(response.url))

        answer_item = answer_item_loader.load_item()
        yield answer_item

    def start_requests(self):
        # return [scrapy.Request('https://www.zhihu.com/topic/19552832/top-answers',
        #                        dont_filter=True, callback=self.parse)]
        return [scrapy.Request('https://www.zhihu.com/topic/19552832/top-answers', headers=self.headers,
                                dont_filter=True, callback=self.parse)]
