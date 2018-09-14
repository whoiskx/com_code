# -*- coding: utf-8 -*-
# import time
# from selenium import webdriver
# browser = webdriver.Chrome()
# url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=gh_2219b94b95b1&ie=utf8&_sug_=n&_sug_type_='
# url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=qqwrd007&ie=utf8&_sug_=n&_sug_type_='
# browser.get(url)
# time.sleep(2)
# if '搜公众号' in browser.page_source:
#     for i in range(30):
#         browser.get(url)
#         time.sleep(0.1)
# print('end')

import requests

url = 'http://58.56.160.39:38012/MediaManager/api/weixinInfo/add'
d = {'name': '文松小品王adf', 'account': 'afwsxpw12313669', 'feature': '精选小品;搞笑视频;世间动态;关注小品有内涵.', 'certification': 'affadsf', 'imageUrl': 'afadf',
     'message': True, 'status': 0}
r = requests.post(url, json=d)
print(r.status_code)
print(r.text)