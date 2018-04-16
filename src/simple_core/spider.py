# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:51
# @Author  : Yunhao Cao
# @File    : spider.py
import re
import types

from .exceptions import RuleManyMatchedError
from .storage import Storage
from . import logger

__author__ = 'Yunhao Cao'

__all__ = [
    'Spider',
]


class Spider(object):
    class Rule(object):
        def __init__(self, url, func, dynamic=False, use_proxy=False, customized=False):
            self.url = re.compile(url)
            self.func = func
            self.dynamic = dynamic
            self.use_proxy = use_proxy
            self.customized = customized

    def __init__(self):
        self._rule_list = []
        self._db_config = None
        self._storage = None

    def save(self, item):
        if self._storage is None:
            self._storage = Storage(self._db_config)
        self._storage.save(item)

    def parse(self, response, **kwargs):
        """
        根据对应的解析规则解析页面
        :param response: Response
        :param kwargs: 其他参数
        :return:
        """
        logger.info("Enter Spider.parse")
        current_url = response.url

        _rule = self._match_rule(current_url)

        if _rule is None:
            logger.info(u"Wrong url: {}; task url: {}".format(current_url, getattr(kwargs.get("task"), "url", None)))
            return

        func = _rule.func

        if isinstance(func, (staticmethod, types.FunctionType, types.LambdaType)):
            if isinstance(func, (staticmethod,)):
                func = func.__func__
            return func(response, **kwargs)
        elif isinstance(func, (classmethod, types.MethodType)):
            return func.__func__(self, response, **kwargs)
        else:
            raise Exception("`func` must be a method or function.")

    def get_rule(self, url):
        return self._match_rule(url)

    def _match_rule(self, url):
        """
        检测是否只有一个规则与之匹配
        :param url:
        :return: rule 规则
        """
        match_count = 0

        _rule = None
        for rule in self._rule_list:
            if re.match(rule.url, url):
                _rule = rule
                match_count += 1

        if match_count < 1:
            logger.info(u"Unknown url ({})".format(url))
        elif match_count > 1:
            raise RuleManyMatchedError("Matched rules more than 1.")

        return _rule
