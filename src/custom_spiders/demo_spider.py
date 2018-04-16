# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:55
# @Author  : Yunhao Cao
# @File    : demo_spider.py
import datetime

from src.custom_interface import *

__author__ = 'Yunhao Cao'


class DemoItem(Item):
    __tablename__ = 'request_record'
    id = Column(Integer(), primary_key=True)
    ip = Column(String())
    create_time = Column(DateTime())


class DemoSpider(Spider):
    def __init__(self):
        super().__init__()
        self._db_config = 'mysql+mysqlconnector://root:123456@localhost:3306/demo'
        self._rule_list = [
            Rule(url=r"^(?:https?://)?ip.chinaz.com/getip.aspx$",
                 func=self.func,
                 dynamic=False,
                 use_proxy=False,
                 customized=False),
        ]

    def func(self, response, **kwargs):
        """
        解析函数
        """
        logger.info("Enter DemoSpider.func")

        logger.debug(response.text)

        logger.info("Parse successfully...")

        yield DemoItem(ip='192.168.1.1', create_time=datetime.datetime.now())

        yield RequestTask("http://ip.chinaz.com/getip.aspx")


if __name__ == '__main__':
    url = "http://ip.chinaz.com/getip.aspx"
    CrawlerMain.run(DemoSpider, [url, ])
