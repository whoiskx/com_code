# -*- coding: utf-8 -*-
import requests

with open('test.jpg', 'rb') as f:
    img_b = f.read()
url = "http://127.0.0.1:5000/"
data = {"content": img_b}
s = requests.post(url, data=data)
print(s)
