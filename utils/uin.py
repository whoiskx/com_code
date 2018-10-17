# -*- coding: utf-8 -*-
wxuin = '1156918861'.encode()
# -*- coding: utf-8 -*-
import base64
import requests

#
# # uin
# uin = base64.b64encode(wxuin)
#
# def convert_to_permanent_url(temp_url):
#     pre_redirect_url = "".join([temp_url, "&uin=", uin])
#     response = requests.head(pre_redirect_url)
#     permanent_url = response.headers['Location']
#     return permanent_url
# temp= 'https://mp.weixin.qq.com/s?src=11&timestamp=1539592850&ver=1183&signature=ZNgK7MzcRo*67n6PDJo7UyPOJKR434yEbN-O3eRO1vNz8as8lIwzIdvC1pO86O5ja31rmbednmNA2dXRJ2pJS-vpfA4n8sykXgMVzGKnhd8kyqGEJbs3Z2-oROa*l4wY&new=1'
# r = convert_to_permanent_url(temp)
# print(r)
biz = 'MzAxOTgyMjA1NA=='
key = '0ff3713247d3532c437a688be7c66ca6ffd2d58297743d81932896db2ec6a62ff8c2196561e1f24775d4facffbbff1c73a97d8911f0a070f0701f86f1554b8f729ea1ae1cb3d48f0aeab6e0bec431199'
uin = 'MTE1NjkxODg2MQ%3D%3D'
wz_url = "http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s&uin=%s&key=%s" % (
    biz, uin, key)
headsers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
}
r = requests.get(wz_url, headers=headsers, allow_redirects=False)
print(r.text)
print(r.cookies)
print(r.headers)
kwargs = {
    'mid': '2768393603',
    'sn': '',
    'idx': '1',
}
biz = "MzA4MjQxNjQzMA=="
url = 'http://mp.weixin.qq.com/mp/getappmsgext?'
url = url + '__biz=' + biz + '&'
url = url + 'mid=' + kwargs.get('mid', None) + '&'
url = url + 'sn=' + kwargs.get('sn', None) + '&'
url = url + 'idx=' + kwargs.get('idx', None) + '&'
url = url + 'is_need_ad=0'
