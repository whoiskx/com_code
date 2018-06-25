import time
from random import randint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
from setting import driver_facebook
import re



# with open("group_members.html", "r", encoding="utf-8") as f:
#     html = f.read()

driver = driver_facebook()
time.sleep(2)
driver.get('https://www.facebook.com/groups/southmongoliasupport/members/')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
print("ok")


def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(randint(1, 3))
        print(i)


execute_times(80)

html = driver.page_source
with open("group_members.html", "w", encoding="utf-8") as f:
    f.write(html)
group_members_div = re.findall(r'<div id="groupsMemberBrowser".*?<div id="bottomContent"></div>', html)
print('afasdf', group_members_div)
if group_members_div == []:
    print("not find group_members_div")
e = pq(group_members_div[0])
# print(e('_6a'))
# e('._6a')('.fsl').find('a').attr('href')

all_members_div = e('._6a')('.fsl')
results = []
for member in all_members_div:
    members_url = pq(member).find('a').attr('href')
    name = pq(member).find('a').text()
    results.append({"name": name, 'url': members_url})

print(results)
print(len(results))
import json

s = json.dumps(results, indent=2, ensure_ascii=False)
with open('members_url.txt', 'w', encoding='utf-8') as f:
    f.write(s)
