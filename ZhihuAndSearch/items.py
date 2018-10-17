# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from ZhihuAndSearch.models.es_type import ZhihuQuestionType, ZhihuAnswerType, ZhihuZhuanlanType


class ZhihuAndSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题Item
    question_id = scrapy.Field()
    question_url = scrapy.Field()
    question_title = scrapy.Field()
    question_descr = scrapy.Field()
    answer_num = scrapy.Field()
    followers = scrapy.Field()
    visitors = scrapy.Field()
    topics = scrapy.Field()
    answer_id_list = scrapy.Field()
    answer_url_list = scrapy.Field()

    def save_to_es(self):
        question = ZhihuQuestionType()
        question.question_id = self['question_id']
        question.question_url = self['question_url']
        question.question_title = self['question_title']
        question.question_descr = self['question_descr']
        question.answer_num = self['answer_num']
        question.followers = self['followers']
        question.visitors = self['visitors']
        question.topics = self['topics']
        question.answer_id_list = self['answer_id_list']
        question.answer_url_list = self['answer_url_list']

        question.save()

        return


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的回答Item
    answer_id = scrapy.Field()
    comments_num = scrapy.Field()
    answer_article = scrapy.Field()
    praise_num = scrapy.Field()
    answer_url = scrapy.Field()

    def save_to_es(self):
        answer = ZhihuAnswerType()
        answer.id = self['answer_id']
        answer.comments_num = self['comments_num']
        answer.answer_article = self['answer_article']
        answer.praise_num = self['praise_num']
        answer.answer_url = self['answer_url']

        answer.save()

        return


class ZhihuZhuanlanItem(scrapy.Item):
    # 知乎的专栏Item
    zhuanlan_id = scrapy.Field()
    zhuanlan_title = scrapy.Field()
    praise_num = scrapy.Field()
    zhuanlan_article = scrapy.Field()
    comments_num = scrapy.Field()
    zhuanlan_url = scrapy.Field()

    def save_to_es(self):
        zhuanlan = ZhihuZhuanlanType()
        zhuanlan.zhuanlan_id = self['zhuanlan_id']
        zhuanlan.zhuanlan_title = self['zhuanlan_title']
        zhuanlan.praise_num = self['praise_num']
        zhuanlan.zhuanlan_article = self['zhuanlan_article']
        zhuanlan.comments_num = self['comments_num']
        zhuanlan.zhuanlan_url = self['zhuanlan_url']

        zhuanlan.save()

        return
