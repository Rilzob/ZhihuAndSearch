# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity, Compose
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ZhihuAndSearch.models.es_type import ZhihuQuestionType, ZhihuAnswerType, ZhihuZhuanlanType
from ZhihuAndSearch.utils.common import extract_num, return_followers_num, return_visitors_num


class ZhihuAndSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题Item
    question_id = scrapy.Field()
    question_url = scrapy.Field()
    question_title = scrapy.Field()
    question_descr = scrapy.Field()
    question_object_id = scrapy.Field()
    answer_num = scrapy.Field(
        input_processor=MapCompose(extract_num),
    )
    followers = scrapy.Field(
        input_processor=Compose(return_followers_num, extract_num)
    )
    visitors = scrapy.Field(
        input_processor=Compose(return_visitors_num, extract_num)
    )
    topics = scrapy.Field(
        input_processor=Join(",")
    )
    answer_id_list = scrapy.Field(
        input_processor=Join(",")
    )
    answer_url_list = scrapy.Field(
        input_processor=Join(",")
    )

    def save_to_es(self):
        question = ZhihuQuestionType()
        question.question_id = self['question_id']
        question.question_url = self['question_url']
        question.question_title = self['question_title']
        question.question_descr = self['question_descr']
        question.question_object_id = self['question_object_id']
        question.answer_num = self['answer_num']
        question.followers = self['followers']
        question.visitors = self['visitors']
        question.topics = self['topics']
        question.answer_id_list = self['answer_id_list']
        question.answer_url_list = self['answer_url_list']

        question.save()

        return

    def get_insert_sql(self):
        # 插入zhihu_question表的sql语句
        insert_sql = '''
            insert into zhihu_question(question_id, question_url, question_title, question_descr,
            answer_num, followers, visitors, topics, answer_id_list, answer_url_list, question_object_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        params = (self['question_id'], self['question_url'], self['question_title'], self['question_descr'],
                  self['answer_num'], self['followers'], self['visitors'], self['topics'], self['answer_id_list'],
                  self['answer_url_list'], self['question_object_id'])

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎的回答Item
    answer_id = scrapy.Field()
    comments_num = scrapy.Field(
        input_processor=MapCompose(int)
    )
    answer_article = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    praise_num = scrapy.Field(
        input_processor=MapCompose(int)
    )
    answer_url = scrapy.Field()
    answer_object_id = scrapy.Field()

    def save_to_es(self):
        answer = ZhihuAnswerType()
        answer.id = self['answer_id']
        answer.comments_num = self['comments_num']
        answer.answer_article = self['answer_article']
        answer.praise_num = self['praise_num']
        answer.answer_url = self['answer_url']
        answer.answer_object_id = self['answer_object_id']

        answer.save()

        return

    def get_insert_sql(self):
        # 插入zhihu_answer表的sql语句
        insert_sql = '''
            insert into zhihu_answer(answer_id, comments_num, answer_article, praise_num, answer_url, answer_object_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        comments_num = int(self['comments_num'])
        praise_num = int(self['praise_num'])

        params = (self['answer_id'], comments_num, self['answer_article'],
                  praise_num, self['answer_url'], self['answer_object_id'])

        return insert_sql, params


class ZhihuZhuanlanItem(scrapy.Item):
    # 知乎的专栏Item
    zhuanlan_id = scrapy.Field()
    zhuanlan_title = scrapy.Field()
    praise_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    zhuanlan_article = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    comments_num = scrapy.Field(
        input_processor=MapCompose(extract_num),
    )
    zhuanlan_url = scrapy.Field()
    zhuanlan_object_id = scrapy.Field()

    def save_to_es(self):
        zhuanlan = ZhihuZhuanlanType()
        zhuanlan.zhuanlan_id = self['zhuanlan_id']
        zhuanlan.zhuanlan_title = self['zhuanlan_title']
        zhuanlan.praise_num = self['praise_num']
        zhuanlan.zhuanlan_article = self['zhuanlan_article']
        zhuanlan.comments_num = self['comments_num']
        zhuanlan.zhuanlan_url = self['zhuanlan_url']
        zhuanlan.zhuanlan_object_id = self['zhuanlan_object_id']

        zhuanlan.save()

        return

    def get_insert_sql(self):
        # 插入zhihu_zhuanlan表的sql语句
        insert_sql = '''
            insert into zhihu_zhuanlan(zhuanlan_id, zhuanlan_title, praise_num, 
            zhuanlan_article, comments_num, zhuanlan_url, zhuanlan_object_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        params = (self['zhuanlan_id'], self['zhuanlan_title'], self['praise_num'],
                  self['zhuanlan_article'], self['comments_num'], self['zhuanlan_url'],
                  self['zhuanlan_object_id'])

        return insert_sql, params
