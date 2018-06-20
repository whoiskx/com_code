from pyquery import PyQuery as pq

# with open("index_xihaiming.html", "r", encoding="utf-8") as f:
with open("copy_index.html", "r", encoding="utf-8") as f:
    html = f.read()
    # print(html)
# html = html.replace('<!-- <div', '<div')
# html = html.replace('--></code>', '</code>')


# e = pq(html)
#
# all = e(".uiList _262m _4kg")
#
# name = e(".fsl fwb fcb")
# new = pq(name)
# name_2 = new('.fsl fwb fcb').html()

# print(all, name, type(name_2))
from bs4 import BeautifulSoup
import re
soup = BeautifulSoup(html, "lxml")
# r = soup.find_all(name='div')
#
# r = soup.findAll("div", {"class": "hidden_elem"})
# print(r)

# results = re.findall(r'<a href="https://www.facebook.com/profile.php.*?</a>', html)
# result = []
# for url in results:
#     e = pq(url)
#     name = e("a").text()
#     link = e('a').attr("href")
#     result.append({"name": name, "link": link})
#
# print(results)
# print("==========")
# print(result)


results = re.findall(r'<div class="fsl fwb fcb">.*?</div>', html)
result = []
for index, url in enumerate(results) :
    e = pq(url)
    name = e("a").text()
    link = e('a').attr("href")
    result.append({"name": name, "link": link})

print(results)
print("==========")
print(result)

import json
r = json.dumps(result)
with open("all_friends.txt", "w", encoding="utf-8") as f:
    f.write(r)
print(index)
