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
url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=arqnyry2017&ie=utf8&_sug_=n&_sug_type_='
headers = {
}
cookies = {'JSESSIONID': 'aaaMNOC3w6UnQ-DFl7Dvw', 'SUID': '14CF2A3B5118910A000000005B94AE49', 'ABTEST': '5|1536470600|v1', 'SNUID': 'A07A9F8EB5B0C1DDC5EA5D2EB5C27C8D', 'IPLOC': 'CN4401'}
cookies = {'JSESSIONID': 'aaaMNOC3w6UnQ-DFl7Dvw', 'SUID': '14CF2A3B5118910A000000005B94AE49', 'ABTEST': '5|1536470600|v1', 'SUIR': 'A07A9F8EB5B0C1DDC5EA5D2EB5C27C8D', 'IPLOC': 'CN4401', 'SNUID': '5A8264754E483827C5777CF24ED8B9E3', 'PHPSESSID': '78n8tcono1felpb3ius35qb9p3', 'SUV': '00B92B863B2ACF145B94B007DE1F9444', 'seccodeRight': 'success', 'successCount': '1|Sun, 09 Sep 2018 05:35:51 GMT', 'refresh': '1'}
cookies = {'JSESSIONID': 'aaaMNOC3w6UnQ-DFl7Dvw', 'SUID': '14CF2A3B5118910A000000005B94AE49', 'ABTEST': '5|1536470600|v1', 'SUIR': 'A07A9F8EB5B0C1DDC5EA5D2EB5C27C8D', 'IPLOC': 'CN4401', 'SNUID': '5A8264754E483827C5777CF24ED8B9E3', 'PHPSESSID': '78n8tcono1felpb3ius35qb9p3', 'SUV': '00B92B863B2ACF145B94B007DE1F9444', 'seccodeRight': 'success', 'successCount': '1|Sun, 09 Sep 2018 05:35:51 GMT'}
cookies = {'SUID': '14CF2A3B2E18960A000000005B94BC1A', 'ABTEST': '3|1536474137|v1', 'seccodeErrorCount': '2|Sun, 09 Sep 2018 06:27:20 GMT', 'SUIR': '1536474137', 'IPLOC': 'CN4401', 'SNUID': 'E239DCCCF7F3839DB384BE21F78219AD', 'PHPSESSID': 'ffe2uhlspmes9g6oikh8ct4ee7', 'SUV': '00CA47B13B2ACF145B94BC1AE06F7863', 'seccodeRight': 'success', 'successCount': '1|Sun, 09 Sep 2018 06:27:38 GMT', 'JSESSIONID': 'aaaoKApmGNdzbabt7MBvw'}
cookies = {'SUID': '14CF2A3B2E18960A000000005B94BC1A', 'ABTEST': '3|1536474137|v1', 'seccodeErrorCount': '2|Sun, 09 Sep 2018 06:27:20 GMT', 'SUIR': '1536474137', 'IPLOC': 'CN4401', 'SNUID': 'E239DCCCF7F3839DB384BE21F78219AD', 'PHPSESSID': 'ffe2uhlspmes9g6oikh8ct4ee7', 'SUV': '00CA47B13B2ACF145B94BC1AE06F7863', 'seccodeRight': 'success', 'successCount': '1|Sun, 09 Sep 2018 06:27:38 GMT', 'JSESSIONID': 'aaaoKApmGNdzbabt7MBvw'}
cookies = {'SUID': '14CF2A3B2E18960A000000005B94BC1A', 'ABTEST': '3|1536474137|v1', 'seccodeErrorCount': '2|Sun, 09 Sep 2018 06:27:20 GMT', 'SUIR': '1536474137', 'IPLOC': 'CN4401', 'PHPSESSID': 'ffe2uhlspmes9g6oikh8ct4ee7', 'refresh': '1', 'SUV': '00CA47B13B2ACF145B94BC1AE06F7863', 'SNUID': 'E239DCCCF7F3839DB384BE21F78219AD', 'seccodeRight': 'success', 'successCount': '1|Sun, 09 Sep 2018 06:27:38 GMT', 'JSESSIONID': 'aaaoKApmGNdzbabt7MBvw'}
cookies =  {'SUID': '14CF2A3B5118910A000000005B94C089', 'ABTEST': '7|1536475273|v1', 'seccodeErrorCount': '1|Sun, 09 Sep 2018 06:46:16 GMT', 'SUIR': '1536475273', 'IPLOC': 'CN4401', 'SNUID': '5A8165744F4A3A24C8D5AFC64F993E41', 'PHPSESSID': 'm6cr9ro8e96tq9d0lhr0uoo042', 'SUV': '001417803B2ACF145B94C089D4680507', 'seccodeRight': 'success', 'successCount': '1|Sun, 09 Sep 2018 06:46:25 GMT', 'JSESSIONID': 'aaa50wBVcWaK4bhy7QBvw'}
r = requests.get(url, headers=headers, cookies=cookies)
print(r.text)
print("end")