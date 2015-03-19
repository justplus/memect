#!/usr/bin/env python
# coding=utf-8

import requests
import MySQLdb
from models.MemectType import MemectType
from bs4 import BeautifulSoup
from utils.weibo import Client
import config
import time


class Memect(object):
    con = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD,
                          host=config.MYSQL_HOST, db=config.MYSQL_DB, charset=config.MYSQL_CHARSET)
    cursor = con.cursor()

    def __init__(self, memect_type_abbr, archive_date):
        self.memect_type_abbr = memect_type_abbr
        self.archive_date = archive_date
        # 初始化微博客户端
        self.weibo_client = Client(config.WEIBO_APPKEY, config.WEIBO_SECRET, config.WEIBO_REDIRECT_URL,
                                   username=config.WEIBO_USER, passwrod=config.WEIBO_PASSWORD)

    def grab_and_save(self):
        """抓取页面内容并保存到数据库
        抓取的内容包括所有的标签、所有的内容以及对应的标签
        """
        self.__get_memect_type()
        url = '%s/archive/%s/long.html' % (self.memect_type.url, self.archive_date)
        r = requests.get(url)
        r.encoding = 'utf-8'    # don't forget this
        if r.status_code == 200:
            content = r.text
            bs = BeautifulSoup(content)

            # find all available tags and insert into database
            tags = bs.find_all('span', class_='keyword')
            tag_list = set([tag.string for tag in tags if tag.string != u'全部'])
            for tag_name in tag_list:
                insert_memect_tag = 'insert into memect_tag(tag_name) values (\'%s\') on duplicate key UPDATE ' \
                                     'tag_name = \'%s\'' % (tag_name, tag_name)
                Memect.cursor.execute(insert_memect_tag)
                Memect.con.commit()

            # find all available threads
            headline_threads = set(bs.find_all('div', class_='today')) & set(bs.find_all('div', class_='headline'))
            for thread_tag in headline_threads:
                weibo_id = thread_tag['id']
                self.__set_memect_content(weibo_id, 0)
            trend_thread = set(bs.find_all('div', class_='today')) - set(bs.find_all('div', class_='headline'))
            for thread_tag in trend_thread:
                weibo_id = thread_tag['id']
                self.__set_memect_content(weibo_id, 0)

    def __get_memect_type(self):
        """根据类型缩写获取memect_type model
        """
        query_memect_type = 'select * from memect_type where abbr = "%s"' % self.memect_type_abbr
        Memect.cursor.execute(query_memect_type)
        (type_id, type_name, type_abbr, type_url) = Memect.cursor.fetchone()
        self.memect_type = MemectType(type_id, type_name, type_abbr, type_url)

    def __set_memect_content(self, weibo_id, category):
        """根据id获取微博内容并插入到数据库
        :category 0-焦点 1-动态
        """
        weibo_content = self.weibo_client.get('statuses/show', id=weibo_id)
        insert_memect_content = 'insert into memect_content(weibo_id, weibo_content, memect_type,' \
                                ' create_time, memect_category) values (%d, \'%s\', %d, \'%s\', %d)' % \
                                (weibo_id, weibo_content, self.memect_type.id,
                                 time.strftime('%Y-%m-%d', time.localtime(time.time())), category)
        Memect.cursor.execute(insert_memect_content)
        Memect.con.commit()

    def __set_memect_type(self):
        """获取thread对应的标签(memect_type)
        """
        pass

if __name__ == '__main__':
    m = Memect('py', '2015-03-14')
    m.grab_and_save()