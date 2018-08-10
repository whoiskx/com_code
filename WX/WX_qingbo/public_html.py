import requests

url = 'http://mp.weixin.qq.com/s?__biz=MjM5ODc2ODc4OQ==&mid=2652543602&idx=1&sn=f72df4a413cfba5e8c0194d853ec70dd&chksm=bd2b83888a5c0a9efc341b63c8db0b75a8b6e4d3285078d4e1608d2be6eda34a46936447c7df&scene=27#wechat_redirect'

resp = requests.get(url)
print(resp.text)
with open('wx.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)