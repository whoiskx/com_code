# encoding=utf-8
import json

import requests

body_one = [{'headers': {'topic': 'weixin', 'key': '2acaeb6539ff729a3dc32eccd110d151', 'timestamp': 1534301213},
            'body': json.dumps({'ID': '2acaeb6539ff729a3dc32eccd110d151', 'Account': 'smzdc2015', 'TaskID': '59508952',
                     'TaskName': '微信_什么值得吃', 'AccountID': '59508952', 'SiteID': 59508952, 'TopicID': 0,
                     'Url': 'http://mp.weixin.qq.com/s?__biz=MjM5NzI5ODE3Nw==&mid=2655272406&idx=1&sn=eeb38a3738567c52bcaeabba58468d30&chksm=bd6cb4b88a1b3daec72f1187291340dd8cbabaad7d40b526b351690a89a9e39f186cf41e40de&scene=27#wechat_redirect',
                     'Title': 'abc',
                     'Content': 'abcd',
                     'Author': '什么值得吃', 'Time': 1534082400000, 'AddOn': 1534301213000})}]
url0 = 'http://101.71.28.12:12007/'
url1 = 'http://115.231.251.252:26016/'
url2 = 'http://60.190.238.168:38015/'
body = json.dumps(body_one)

# body = body_one
print(body)

r = requests.post(url0, data=body)
print(r.status_code)
print(r.text)

url = 'http://27.17.18.131:38072'
r = requests.post(url1, data=body)
print(r.status_code)
print(r.text)

print("=====")
r2 = requests.post(url2, data=body)
print(r2.status_code)
print(r2.text)
