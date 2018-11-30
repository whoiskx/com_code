# -*- coding: utf-8 -*-
import requests
url = 'http://127.0.0.1:1111/ReadImage'
params = dict(path=r'Images\45445\45445454.jpg')

r = requests.get(url ,params=params)
print(r.text)
print(r.status_code)