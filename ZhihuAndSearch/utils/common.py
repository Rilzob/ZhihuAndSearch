# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/10/17 下午5:53

import re
import hashlib


def extract_num(text):
    # 从字符串中提取出数字
    text = text.replace(',', '')  # 有的数字中存在',' ，所以需要先去掉,才能使用正则表达式
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1).replace(',', ''))
    else:
        nums = 0

    return nums


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def return_followers_num(value):
    # print("value:", value)
    # print("value[0]:", value[0])
    return value[0]


def return_visitors_num(value):
    # print("value:", value)
    # print("value[1]", value[1])
    return value[1]
