import re
import time

import requests


name = '大鼎豫剧'
url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='.format(name)

resp_search = requests.get(url)
# print(resp_search.text)

from pyquery import PyQuery as pq

e = pq(resp_search.text)
account_linke = e(".tit").find('a').attr('href')

resp = requests.get(account_linke)
# print(resp.text)

html = resp.text
items = re.findall('"content_url":".*?,"copyright_stat"', html)


for item in items:
    url_last = item[15:-18].replace('amp;', '')
    # print(url)
    url = 'https://mp.weixin.qq.com' + url_last
    resp_article = requests.get(url)
    r = pq(resp_article.text)
    print(r("h2").text())
    time.sleep(1)

# e = pq(resp.text)
