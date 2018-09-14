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
d = {'name': '文松小品王adf', 'account': 'afwsxpw12313669', 'feature': '精选小品;搞笑视频;世间动态;关注小品有内涵.', 'certification': 'affadsf',
     'imageUrl': 'afadf',
     'message': True, 'status': 0}
r = requests.post(url, json=d)
print(r.status_code)
print(r.text)

s = 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; LSTMV=0%2C0; LCLKINT=235; PHPSESSID=qvdgtcif7omomgook8bb7vs8n2; SUIR=1FC521300A0E7EA98FD8DC830B40B654; sct=279; seccodeErrorCount=1|Fri, 14 Sep 2018 08:36:40 GMT; SNUID=CED36F3DE7E39337419D0C50E70409F0; seccodeRight=success; successCount=1|Fri, 14 Sep 2018 08:36:47 GM'
