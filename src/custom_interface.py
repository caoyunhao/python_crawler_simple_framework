# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 19:19
# @Author  : Yunhao Cao
# @File    : custom_interface.py
from src.simple_core import main, spider, task, storage, logger

__author__ = 'Yunhao Cao'

__all__ = [
    'CrawlerMain',
    'Spider',
    'Rule',
    'RequestTask',
    'Item',
    'Column',
    'Integer',
    'String',
    'DateTime',
    'storage',
    'logger',
]

CrawlerMain = main.CrawlerMain
Spider = spider.Spider
Rule = Spider.Rule
RequestTask = task.RequestTask
Item = storage.Item
Column = storage.Column
Integer = storage.Integer
String = storage.String
DateTime = storage.DateTime
logger = logger
