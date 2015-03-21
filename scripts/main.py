#!/usr/bin/env python
# coding=utf-8

from memect.memect import Memect
import datetime

# 开始抓取前一天所有分类下的文章
try:
    memect_types = Memect.list_memect_type()
    for memect_type in memect_types:
        memect = Memect(memect_type.abbr)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        memect.grab_and_save(datetime.datetime.strftime(yesterday, '%Y-%m-%d'))
except Exception, ex:
    print str(ex)