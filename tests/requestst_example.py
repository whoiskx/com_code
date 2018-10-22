# -*- coding: utf-8 -*-
import time

import requests


def main():
    url = 'http://weixin.sogou.com/api/share?timestamp=1539244801&signature=qIbwY*nI6KU9tBso4VCd8lYSesxOYgLcHX5tlbqlMR8N6flDHs4LLcFgRw7FjTAO*R9o10ANaKDMEchDmiGRDb47tG*AW2Kgcj2*6vmDdN3eJdDwdDknqg3oFwtYMi8pXzwa9DrdpgftQZ4vHdqhiW9rJR5*R3JC5te2RzFIt1UN796VLVb8xmu-OYToszjno2mCC1yiDXW1P6c9T8bFt2TCgIPueMHmShkUaDyFcq4='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    r = requests.get(url)
    print(r.text)
    # from selenium import webdriver
    # d = webdriver.Chrome()
    # d.get(url)
    # time.sleep(10)


if __name__ == '__main__':
    # main()
    # for i in range(10):
        url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=yljyjt&ie=utf8&_sug_=n&_sug_type_='
        headers = {
        'Cookie':'ABTEST=0|1540189245|v1; SNUID=E6C67A29F2F68A39B22B3E09F35724B0; IPLOC=CN4401; SUID=143489DB721A910A000000005BCD6C3D; SUID=143489DB5018910A000000005BCD6C3D; JSESSIONID=aaa-lAxGGKRzP4ODRmIzw; SUV=006D6411DB8934145BCD6C3E87B85433'
        # "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        from pyquery import PyQuery as pq
        print(pq(r.text)('title'))
        # print(r.text)
