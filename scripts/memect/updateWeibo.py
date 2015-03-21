#!/usr/bin/env python
# coding=utf-8

import MySQLdb
from utils.weibo import Client
import config
import json
import re


class UpdateWeibo(object):
    con = MySQLdb.connect(user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD,
                          host=config.MYSQL_HOST, db=config.MYSQL_DB, charset=config.MYSQL_CHARSET)
    cursor = con.cursor()

    def __init__(self):
        # 初始化微博客户端
        self.weibo_client = Client(config.WEIBO_APPKEY, config.WEIBO_SECRET, config.WEIBO_REDIRECT_URL,
                                  username=config.WEIBO_USER, password=config.WEIBO_PASSWORD)

    def update_wb(self):
        query_sql = 'select weibo_id from memect_thread where weibo_content is null limit 0,2000'
        UpdateWeibo.cursor.execute(query_sql)
        for (weibo_id,) in UpdateWeibo.cursor.fetchall():
            try:
                print weibo_id
                weibo_content = json.dumps(self.weibo_client.get('statuses/show', id=weibo_id), ensure_ascii=False)
                print weibo_content
                insert_memect_content = 'update memect_thread set weibo_content = \'%s\' where weibo_id = %d' % \
                                        (weibo_content.replace('\'', '\\\''), weibo_id)
                UpdateWeibo.cursor.execute(insert_memect_content)
                UpdateWeibo.con.commit()
            except Exception, ex:
                print str(ex)

if __name__ == '__main__':
    wb = UpdateWeibo()
    wb.update_wb()