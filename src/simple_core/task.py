# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/1 14:40
# @Author  : Yunhao Cao
# @File    : task.py

__author__ = 'Yunhao Cao'

__all__ = [
    'RequestTask', 'Task'
]


class Task(object):
    pass


class RequestTask(Task):
    def __init__(self, url, fail_time=0, **params):
        self.url = url
        self.fail_time = fail_time
        self.params = params
