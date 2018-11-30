# -*- coding: utf-8 -*-
from io import BytesIO

import requests
ID = '126766281'
url = 'http://183.131.241.60:38011/SaveImage?accountid='.format(ID)
f = open('test.jpg', 'rb')
data = f.read()
t = BytesIO()
t.write(data)
d = t.getvalue()
s = requests.post(url, data=d)
print(s.status_code)
print('end')