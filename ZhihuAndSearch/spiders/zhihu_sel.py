# -*- coding: utf-8 -*-
import scrapy
import time


class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        pass

    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome(executable_path="/Users/rilzob/PycharmProjects/ZhihuAndSearch/chromedriver")
        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("15724428236")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("watermirrorsir")
        time.sleep(10)
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        Cookies = browser.get_cookies()
        print(Cookies)
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            # 写入文件
            f = open("/Users/rilzob/PycharmProjects/ZhihuAndSearch/cookies/zhihu" + cookie['name'] + '.zhihu')
            pickle.dump(cookie, f)
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

