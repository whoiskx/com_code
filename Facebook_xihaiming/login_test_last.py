import time
from random import randint

from selenium import webdriver
import json
import re
from setting import db, driver_facebook
from pyquery import PyQuery as pq
g
# driver = webdriver.Chrome()

with open("all_friends.txt", 'r', encoding="utf-8") as f:
    results = json.load(f)
print(results, type(results))
driver = driver_facebook()

for count, d in enumerate(results):
    link = "https://www.facebook.com/longson.chang/about?lst=1682293696%3A1816532918%3A1529546966"
    # driver.get(d.get("link", ''))
    driver.get(link)
    print(d.get("name"))
    time.sleep(1)

    index_html = driver.page_source
    data_tab = re.findall(r'data-tab-key="about".*?>', index_html)

    url_introduction = re.findall(r'https.*?"', data_tab[-1])
    driver.get(url_introduction[0])

    introduction_html = driver.page_source
    print('==')

    profile = re.findall(r'<div class="_4ms4".*?</ul></div></div></div>', introduction_html)

    e = pq(profile[0])
    # print(e)
    # all = e("._c24 _50f4")
    # job = ''
    # address = e("._c24 _50f4").find('a').text()
    # sex = ''
    # print("======")
    # print(all)
    # print(address)
    #
    # # with open("temp.html", "r", encoding="utf-8") as f:
    # #     html = f.read()
    # # e = pq(html)
    # # print(e, len(e))
    # address = e(".profileLink")

    host, school, job = '', '', ''

    address = e("._50f4").text()
    if '所在地' in address:
        host = address.split("：")[1]
        address = address.split("：")[0]
        address = address.replace('所在地', '')
    if '曾' in address:
        school = address.split(" ")[-2]
        address = address.replace(school, "")
    if "-" in address:
        job = address.split("-")[-1]
    print("====")
    print(address, type(address))
    print(host, school, job)
    db['facebook'].insert(
        {"host": host, 'school': school, 'job': job, 'url_profile': url_introduction[0], "name": d.get("name")})
    time.sleep(randint(1, 3))
    if count == 3:
        break
