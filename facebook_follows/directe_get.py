import time
from random import randint

from selenium import webdriver
import json
import re
from setting import urun, driver_facebook
from pyquery import PyQuery as pq

def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('gua.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


# driver = webdriver.Chrome()

with open("all_friends.txt", 'r', encoding="utf-8") as f:
    results = json.load(f)
log(results, type(results))

driver = driver_facebook()

error_count = 0
for count, d in enumerate(results):
    # link = "https://www.facebook.com/longson.chang/about?lst=1682293696%3A1816532918%3A1529546966"
    # driver.get(d.get("link", ''))
    if count <= 00:
        log("skip {} {}".format(count, d.get('name')))
        continue
    log("begin {}", count)
    try:
        link = d.get('link')
        name = d.get('name')
        driver.get(link)
        log(d.get("name"))
        time.sleep(2)

        index_html = driver.page_source
        data_sex = re.findall(r'"addFriendText".*?<', index_html) or re.findall(r'<span class="FollowLink">.*?</span>', index_html)
        sex = ''
        log(data_sex)
        if data_sex != []:
            if '他' in data_sex[0]:
                sex = 'man'
            if "她" in data_sex[0]:
                sex = "woman"


        profile = re.findall(r'<div id="intro_container_id">.*?</ul></div>', index_html)
        if profile == []:
            error_count += 1
            log("error {} : {} {}".format(error_count, count, link))
        e = pq(profile[0])

        account_name = ''
        home_page = ''
        location = ''
        come_form = ''
        job = ''
        degree = ''
        follows = ''
        all_profile = e.text()
        log(all_profile)

        list_profile = all_profile.split("\n")
        for item in list_profile:
            if "-" in item and job == '':
                job = item
            elif "曾经" in item and degree == '':
                degree = item
            elif "所在地" in item:
                location = item
            elif "来自" in item:
                come_form = item
            elif "粉丝" in item:
                follows = item

        account_name = d.get("name")
        home_page = link
        urun['facebook'].insert(
            {"account_name": account_name, 'home_page': home_page, 'location': location, 'come_form': come_form,
             "job": job, 'followers': follows,
             "degree": degree, "sex": sex, "is_get": True})
        log("insert sucessful")
        time.sleep(randint(2, 5))
        if count >= 600:
            break
    except Exception as e:
        log(count, name, e)
        continue
log('end')
driver.close()