# -*- coding: utf-8 -*-
#
# def t():
#     return 0
#
# p = t()
# print(p)
#
# s = 'NDAyNzE2MzQ1Ng==|9068b8cf3c4b19e45129213ddbfd60a0a4b10387abb2db3296048c71611f4c428b902eeefd2b0f6141cd9defbec3f54b603f7ba42281a66422c8b69bed0942a773e931c42b379547337bc4643f6d48d3'
# key_uin = s.split('|')
# if key_uin:
#     uin, key = key_uin
#     print(uin)
#     print(key)
# import json
#
# import requests
#
# url = 'http://183.131.241.60:38011/nextaccount?label=5'
# r = requests.get(url)
# info_str = r.text
# info_list= json.loads(info_str)
# for info in info_list:
#     _biz = info.get('biz')
# 
# s = 'content_url":"http:\\/\\/mp.weixin.qq.com\\/s?__biz=MzIzMDQyMjcxOA==&amp;mid=2247486157&amp;idx=1&amp;sn=6c582fa94c4a0da0821a0fc624dd17cc&amp;chksm=e8b2eb1cdfc5620ac7edbd655113f0725875b4fbcdb5777e4bacaa40c57993535985112742d0&amp;scene=27#wechat_redirect'
# url = s.replace('amp;', '').replace('content_url":"http:\\/\\/mp.weixin.qq.com\\/s?', '')
# print(url)
import requests
# url = 'http://183.131.241.60:38011/outkey'
# _biz = ''
# while True:
#     r = requests.get(url)
#     print(r.text)
#     key_uin = r.text.split('|')
#     if len(key_uin) == 2:
#         uin, key = key_uin
#         url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
#                    'action=home&__biz={}&uin={}&key={}'.format(_biz, uin, key)
#         break
#     else:
#         print('none')
#         uin = ''
#         key = ''
# for i in range(2):
#     s = requests.Session()
#     r = s.get('https://mp.weixin.qq.com/profile?src=3&timestamp=1536203019&ver=1&signature=NHsz0BdTJaHizbwPPaEODtFV*unABNSLtg*PGevDLZ4dk6dzGAcREd9LbWW3pKjIwCc9Oq8evkihia9XfLP6Xg==')
#     with open('code.html', 'w', encoding='utf-8') as f:
#         f.write(r.text)
#     if '验证码' in r.text:
#         print('find')
#     cc = r.cookies.get_dict()
#     print(cc)

# with open('ids.txt', 'r', encoding='utf-8') as f:
#     name_all = f.read()
# id_list = name_all.split("\n")
# print(id_list)

import pymongo

conn = pymongo.MongoClient('mongodb://120.78.237.213:27017')
urun = conn.weCaht
