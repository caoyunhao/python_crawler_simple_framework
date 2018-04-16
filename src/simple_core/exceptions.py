# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/16 13:02
# @Author  : Yunhao Cao
# @File    : exceptions.py

__author__ = 'Yunhao Cao'

__all__ = [
    'CrawlerBaseException',
    'RuleManyMatchedError',
]


class CrawlerBaseException(Exception):
    pass


class RuleManyMatchedError(CrawlerBaseException):
    pass
