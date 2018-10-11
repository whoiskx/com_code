# -*- coding: utf-8 -*-
import time

import requests


def main():
    url = 'http://t.cn/E7yaTzI'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    # }
    # r = requests.get(url)
    # print(r.text)
    from selenium import webdriver
    d = webdriver.Chrome()
    d.get(url)
    time.sleep(10)


if __name__ == '__main__':
    main()
