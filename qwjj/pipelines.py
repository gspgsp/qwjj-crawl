# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sqlutil import SqlUtil
from qwjj.items import ArticleItem

class QwjjPipeline(object):
    def process_item(self, item, spider):
        sqlutil = SqlUtil()
        # 平台资讯/公告
        if isinstance(item, ArticleItem):
            sqlutil.insert_data('fanwe_article', item)
        return item
