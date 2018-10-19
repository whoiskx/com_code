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
# s = requests
# biz = 'MjM5MTI2MTI0MA=='
# key = 'a0f3e22b7b882d0e22d418b47306dab801707e708d8f8f99abae3e718f41ed8aa5ff31d88352bf16e3fca527f27f4733a790b1df9bc0a8bb5cd0fa6ff15b60c5632e2668b49a38b465e2ee1141668bc7'
# uin = 'MjE0ODcyODk0MA%3D%3D'
# wz_url = "http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s&uin=%s&key=%s" % (
#     biz, uin, key)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'}
# r = s.get(wz_url, headers=headers, allow_redirects=False)
# print(r.text)
# print(r.cookies.get_dict())
# print(r.headers)
#
# cook_value = ''
# for k, v in r.cookies.get_dict().items():
#     cook_value += k + '=' + v + ';'
# cook_value = cook_value
# print(cook_value)
#
# cookies = r.cookies
kwargs = {
    'mid': '2655142500',
    'sn': '77fbb51f69117d7b573e17928f1a26ce',
    'idx': '1',
}
biz = "MjM5MTI2MTI0MA=="
url = 'http://mp.weixin.qq.com/mp/getappmsgext?'
url = url + '__biz=' + biz + '&'
url = url + 'mid=' + kwargs.get('mid', None) + '&'
url = url + 'sn=' + kwargs.get('sn', None) + '&'
url = url + 'idx=' + kwargs.get('idx', None) + '&'
url = url + 'is_need_ad=0'
print(url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'Cookie': 'devicetype=android-23;lang=zh_CN;version=26070334;wap_sid2=COyAzIAIElw3SUdHa2J1MmRpUXZObjRhakt3NXBJSFVURG1hazAwRmJxNjlBVVVhYWZ1Q1padG52UjYwVGpES0NtQWw3MEE1Ql9IdUVKX21EclVzcWNEWFVCOVZGZE1EQUFBfjCOyqHeBTgMQAo=;wxuin=2148728940;',
}
r_cookies = requests.post(url, data={'is_only_read':1}, headers=headers)
print(r_cookies.status_code)
print(r_cookies.text)
