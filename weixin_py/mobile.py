# -*- coding: utf-8 -*-
import requests
import re
import html


class Mobile(object):
    def __init__(self):
        pass

    def run(self):
        url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjEwNjI0NzM4MQ==&scene=124&uin=MTk3OTM0NzMxMQ%3D%3D&key=c768c5a77e81d0028070dd50324701764d83da096891ef217f6960c8e39039277394b2addf4a0c70c092cffef018b0a08992f22ff15c0d2ae179f300e74b8e04eb7ed7561e19c5fabce93bf958ec5616&devicetype=android-22&version=26050731&lang=zh_CN&nettype=3gnet&a8scene=1&pass_ticket=https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA5NTg2MTEwMA==&scene=124&devicetype=android-19&version=26060532&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=Q%2F3OLZ9qhQBTgrsMyxcZYa7yuxMX5h4JFtEnCxDV%2F2dMI7Sucevc7uIX1%2BK6or%2Fo&wx_header=1%27%20-H%20%27Host:%20mp.weixin.qq.com%27%20-H%20%27Connection:%20keep-alive%27%20-H%20%27Accept:%20text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8%27%20-H%20%27x-wechat-uin:%20MTk3OTM0NzMxMQ%3D%3D%27%20-H%20%27x-wechat-key:%20700d516b3f9c9921111662e593b5f557edbdc6035e32a7927dde351905ba3b41eae097b3d7a25d47d7d3281bdc05b93d1bbb046cd3a1cd376519e1b5ed0e0af7331931ffb2edc6f715444679513a8b55%27%20-H%20%27User-Agent:%20Mozilla/5.0%20(Linux;%20Android%204.4.2;%20vivo%20X20%20Build/NMF26X)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Version/4.0%20Chrome/30.0.0.0%20Mobile%20Safari/537.36%20MicroMessenger/6.6.5.1280(0x26060532)%20NetType/WIFI%20Language/zh_CN%27%20-H%20%27Accept-Language:%20zh-CN,en-US;q=0.8%27%20-H%20%27Cookie:%20wxuin=1979347311;%20devicetype=android-19;%20version=26060532;%20lang=zh_CN;%20pass_ticket=Q/3OLZ9qhQBTgrsMyxcZYa7yuxMX5h4JFtEnCxDV/2dMI7Sucevc7uIX1+K6or/o;%20wap_sid2=CO/i6a8HElxBN3Z3el9FYzdxYjJsU3JUbnFrdER0WUh1UnpSQ0JGMUpBV240aXJiTmF0TkxnVzFUY2tIc0w0YUs3djRsQWpZd2YxblFydGl0dURmbEZ0di1IcUt1Y3dEQUFBfjCU2bLcBTgNQJVOOGqqBqT9kt9DM5VN1Q1Iahweu01CgdhkRF8qi218uDwfZRShpUgAUcINFrqqa%2Ffc'
        index_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA5ODUzOTA0OQ==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=44a583e876248c8c32001333967b15067f38cac501cd75c683e8ebefac6c84bb4fbca8712bba0e453fada0db724bbd0a99676e9f1163e609e58d7067cf3110267cdf5ba1946404fec7dcaa1b14e01c27&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=ktwKhTuQVAnqINc9i46vlSW58NmLhwSQecJbbQ66pC8dB7PQ2i%2F6%2BnxtgdjDV5Bf&winzoom=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        resp = requests.get(index_url, headers=headers)
        # print(resp.text)
        # with open('mobile.html', 'w', encoding='utf-8') as f:
        #     f.write(resp.text)

        match_url = re.search('var msgList =.*?\';', resp.text).group()
        escape_url = html.unescape(match_url)

        urls = re.findall(r'mp.weixin.qq.com.*?#wechat_redirect', escape_url)
        prefix = 'https://mp.weixin.qq.com/s?'
        for url in urls:
            url = prefix + url.replace('amp;', '').replace(r'mp.weixin.qq.com\\/s?', '')
            print(url)
        print('end')


def main():
    test = Mobile()
    test.run()


if __name__ == '__main__':
    main()
