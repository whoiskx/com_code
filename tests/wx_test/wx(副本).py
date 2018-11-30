import time

import requests


def abuyun_proxy():
    # if not USE_PROXY:
    #     return False
    # proxy_host = "http-dyn.abuyun.com"
    # proxy_port = "9020"
    # # 代理隧道验证信息
    # proxy_user = "H47MY63960OG8D8D"
    # proxy_pass = "DA3B03DDAEE0CDF7"
    proxy_host = "http-dyn.abuyun.com"
    proxy_port = "9020"
    proxy_user = "HA8J88B72RMD896D"
    proxy_pass = "B9DC78EE0EE4DB7B"
    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_user,
        "pass": proxy_pass,
    }
    proxies = {
        "http": proxy_meta,
        "https": proxy_meta,
    }
    return proxies


proxies = abuyun_proxy()
count_proxy = 0
headers = {
           # 'Cookie': 'pt2gguin=o0574613576; RK=3dIUcz6EF6; ptcz=cf0a39e4feb932ca0c2da4fdb1775b583939a88cc966c7df7506eb28b0f2adbe; rewardsn=; wxtokenkey=777; uin=o0574613576; skey=@rmE5odnTH; ptisp=os; pgv_info=ssid=s2408541644; pgv_pvid=2134856442; sig=h01da9139101aec63f42fba9e2ab28c4134da0b888791d75b88c23cc1085c08ff13f2bbbbf70dc09328',
           'Host': 'mp.weixin.qq.com',
           'Referer': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1543393801&ver=1&signature=hQDpZ3Kj-jSImow1GKOSD9k5HYbv0VER36-NMwH5s058DQuhwNnfRzmI5jkDoVeCdZznnBKKqrGBllRoGe84mw==',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
#
# proxies = {
#         'https': "http://localhost:1080",
#         'http': 'http://localhost:1080'
#
#     }
# proxies = {"https": "http://localhost:1080", }
while True:
    account_link = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1543399223&ver=1&signature=0YJG5t3bkxCgwJwZc3nstJOta0rtxNv7wdbf0fgmMbMgGiKLHdLdFbs5uVUdLpAlsXTKj0ni-b7bpmFbWjuhlg=='
    # account_link = 'https://www.facebook.com/ckkoffice'
    homepage = requests.get(account_link, proxies=proxies, headers=headers)
    print(homepage)
    if '<title>请输入验证码 </title>' in homepage.text:
        count_proxy += 1
        with open('wx_{}.txt'.format(count_proxy), 'w', encoding='utf-8') as f:
            f.write(homepage.text)
        print('历史页需要输入验证码，重新发送请求 {}'.format(count_proxy))
        time.sleep(0.5)
    else:
        print('获取页面成功')
        break
