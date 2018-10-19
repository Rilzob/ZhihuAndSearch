# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
import time


class ZhihuAndSearchSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    # 随机更换User-Agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent(verify_ssl=False)
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class JSPageMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.dropdown_num = settings.getint("DROPDOWN_NUM")
        # 从配置文件中导入全局变量DROPDOWN_NUM

    # 通过chrome请求动态网页
    def process_request(self, request, spider):
        spider.browser.get(request.url)
        time.sleep(1)
        print("访问:{0}".format(request.url))
        if request.url.startswith("https://www.zhihu.com/"):
            if request.url.startswith("https://www.zhihu.com/question/"):
                try:
                    spider.browser.find_element_by_css_selector("div.QuestionHeader-detail button.QuestionRichText-more").click()
                    # 将问题描述展开，当然问题描述可能没有或者不需要展开
                except:
                    print("不存在显示全部按钮")
            for i in range(self.dropdown_num):  # 下拉次数
                spider.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                                            "var lenOfPage=document.body.scrollHeight;"
                                            "return lenOfPage")  # 执行下拉操作刷新页面
                time.sleep(3)
        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)
