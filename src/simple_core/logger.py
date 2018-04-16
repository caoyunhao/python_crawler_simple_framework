# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:45
# @Author  : Yunhao Cao
# @File    : logger.py
import logging

__author__ = 'Yunhao Cao'

__all__ = [
    'simple_config',
    'config',
    'debug',
    'info',
    'warning',
    'error',
]


def config(**kwargs):
    """
    Configure logger. Detail reference -> logging
    - filename: output filename
    - level: output level for file. default:INFO
    - format: output format
    - datefmt: output time format
    - console_level: output level for console. Default=level
    :return:
    """
    level = kwargs.get("level", logging.INFO)
    filename = kwargs.get("filename")
    fmt = kwargs.get("format")
    datefmt = kwargs.get("datefmt")
    # formatter = logging.Formatter(fmt, datefmt)

    logging.basicConfig(**{
        "filename": filename,
        "level": level,
        "format": fmt,
        "datefmt": datefmt
    })
    # sh = logging.StreamHandler(sys.stdout)
    # sh.setFormatter(formatter)
    # sh.setLevel(kwargs.get("console_level") or level)
    # logging.getLogger().addHandler(sh)
    # error solo file
    # if filename:
    #     temp1 = filename.split('/')
    #     temp2 = temp1[-1].split('.')
    #     temp2[0] += "-err"
    #     temp1[-1] = ".".join(temp2)
    #     error_filename = "/".join(temp1)
    #     # error FileHandler
    #     error_fh = logging.FileHandler(error_filename)
    #     error_fh.setFormatter(formatter)
    #     error_fh.setLevel(logging.ERROR)
    #     logging.getLogger().addHandler(error_fh)


def simple_config():
    config(**{
        "filename": None,
        "level": logging.DEBUG,
        "format": "%(asctime)s [%(process)-4d] %(levelname)-8s : %(message)s",
        "datefmt": "[%Y-%m-%d %H:%M:%S]",
    })


simple_config()


def debug(msg):
    logging.debug(msg)


def info(msg):
    logging.info(msg)


def warning(msg):
    logging.warning(msg)


def error(msg):
    logging.error(msg)


def _test():
    simple_config()
    info('123')


if __name__ == '__main__':
    _test()
