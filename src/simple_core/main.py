# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:51
# @Author  : Yunhao Cao
# @File    : main.py
import traceback
import time
from functools import partial

from .downloader import DownloaderFactory
from .scheduler import Scheduler
from .cqueue import WebRequestQueue
from .storage import Item
from .task import RequestTask
from . import logger

__author__ = 'Yunhao Cao'

__all__ = [
    'CrawlerMain'
]


def work(task, spider, task_queue, **config):
    url = task.url

    # 检测url的合法性, 根据自定义规则匹配, 返回定义规则,
    rule = spider.get_rule(url)
    if rule is None:
        return

    # 解析函数
    _parse_func = partial(spider.parse, current_task=task, task_queue=task_queue, params=task.params)

    success = True
    response = None

    _downloader_factory = DownloaderFactory()

    _downloader = _downloader_factory.creator()

    try:
        response = _downloader.get(url)
    except Exception as e:
        success = False
        logger.info("[sub thread] Exception = {}".format(e))
        task.fail_time += 1
        if task.fail_time < 3:
            task_queue.put(task)
        else:
            logger.info("Failure more than 3 times. ({})".format(url))

    if success and response:
        parse_results_generator = _parse_func(response)

        def handle_result(r):
            try:
                if isinstance(r, RequestTask):
                    task_queue.put(r)
                elif isinstance(r, Item):
                    spider.save(r)
            except Exception:
                logger.error(traceback.format_exc())

        if parse_results_generator:
            for parse_result in parse_results_generator:
                handle_result(parse_result)

    sleep_time = config.get("sleep_time", 5)
    logger.info("Wait {} seconds...".format(sleep_time))
    time.sleep(sleep_time)


class CrawlerMain(object):
    @staticmethod
    def run(spider, requests, **config):
        """
        主函数
        :return:
        """
        # 请求队列初始化
        logger.debug("config: {}".format(config))

        queue = WebRequestQueue()
        queue.put(requests)

        scheduler = Scheduler(config.get("worker", 1))

        spider = spider()
        partial_work_func = partial(work, spider=spider, task_queue=queue, config=config)

        while True:
            task = queue.get()
            scheduler.put(partial_work_func, (task,))
