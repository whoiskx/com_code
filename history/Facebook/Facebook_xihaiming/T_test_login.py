import time
from random import randint
import json
import re
from setting import urun, driver_facebook
from pyquery import PyQuery as pq

#  抓取测试
# with open("all_friends.txt", 'r', encoding="utf-8") as f:
#     results = json.load(f)
# print(results, type(results))
# driver = driver_facebook()
#
# for count, d in enumerate(results):
#     # link = "https://www.facebook.com/longson.chang/about?lst=1682293696%3A1816532918%3A1529546966"
#     # driver.get(d.get("link", ''))
#     try:
#         link = d.get('link')
#         name = d.get('name')
#         driver.get(link)
#         print(d.get("name"))
#         time.sleep(1)
#
#         index_html = driver.page_source
#         data_sex = re.findall(r'"addFriendText".*?<', index_html)
#         sex = ''
#         print(data_sex)
#         if '他' in data_sex[0]:
#             sex = 'man'
#         if "她" in data_sex[0]:
#             sex = "woman"
#
#         data_tab = re.findall(r'data-tab-key="about".*?>', index_html)
#
#         url_introduction = re.findall(r'https.*?"', data_tab[-1])
#         driver.get(url_introduction[0])
#         print("url", url_introduction)
#         introduction_html = driver.page_source
#         print('==')
#
#         profile = re.findall(r'<div class="_4ms4".*?</ul></div></div></div>', introduction_html)
#
#         e = pq(profile[0])
#
#         account_name = []
#         home_page = []
#         location = ''
#         come_form = ''
#         job = []
#         degree = []
#         all_profile = e.text()
#         list_profile = all_profile.split("\n")
#         for item in list_profile:
#             if "-" in item:
#                 job.append(item)
#             elif "曾" in item:
#                 degree.append(item)
#             elif "所在地" in item:
#                 location = item
#             elif "来自" in item:
#                 come_form = item
#         account_name = d.get("name")
#         home_page.append(link)
#         urun['facebook'].insert(
#             {"account_name": account_name, 'home_page': home_page, 'location': location, 'come_form': come_form,
#              "job": job,
#              "degree": degree, "sex": sex, "is_get": True})
#         time.sleep(randint(1, 3))
#     except Exception as e:
#         print(count, name, e)
#         continue
# print('end')
# fooo = 'abc'


# driver = driver_facebook()
print(1)
def foo():
    print(2)
