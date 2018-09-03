import datetime
import json

import requests

url = 'http://127.0.0.1:5000/search/common/wxaccount/select?account=chaoliunvren88'
d = {
    # 'id': 127762999,
    'name': '泓升源律所', 'url': 'http://weixin.sogou.com/gzh?openid=oIWsFtxl2qXfiTUqtT4kz94OeKl4',
    'account': 'fjl652_fa',
    'collectiontime': datetime.datetime.now(), 'biz': 'MzUzOTI0ODE2MQ=='}
# d2 = {'id': 50000328, 'name': '穿衣潮搭配', }
requests.post(url, data=d)
