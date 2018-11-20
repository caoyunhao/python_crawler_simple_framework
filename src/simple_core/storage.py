# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 19:37
# @Author  : Yunhao Cao
# @File    : storage.py
from threading import Lock

from sqlalchemy import Column, Integer, String, DateTime, orm, create_engine
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Yunhao Cao'

__all__ = [
    'Item',
    'Column',
    'Integer',
    'String',
    'DateTime',
    'Storage',
]

# 创建数据库实体的基类:
Item = declarative_base()


class Storage(object):
    def __init__(self, config):
        engine = create_engine(config)
        self.session = orm.sessionmaker(bind=engine)()
        self.lock = Lock()

    def save_with_lock(self, item):
        self.with_lock(self.save, item)

    def save_all_with_lock(self, items):
        self.with_lock(self.save_all, items)

    def save(self, item):
        self.session.add(item)
        self.session.commit()

    def save_all(self, items):
        self.session.add_all(items)
        self.session.commit()

    def with_lock(self, func, *args, **kwargs):
        self.lock.acquire()
        try:
            func(*args, **kwargs)
        finally:
            self.lock.release()
