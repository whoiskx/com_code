import requests

url = 'http://www.gsdata.cn/rank/wxdetail?wxname=RQ3BVDvSaJ3qIi0nMgg5O0O0O2O0O0O1'
resp = requests.get(url)
print(resp.status_code)
print(resp.text)
