#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import time
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from qwjj.items import ArticleItem

class ArticleSpider(scrapy.Spider):
    name = 'article'

    allowed_domains = ['wdzj.com']
    base_domain = 'https://www.wdzj.com'
    shuju_domain = 'https://shuju.wdzj.com'
    bash_url = base_domain + '/dangan/search?filter=e1'


    def start_requests(self):
        yield Request(self.bash_url, self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pageList').find_all('a')[-1].attrs['currentnum']
        bashurl = str(response.url)
        for num in range(1, int(max_num) + 1):
            url = bashurl + '&currentPage=' + str(num)
            yield Request(url, callback=self.get_list)

    # 获取列表页数据
    def get_list(self, response):
        lis = BeautifulSoup(response.text, 'lxml').find('ul', class_='terraceList').find_all('li', class_='item')
        for li in lis:
            infourl = self.base_domain + li.find('a', class_='look').attrs['href']
            tag = li.find_all('div', class_="itemTitleTag")
            if len(tag) > 0:
                ul = tag[0].find('ul')
                if ul:
                    start = 1
                    hot_solution = ',1'
                else:
                    start = 0
                    hot_solution = ''
                divs = li.find_all('div', class_="itemTitleTag")
                for index in range(len(divs)):
                    if index > start:
                        text = self.self_strip(divs[index].find('em').get_text())
                        hot_solution = hot_solution + self.deal_hot_solution(text)
            else:
                hot_solution = ''
            #print(lis)
            yield Request(infourl, callback=self.get_info, meta={'hot_solution': hot_solution})

    # 处理热门方案字段
    def deal_hot_solution(self, arg):
        # 1-评级百强 2-银行存管 3-加入协会 4-ICP认证 5-之家考察 6-融资平台
        switcher = {
            "评级百强": ",1",
            "银行存管": ",2",
            "加入协会": ",3",
            "融资平台": ",4",
            "ICP认证": ",5",
            "之家考察": ",6",
        }
        return switcher.get(arg.encode('utf-8'), "")

    # 获取详情页数据
    def get_info(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        plat_id = soup.find(id="platId").attrs['value']

        # 平台资讯
        newsurl = response.url + 'zixun/'
        #print(newsurl)
        yield Request(newsurl, callback=self.get_news, meta={'plat_id': plat_id})

    # 获取平台资讯
    def get_news(self, response):
        cate_id = 5
        plat_id = response.meta['plat_id']
        zllist = BeautifulSoup(response.text, 'lxml').find('ul', class_='zllist')
        if zllist:
            lis = zllist.find_all('li')
            for li in lis:
                infourl = 'https:' + li.find('h3').find('a').attrs['href']
                #print(infourl)
                yield Request(infourl, callback=self.get_news_info, meta={'cate_id': cate_id, 'plat_id': plat_id})

    # 获取资讯详情页
    def get_news_info(self, response):
        item = ArticleItem()
        soup = BeautifulSoup(response.text, 'lxml')
        item['title'] = self.self_strip(soup.find('div', class_='show-box').find('h1', class_='s-title').get_text())
        cate_id = response.meta['cate_id']
        item['cate_id'] = cate_id
        item['plat_id'] = response.meta['plat_id']
        create_time = self.self_strip(soup.find('div', class_='show-box').find('div', class_='s-bq').find('span').get_text())

        if cate_id == 5:
            fstr = '%Y-%m-%d %H:%M:%S'
        elif cate_id == 6:
            fstr = '%Y-%m-%d'
        item['create_time'] = time.mktime(time.strptime(create_time, fstr))
        zy = soup.find('div', class_='show-box').find('div', class_='s-zy')
        if zy:
            item['brief'] = self.self_strip(zy.find('span').get_text())
        content = soup.find('div', class_='show-box').find('div', class_='c-cen').prettify().replace('网贷之家', '网金之家')
        content = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", content)

        item['content'] = content

        yield item

    # 自定义字符串去除空格函数
    def self_strip(self, str):
        str = str.strip()
        if str == '-':
            str = ''
        return str
