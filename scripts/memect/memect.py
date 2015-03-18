#!/usr/bin/env python
# coding=utf-8

import requests
import MySQLdb
from models.MemectType import MemectType
from bs4 import BeautifulSoup


class Memect(object):
    con = MySQLdb.connect(user='root', passwd='root', host='localhost', db='memect', charset='utf8')
    cursor = con.cursor()

    def __init__(self, memect_type_abbr, archive_date):
        self.memect_type_abbr = memect_type_abbr
        self.archive_date = archive_date

    def grab_and_save(self):
        """抓取页面内容并保存到数据库
        抓取的内容包括所有的标签、所有的内容以及对应的标签
        """
        self.__get_memect_type()
        url = '%s/archive/%s/long.html' % (self.memect_type.url, self.archive_date)
        r = requests.get(url)
        r.encoding = 'utf-8'    # don't forget this
        content = r.text
        bs = BeautifulSoup(content)
        # find all available tags and insert into database
        tags = bs.find_all('span', class_='keyword')
        tag_list = set([tag.string for tag in tags if tag.string != u'全部'])
        # find all available threads
        headline_threads = set(bs.find_all('div', class_='today')) & set(bs.find_all('div', class_='headline'))
        print len(headline_threads)
        trend_thread = set(bs.find_all('div', class_='today')) - set(bs.find_all('div', class_='headline'))
        print len(trend_thread)


    def __get_memect_type(self):
        """根据类型缩写获取memect_type model
        """
        query_memect_type = 'select * from memect_type where abbr = "%s"' % self.memect_type_abbr
        Memect.cursor.execute(query_memect_type)
        (type_id, type_name, type_abbr, type_url) = Memect.cursor.fetchone()
        self.memect_type = MemectType(type_id, type_name, type_abbr, type_url)


if __name__ == '__main__':
    m = Memect('py', '2015-03-14')
    m.grab_and_save()