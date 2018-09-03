import datetime
import json

import requests

url = 'http://127.0.0.1:5000/search/common/wxaccount/select?account=chaoliunvren88'
d = {'id': 126762962, 'name': '诺和诺德唐山郊区组', 'url': 'http://weixin.sogou.com/gzh?openid=oIWsFtxKrqEr7itlDaimZxbnrHnM',
     'account': 'immissifaf13123',
     'collectiontime': '', 'biz': 'MzAwMTA2MzUzNQ=='}
# d2 = {'id': 50000328, 'name': '穿衣潮搭配', }
requests.post(url, data=d)
