#encoding=utf-8
from __future__ import absolute_import, unicode_literals, print_function

import requests

url = "https://graph.facebook.com/820882001277849?access_token=1589926074663087|0oYs68afqIR56YzQvM3T4QC_qDo"
proxy_host = "223.93.172.248:3128"
proxies = {"http": "http://{}".format(proxy_host), "https": "https://{}".format(proxy_host)}
headers = {'Host': 'graph.facebook.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cookie': 'datr=OxkjW4MYaIelucIws97V02xW; wd=1920x946; sb=_R0jWyoRctx7GnDrlLyCjFE2; c_user=100005036989194; xs=32%3Am5RP8dyGJGCEZg%3A2%3A1529028093%3A-1%3A-1; pl=n; fr=0ICeTuNMbW3ThPfuj.AWW3O-4qdU12Mkzlc15GCq9APr4.BbHxb1.s-.Fsj.0.0.BbIx39.; act=1529028586747%2F2'}
url_weibo = "https://weibo.com/login.php"
resp = requests.get(url_weibo, proxies=proxies)
print(resp.status_code)
#
# url_google = "https://www.google.com/"
# resp = requests.get(url_google, proxies=proxies)
# print(resp.status_code)


resp = requests.get(url, headers=headers)
print(resp.text)

#
# def _main():
#
#     with open("fbtoken", "r") as f:
#         for i in range(290):
#             token = f.readline()
#             url_add = "https://graph.facebook.com/820882001277849?access_token={}".format(token)
#
#
#
# if __name__ == '__main__':
#     _main()
