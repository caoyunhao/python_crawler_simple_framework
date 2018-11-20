# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:48
# @Author  : Yunhao Cao
# @File    : cqueue.py
import queue as thread_queue

from . import logger
from .task import RequestTask

__author__ = 'Yunhao Cao'

__all__ = [
    'WebRequestQueue',
]


class Queue(object):
    def get(self, block, timeout):
        raise NotImplementedError

    def _put_one(self, task, block=True, timeout=None):
        raise NotImplementedError

    def put(self, task, block=True, timeout=None):
        if isinstance(task, (list, tuple)):
            for task_ in task:
                self.put(task_, block, timeout)
        else:
            self._put_one(task, block, timeout)


class FIFOQueue(Queue):
    def __init__(self):
        self.queue = thread_queue.Queue(100)

    def get(self, block=True, timeout=None):
        return self.queue.get(block, timeout)

    def _put_one(self, task, block=True, timeout=None):
        return self.queue.put(task, block, timeout)


class WebRequestQueue(FIFOQueue):
    def __init__(self):
        super().__init__()

    def get(self, block=True, timeout=None):
        return super().get(block, timeout)

    def _put_one(self, task, block=True, timeout=None):
        logger.info('WebRequestQueue: put new request')
        if not isinstance(task, RequestTask):
            task = RequestTask(task)
        return super()._put_one(task, block, timeout)
