import requests
from pyquery import PyQuery as pq

url = 'https://movie.douban.com/top250'

resp = requests.get(url)
print(resp.status_code)
# print(resp.text)

e = pq(resp.text)
q = e(".item")
# q = qq(".info")
for i in q.items('.info'):
    item = {}
    item['name'] = i("span").eq(0).text()
    item['quote'] = i('.quote').eq(0).text()
    print(item)
print(q[1])