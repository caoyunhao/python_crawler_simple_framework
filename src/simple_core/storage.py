# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 19:37
# @Author  : Yunhao Cao
# @File    : storage.py
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

    def save(self, item):
        self.session.add(item)
        self.session.commit()
