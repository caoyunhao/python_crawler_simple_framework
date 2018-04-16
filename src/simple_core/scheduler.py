# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:53
# @Author  : Yunhao Cao
# @File    : scheduler.py
import time
import threading
import queue as Queue

__author__ = 'Yunhao Cao'

__all__ = [
    'Scheduler',
]


def work_func(func, args, kwargs, queue, token):
    args = args or []
    kwargs = kwargs or {}
    func(*args, **kwargs)
    queue.put(token)


def wait_func(wait_queue, work_queue):
    while True:
        task = wait_queue.get()
        func, args, kwargs = task
        token = work_queue.get()
        args = [func, args, kwargs, work_queue, token]
        t = threading.Thread(target=work_func, args=args)
        t.daemon = True
        t.start()


class ThreadPool(object):
    def __init__(self, size):
        self.size = size
        self.wait_queue = None
        self.work_queue = None
        self.wait_thread = None
        self.init()

    def init(self):
        self.wait_queue = Queue.Queue()
        self.work_queue = Queue.Queue(maxsize=self.size)
        for i in range(self.size):
            self.work_queue.put(i)
        wait_thread = threading.Thread(target=wait_func, args=[self.wait_queue, self.work_queue])
        wait_thread.daemon = True
        wait_thread.start()

    def put(self, func, args=None, kwargs=None):
        self.wait_queue.put((func, args, kwargs))


class Scheduler(object):
    def __init__(self, size=4):
        self.pool = ThreadPool(size)

    def put(self, func, args=None, kwargs=None):
        self.pool.put(func, args, kwargs)


def hello(*args):
    print(args)
    print('{} says \'hello\' to {}.'.format(args[0], args[1]))
    time.sleep(5)
    print('{} end.'.format(args))
    return args


def _test():
    tp = ThreadPool(2)
    tp.put(hello, ['a', 'b'])
    tp.put(hello, ['c', 'd'])
    tp.put(hello, ['e', 'f'])
    tp.put(hello, ['1', '2'])
    tp.put(hello, ['3', '4'])

    print('main exit.')


if __name__ == '__main__':
    _test()
