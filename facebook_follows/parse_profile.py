from pyquery import PyQuery as pq
import re


with open("profile.html", "r", encoding="utf-8") as f:
    html = f.read()

result = re.findall(r'<div class="_4ms4".*?</ul></div></div></div>', html)

e = pq(result[0])
print(e)
all = e("._c24 _50f4")
job = ''
address = e("._c24 _50f4").find('a').text()
sex = ''
print("======")
print(all)
print(address)