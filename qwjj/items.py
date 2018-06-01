# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.qwjj.org/en/latest/topics/items.html

import scrapy


# 平台新闻资讯
class ArticleItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 分类id
    cate_id = scrapy.Field()
    # 平台id
    plat_id = scrapy.Field()
    # 摘要
    brief = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 发布时间
    create_time = scrapy.Field()
