import json

import requests


url = 'http://127.0.0.1:5000/search/common/wxaccount/select?account=chaoliunvren88'
d = json.dumps({'id': 50000328, 'name': '穿衣潮搭配', })
d2 = {'id': 50000328, 'name': '穿衣潮搭配', }
requests.post(url, data=d2)