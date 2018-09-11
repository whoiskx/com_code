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

import requests
# url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=arqnyry2017&ie=utf8&_sug_=n&_sug_type_='
# url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1536486381&ver=1112&signature=ScE-pz2hLr1V1tkIu6wxp76JFxUI4rkl-qRkSiil*c*6W4mipqM0O0WtvasHF6rdzg*H8*wK0*2kTvoLclGPIGZ6eHbfpBimCmQsbULvAusMvza0NRWC25g4z5KFqZP7&new=1'
# headers = {
# }
# cookies = {'JSESSIONID': 'aaavp31avj27S5eZm8Dvw', 'SUID': '14CF2A3B2E18960A000000005B94DFAF', 'ABTEST': '0|1536483247|v1', 'SNUID': '2FF511013A3F4F56591CA0FF3B9BA01E', 'IPLOC': 'CN4401'}
# r = requests.get(url, headers=headers, cookies=cookies)
# # print(r.text)
# from pyquery import PyQuery as pq
# print(pq(r.text)("#js_content").text().replace('\n', ''))
# print("end")

# 查询公众号
url = 'http://183.131.241.60:38011/MatchAccount?account=gh_2219b94b95b1'
r = requests.get(url)
print(type(r.json()))
s = r.json().get('imageUrl')
print(s)
if len(s) == 0:
    print("头像不存在")
    url_save = 'http://183.131.241.60:38011/SaveImage'
    r_save = requests.post(files=r_img.content)
    print(r_save.status_code)
else:
    print("头像存在,判断是否正确")


url2 = 'http://60.190.238.188:38016/{}'.format(s)
r_img = requests.get(url2)
print(r_img)
# else:
#     print("头像存在")
if r_img.text:
    print('存在')
else:
    url_save = 'http://183.131.241.60:38011/SaveImage'
    r_save = requests.post(files=r_img.content)
    print(r_save.status_code)

# url = 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt-9qc9wQlpNOwJuYnewXRlQ'
# r = requests.get(url)
# url2 = 'http://183.131.241.60:38011/SaveImage'
# s = requests.post(url2, files=r.content)
# print(s.status_code)
