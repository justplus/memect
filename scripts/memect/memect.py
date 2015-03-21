#!/usr/bin/env python
# coding=utf-8

import requests
import MySQLdb
from models.MemectType import MemectType
from bs4 import BeautifulSoup, Tag
from utils.weibo import Client
import config
import json
import datetime
import time


class Memect(object):
    con = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD,
                          host=config.MYSQL_HOST, db=config.MYSQL_DB, charset=config.MYSQL_CHARSET)
    cursor = con.cursor()

    def __init__(self, memect_type_abbr):
        """构造函数
        :param memect_type_abbr: abbr, 如需要抓取机器学习日报，填ml, 具体参照memect_type
        """
        self.memect_type_abbr = memect_type_abbr
        # 初始化微博客户端
        self.weibo_client = Client(config.WEIBO_APPKEY, config.WEIBO_SECRET, config.WEIBO_REDIRECT_URL,
                                   username=config.WEIBO_USER, password=config.WEIBO_PASSWORD)
        # 初始化memect_type
        self.__get_memect_type()

    def grab_all_from_start(self):
        today = datetime.date.today()
        start = datetime.datetime.strptime(self.memect_type.start_date, '%Y-%m-%d').date()
        date_delta = today - start
        for delta in range(date_delta.days):
            next_day = start + datetime.timedelta(days=delta)
            self.grab_and_save(datetime.datetime.strftime(next_day, '%Y-%m-%d'))
            # maybe wait for 1 second is a good choice
            time.sleep(1)



    def grab_and_save(self, archive_date):
        """抓取某一天的页面内容并保存到数据库
        抓取的内容包括所有的标签、所有的内容以及对应的标签
        :param archive_date: 日报对应的日期，格式为:%Y-%m-%d
        """
        print '%s: %s' % (self.memect_type_abbr, archive_date)
        url = '%s/archive/%s/long.html' % (self.memect_type.url, archive_date)
        try:
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

                # find all available threads and insert into database
                headline_threads = set(bs.find_all('div', class_='today')) & set(bs.find_all('div', class_='headline'))
                for thread_tag in headline_threads:
                    weibo_id = int(thread_tag['id'])
                    thread_id = self.__set_memect_content(weibo_id, 0, archive_date)
                    if thread_id:
                        self.__set_memect_thread_tag(thread_id, thread_tag)
                    print weibo_id, thread_id
                trend_thread = set(bs.find_all('div', class_='today')) - set(bs.find_all('div', class_='headline'))
                for thread_tag in trend_thread:
                    weibo_id = int(thread_tag['id'])
                    thread_id = self.__set_memect_content(weibo_id, 1, archive_date)
                    if thread_id:
                        self.__set_memect_thread_tag(thread_id, thread_tag)
                    print weibo_id, thread_id
        except Exception, ex:
            print "request error: " + str(ex)



    def __get_memect_type(self):
        """根据类型缩写获取memect_type model
        """
        query_memect_type = 'select * from memect_type where abbr = "%s"' % self.memect_type_abbr
        Memect.cursor.execute(query_memect_type)
        (type_id, type_name, type_abbr, type_url, start_date) = Memect.cursor.fetchone()
        self.memect_type = MemectType(type_id, type_name, type_abbr, type_url, start_date)

    def __set_memect_content(self, weibo_id, category, archive_date):
        """根据id获取微博内容并插入到数据库
        :param category: 0-焦点 1-动态
        :return 返回插入到数据库中thread编号，如果微博不存在了，返回None
        """
        try:
            weibo_content = json.dumps(self.weibo_client.get('statuses/show', id=weibo_id), ensure_ascii=False)
            insert_memect_content = 'insert into memect_thread(weibo_id, weibo_content, memect_type,' \
                                    ' create_time, memect_category) values (%d, \'%s\', %d, \'%s\', %d)' % \
                                    (weibo_id, weibo_content.replace('\'', '\\\''), self.memect_type.id, archive_date, category)
            Memect.cursor.execute(insert_memect_content)
            thread_id = Memect.con.insert_id()
            Memect.con.commit()
            return thread_id
        except RuntimeError, ex:
            print "weibo error:" + str(ex)
            return None

    def __set_memect_thread_tag(self, thread_id, tag):
        """获取thread对应的标签(memect_tag)并插入到数据库
        """
        for child in tag.find_all('span', class_='keyword'):
            tag_name = child.string
            insert_thread_tag = 'insert into memect_thread_tag(thread_id, tag_name) values(%d, \'%s\')' % \
                                (thread_id, tag_name)
            Memect.cursor.execute(insert_thread_tag)
            Memect.con.commit()

    @classmethod
    def list_memect_type(cls):
        """获取所有的memect_type
        """
        query_memect_type = 'select * from memect_type'
        Memect.cursor.execute(query_memect_type)
        memect_types = []
        for (type_id, type_name, type_abbr, type_url, start_date) in Memect.cursor.fetchall():
            memect_types.append(MemectType(type_id, type_name, type_abbr, type_url, start_date))
        return memect_types


if __name__ == '__main__':
    # 开始抓取所有分类下的文章
    try:
        memect_types = Memect.list_memect_type()
        for memect_type in memect_types:
            memect = Memect(memect_type.abbr)
            memect.grab_all_from_start()
    except Exception, ex:
        print "main error: " + str(ex)