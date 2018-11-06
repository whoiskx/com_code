# encoding=utf-8
# import pymongo
# conn = pymongo.MongoClient('120.78.237.213', 27017)
# db = conn.WeChat
# db['account'].insert({})
#
# class A(object):
#     cc = 1
#     def __init__(self):
#         pass
#
# a = A()
# print(a.cc)
# A.cc += 1
# b = A()
# print(b.cc)

# from app import SaveCookie
#
# one_cookie = SaveCookie
import re
import time
from collections import Counter

import jieba
import requests

# url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=arqnyry2017&ie=utf8&_sug_=n&_sug_type_='
# url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1536486381&ver=1112&signature=ScE-pz2hLr1V1tkIu6wxp76JFxUI4rkl-qRkSiil*c*6W4mipqM0O0WtvasHF6rdzg*H8*wK0*2kTvoLclGPIGZ6eHbfpBimCmQsbULvAusMvza0NRWC25g4z5KFqZP7&new=1'
# url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=jdzfhk&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=1565&sst0=1536470115264&lkt=0%2C0%2C0'
# headers = {
# }
# cookies = {'JSESSIONID': 'aaavp31avj27S5eZm8Dvw', 'SUID': '14CF2A3B2E18960A000000005B94DFAF', 'ABTEST': '0|1536483247|v1', 'SNUID': '2FF511013A3F4F56591CA0FF3B9BA01E', 'IPLOC': 'CN4401'}
# # cookies = {'JSESSIONID': 'aaaZAKyLkpkGzgbSYjEvw', 'SUID': '14CF2A3B2E18960A000000005B9775F4', 'ABTEST': '1|1536652788|v1', 'SNUID': '459E7869515427C18AC5C311527C336B', 'IPLOC': 'CN4401'}
# cookies = {'JSESSIONID': 'aaaM-9HbF7EBXed_dnEvw', 'SUID': '14CF2A3B2E18960A000000005B978BC2', 'ABTEST': '8|1536658368|v1', 'seccodeErrorCount': '1|Tue, 11 Sep 2018 09:38:07 GMT', 'SUIR': '1536658370', 'IPLOC': 'CN4401', 'PHPSESSID': 'vfbbj1sb8ag1cc10n2nbm8o082', 'SUV': '0046538E3B2ACF145B978BC2E3386974', 'refresh': '1', 'SNUID': 'E337D2CCF7FD8D6DD11D5543F89167BA', 'seccodeRight': 'success', 'successCount': '2|Tue, 11 Sep 2018 09:37:58 GMT'}
# r = requests.get(url, headers=headers, cookies=cookies)
# print(r.text)
# from pyquery import PyQuery as pq
# print(pq(r.text)("#js_content").text().replace('\n', ''))
# print("end")

# 查询公众号
# url = 'http://183.131.241.60:38011/MatchAccount?account=gh_2219b94b95b1'
# r = requests.get(url)
# print(type(r.json()))
# s = r.json().get('imageUrl')
# print(s)
# if len(s) == 0:
#     print("头像不存在")
#     url_save = 'http://183.131.241.60:38011/SaveImage'
#     r_save = requests.post(files=r_img.content)
#     print(r_save.status_code)
# else:
#     print("头像存在,判断是否正确")
#
#
# url2 = 'http://60.190.238.188:38016/{}'.format(s)
# r_img = requests.get(url2)
# print(r_img)
# # else:
# #     print("头像存在")
# if r_img.text:
#     print('存在')
# else:
#     url_save = 'http://183.131.241.60:38011/SaveImage'
#     r_save = requests.post(files=r_img.content)
#     print(r_save.status_code)
#
# url = 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt-9qc9wQlpNOwJuYnewXRlQ'
# r = requests.get(url)
# url2 = 'http://183.131.241.60:38011/SaveImage'
# s = requests.post(url2, files=r.content)
# print(s.status_code)


# info = {"name": "佛山市华诚餐饮管理有限公司", "account": "fsshccyglyxgs",
#      "features": "佛山市华诚餐饮管理有限公司是一家从田头到餐桌,产业链化经营的餐饮管理、饭堂承包与食材配送专家.公司立足佛山,辐射珠三角,为广大企业、学校、机关单位提供安全、营养的食品解决方案.",
#      "certified": "佛山市华诚餐饮管理有限公司"}
# url = 'http://183.131.241.60:38011/AddNewAccount?json='
# from send_backpack import Zhongxing
# test = Zhongxing()
# test.name = info.get('name')
# test.account = info.get('account')
#
# test.features = info.get('features')
# test.certified = info.get('certified')
#
# resp = requests.post(url, json=test.to_dict())
# print(resp.status_code)

# 分词
# content = '赵饶生身为党员领导干部，丧失理想信念和党性原则，严重违反党的纪律和国家法律法规，并涉嫌职务犯罪，性质恶劣、情节严重。依据《中国共产党纪律处分条例》《中华人民共和国监察法》等有关规定，经中共萍乡市委批准，中共萍乡市纪委、萍乡市监察委员会决定给予赵饶生开除党籍处分、取消其退休待遇；收缴赵饶生违纪违法所得；将赵饶生涉嫌挪用公款、滥用职权犯罪问题移送检察机关依法审查、提起公诉'
# key_words_list = []
# seg_list = jieba.cut(content)
# for s in seg_list:
#     if re.search('[\u4e00-\u9fff]+', s):
#         key_words_list.append(s)
# print(key_words_list)
# with open('positive.txt', 'r', encoding='utf-8') as f:
#     positive = f.read()
# with open('nagetive.txt', 'r', encoding='utf-8') as f:
#     nagetive = f.read()
# # key_list = list(key_words_counter)
# count_positive = 0
# count_nagetive = 0
# for key in key_words_list:
#     if key in positive.split('\n'):
#         count_positive += 1
#     if key in nagetive.split('\n'):
#         count_nagetive += 1
# print(count_positive)
#
# print(count_nagetive)

# 读写正负词
#
# with open('positive.txt', 'r', encoding='utf-8') as f:
#     positive = f.read().split('\n')
# with open('nagetive.txt', 'r', encoding='utf-8') as f:
#     nagetive = f.read().split('\n')
# print(len(positive))
# print(len(nagetive))
#
# print(len(set(positive)))
# print(len(set(nagetive)))
#
# print('end')

from flask import Flask
from selenium import webdriver

app = Flask(__name__)

d = webdriver.Chrome()


@app.route('/<ids>/<ids2>')
def hello_world(ids=1, ids2=None):
    print('开始')
    d.get('https://www.baidu.com/')
    time.sleep(1)
    return '{}_{}'.format(ids, ids2) + '   {}'.format(d.current_url)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=38017, threaded=True)
    info = dict(name='cold', blog='linuxzen.com')
    info.update({'name': 'cold night', 'blogname': 'linuxzen'})
    print(info)