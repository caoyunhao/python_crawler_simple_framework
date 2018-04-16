# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:47
# @Author  : Yunhao Cao
# @File    : proxy.py

__author__ = 'Yunhao Cao'

__all__ = [
    'ProxyManager',
]


class ProxyManager(object):
    def get_next(self):
        return Proxy()


class Proxy(object):
    def __init__(self):
        self.ip = None

    @property
    def valid(self):
        return self.ip
