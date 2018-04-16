# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 21:47
# @Author  : Yunhao Cao
# @File    : downloader.py
import requests
from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType

__author__ = 'Yunhao Cao'

__all__ = [
    'DownloaderFactory',
]


class Response(object):
    def __init__(self, text, url, origin_url):
        self.text = text
        self.url = url
        self.origin_url = origin_url

    def __bool__(self):
        return self.text is not None


class SimpleResponse(Response):
    def __init__(self, text, url, origin_url):
        super().__init__(text, url, origin_url)


class DownloaderFactory(object):
    def creator(self, headers=None, proxy=None, dynamic=False):
        if dynamic:
            downloader = DynamicDownloader()
        else:
            downloader = SimpleDownloader()
        downloader.configure(headers=headers, proxy=proxy)
        return downloader


class Downloader(object):
    def get(self, *args, **kwargs):
        raise NotImplementedError


class SimpleDownloader(Downloader):
    def __init__(self):
        self._headers = None
        self._proxies = None

    def get(self, url, params=None):
        r = requests.get(url, params=params)
        return SimpleResponse(r.text, r.url, url)

    def configure(self, **kwargs):
        self._headers = kwargs.get("headers")
        proxy = kwargs.get("proxy")
        if proxy:
            self._proxies = {
                "http": "http://{}".format(proxy.ip),
                "https": "http://{}".format(proxy.ip),
            }


class DynamicDownloader(Downloader):
    def __init__(self, driver=None):
        if driver:
            self._driver = driver
        else:
            self._driver = webdriver.PhantomJS("phantomjs")

    def __del__(self):
        if self._driver:
            self._driver.quit()

    def get(self, url, **kwargs):
        """
        线程不安全
        :param url:
        :param kwargs:
        """
        self._driver.get(url)
        return SimpleResponse(self._driver.page_source, self._driver.current_url, url)

    def configure(self, **kwargs):
        headers = kwargs.get("headers")
        proxy = kwargs.get("proxy")

        desired_capabilities = {
            "browserName": "safari",
            "version": "",
            "platform": "ANY",
            "javascriptEnabled": True,
            "cookiesEnabled": True,
            "phantomjs.page.settings.loadImages": False,
        }

        if headers:
            for k, v in headers.items():
                desired_capabilities['phantomjs.page.customHeaders.{}'.format(k)] = v

        if proxy:
            webdriver_proxy = webdriver.Proxy()
            webdriver_proxy.proxy_type = ProxyType.MANUAL
            webdriver_proxy.http_proxy = proxy.ip
            webdriver_proxy.add_to_capabilities(desired_capabilities)

        self._driver.start_session(capabilities=desired_capabilities)


def _test():
    pass


if __name__ == '__main__':
    _test()
