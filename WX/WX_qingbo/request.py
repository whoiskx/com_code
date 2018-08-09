import requests

url = 'http://www.gsdata.cn/rank/wxdetail?wxname=RQ3BVDvSaJ3qIi0nMgg5O0O0O2O0O0O1'
url = 'http://183.131.241.60:38011/nextaccount?label=0'
resp = requests.get(url)
print(resp.status_code)
print(resp.text)
