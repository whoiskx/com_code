import time
from random import randint

from selenium import webdriver
import json
import re
from setting import urun, driver_facebook
from pyquery import PyQuery as pq

driver = webdriver.Chrome()

with open("all_friends.txt", 'r', encoding="utf-8") as f:
    results = json.load(f)
# print(results, type(results))
# driver = driver_facebook()

for count, d in enumerate(results):
    link = "https://www.facebook.com/dimon.liu2?fref=pb&hc_location=friends_tab"
    # driver.get(d.get("link", ''))
    try:
        link = d.get('link')
        name = d.get('name')
        driver.get(link)
        print(d.get("name"))
        time.sleep(1)

        index_html = driver.page_source
        e = pq(index_html)
        all_inform = e("._30f")

        account_name = []
        home_page = []
        location = ''
        come_form = ''
        job = []
        degree = []
        all_profile = e.text()
        list_profile = all_profile.split("\n")
        for item in list_profile:
            if "-" in item:
                job.append(item)
            elif "曾" in item:
                degree.append(item)
            elif "所在地" in item:
                location = item
            elif "来自" in item:
                come_form = item
        account_name = d.get("name")
        home_page.append(link)
        urun['facebook'].insert(
            {"account_name": account_name, 'home_page': home_page, 'location': location, 'come_form': come_form,
             "job": job,
             "degree": degree, "is_get": True})
        time.sleep(randint(1, 3))
    except Exception as e:
        print(count, name, e)
        continue
print('end')
