import requests

# 广州佛山
# url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=a6RM70vbT%25252F1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_LttIuaYARdVNC5GJ6GPF2E8A4nmE3oNtXAeiOl_SlsubN4v5T_bmFe0bcA46Iqm2v1EJ0D7n8KyM4fPv&x5=1&f=json"
url = 'https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142500&idx=1&sn=77fbb51f69117d7b573e17928f1a26ce&chksm=bd0ed5338a795c252d9f33b3cb267ef2554ed83e4373207c013d1da02401f5836765d45bbcba&scene=0&ascene=7&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACgA%2Bix4A44seAEKPHgBllR4AepUeAICVHgDwlR4AOJYeAJ2WHgC1lh4AAAA%3D&lang=zh_CN&pass_ticket=lmz4dXv%2FWib0B0%2B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%2FdJNeVlTua%2FCMp8Ki&wx_header=1'
url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=9971a8088dcd256b5c7e393ac6040dc0293ec332ebf538582b5aace75441e6c9839104e02dde01de1991dfb7d7157c84bbc1b307faab31189e0bb7b685b3018bf2125c0e2aa0779314e3ff2ffc4da8fb&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=jydkRwK%2BcnrlvADJ%2F3fcV9F%2FuxIfP9b2GHVxlDOgYvC72Yytm1bIgn%2BWRWF09aay&winzoom=1'
url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_y0eLdh2Qk%252F4vkN9%252B2NJZzmO-jbPJH0r-OoygiiPF3b6L8Fi_n2M097XkkGWXJEDbsCFFcWhMyMs4cG7l&x5=1&f=json'

# headers = {'Host': 'mp.weixin.qq.com', 'Connection': 'keep-alive', 'Content-Length': '978',
#            'Origin': 'https://mp.weixin.qq.com', 'X-Requested-With': 'XMLHttpRequest',
#            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
#            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*',
#            'Referer': 'https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142299&idx=2&sn=e3e403a47fe694a0ec71ab765d0b2043&chksm=bd0ed6cc8a795fdaac756beb8f5f767e46bbe9282153b51c053f508b4317813604f4e88f4a1d&scene=126&ascene=0&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACQA9ix4A44seAEKPHgCzlB4A%2BZQeAGWVHgB6lR4AgJUeAPCVHgAAAA%3D%3D&lang=zh_CN&pass_ticket=a6RM70vbT%2F1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD&wx_header=1',
#            'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
#            'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1156918861; devicetype=android-26; version=26060739; lang=zh_CN; pass_ticket=a6RM70vbT/1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD; wap_sid2=CM3c1KcEElxVWHBDMTJDdUZrVXEzeXp0YzA5V25SM3hINDhtYXFoUUtVZ0VBUVpFQ21QQXZsUDliLV9LNGJ4RFVrTUxwUXc5X3E3dHVjSFA0c0RJRnlSaldYUnF6TU1EQUFBfjDhu9HZBTgNQAE=',
#            'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044109&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL00 &RL=1080*2040&OS=8.0.0&API=26',
#            'Q-GUID': 'c23b47cd4280ad4e1a425962102888cb', 'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'}
headers = {'Host': 'mp.weixin.qq.com', 'Connection': 'keep-alive',
           # 'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
           'x-wechat-key': '2b274b589c4330f832ac676d7717fbb6c826cd9f2844b7fe589b6ab9db7593af4c441f78ae01ad4f2912bbd941f3309b28b921ba77373cf8b706a4b767c353a9422413ceab58b585a764a4e5288c3536',
           'x-wechat-uin': 'MTE1NjkxODg2MQ%3D%3D',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
           'Cookie': 'rewardsn=; wxuin=1156918861; devicetype=android-26; version=26060739; lang=zh_CN; pass_ticket=lmz4dXv/Wib0B0+0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW/dJNeVlTua/CMp8Ki; wap_sid2=CM3c1KcEElxBcV9NT2FZSGxOWmhkOFRMOU9iVHBLdERqTV9HZmhtbmQ4NVIyV3BoN3BoSHJ1ZXJIZk5Va1JNNTRSUG5RaUJYS0c2a1VPVmt4NHEwV3EtT3FmRDRtY01EQUFBfjDvmuvZBTgNQAE=; wxtokenkey=777',
           'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044109&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL00 &RL=1080*2040&OS=8.0.0&API=26',
           'Q-GUID': 'c23b47cd4280ad4e1a425962102888cb', 'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'}

headers123 = {
    'Host': 'mp.weixin.qq.com', 'Connection': 'keep-alive', 'Content-Length': '931',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
    'Referer': 'https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142500&idx=1&sn=77fbb51f69117d7b573e17928f1a26ce&chksm=bd0ed5338a795c252d9f33b3cb267ef2554ed83e4373207c013d1da02401f5836765d45bbcba&scene=0&ascene=7&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACgA%2Bix4A44seAEKPHgBllR4AepUeAICVHgDwlR4AOJYeAJ2WHgC1lh4AAAA%3D&lang=zh_CN&pass_ticket=lmz4dXv%2FWib0B0%2B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%2FdJNeVlTua%2FCMp8Ki&wx_header=1',
    'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1156918861; devicetype=android-26; version=26060739; lang=zh_CN; pass_ticket=lmz4dXv/Wib0B0+0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW/dJNeVlTua/CMp8Ki; wap_sid2=CM3c1KcEElwzNkN1N1hyclZxcUVJdWRxcmx2VTJyZ3d6VEI4UWNJQ25CeUIwREdZYXBDNjVTbWtDYWhvRUhQZmNDVjR1QVBiQzRLa3g3ZGJUc3BpcHhLNEhKZzFPc01EQUFBfjDpm+vZBTgNQAE=',

}

body = 'r=0.9039583323000335&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142299&sn=e3e403a47fe694a0ec71ab765d0b2043&idx=2&scene=126&title=%25E4%25B8%2580%25E5%2591%25A8%25E6%25A6%259C%25E5%258D%2595%25EF%25BC%259A%25E7%25A6%2585%25E5%259F%258E%25E5%25BC%25A0%25E6%25A7%258E%25E5%258D%2595%25E7%259B%2598%25E5%25BC%2582%25E5%2586%259B%25E7%25AA%2581%25E8%25B5%25B7%2520%25E4%25B8%2589%25E6%25B0%25B4%25E9%25AB%2598%25E6%2598%258E%25E7%258B%25AC%25E5%258D%25A0%25E6%25A6%259C%25E5%258D%25956%25E5%25B8%25AD&ct=1530008232&abtest_cookie=BAABAAoACwAMABIACQA9ix4A44seAEKPHgCzlB4A%2BZQeAGWVHgB6lR4AgJUeAPCVHgAAAA%3D%3D&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=342523003080310784&is_need_reward=1&both_ad=0&reward_uin_count=18&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=2812znOYhwcKXd2gXkA4QdeX&pass_ticket=a6RM70vbT%25252F1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD&is_temp_url=0&item_show_type=undefined&tmp_version=1'

resp = requests.get(url, headers=headers)
print(resp.status_code)
print(resp.text)
