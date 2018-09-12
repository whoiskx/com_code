# -*- coding: utf-8 -*-
import requests
import base64
url = 'http://127.0.0.1:1111/SaveImage'
with open('test.jpg', 'rb') as f:
    img_b = f.read()
data = {'content':base64.b64encode(img_b), 'account_id': 45445454}
r = requests.post(url, data=data)
print(r.status_code)