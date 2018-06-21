from pyquery import PyQuery as pq
import re


with open("profile.html", "r", encoding="utf-8") as f:
    html = f.read()

# get 简介
# result = re.findall(r'data-tab-key="about".*?>', html)
#
# e = pq(result[0])
# print( re.findall(r'https.*?"', result[0]))


result = re.findall(r'<div class="_4ms4".*?</ul></div></div></div>', html)

e = pq(result[0])
# print(e)
# all = e("._c24 _50f4")
# job = ''
# address = e("._c24 _50f4").find('a').text()
# sex = ''
# print("======")
# print(all)
# print(address)

# with open("temp.html", "r", encoding="utf-8") as f:
#     html = f.read()
# e = pq(html)
# print(e, len(e))
# # address = e(".profileLink")



address = e("._50f4").text()
if  '所在地' in address:
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