import requests

url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=&key=&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&winzoom=1"
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTEW Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6. 0.0.54r849063.501 NetType/WIFI'
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/WIFI'
    }

resp = requests.get(url, headers=headers)
print(resp.status_code)
print(resp.text)