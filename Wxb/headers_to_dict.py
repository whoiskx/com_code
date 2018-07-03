headers = """Host: mp.weixin.qq.com
Connection: keep-alive
Content-Length: 931
Origin: https://mp.weixin.qq.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*
Referer: https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142500&idx=1&sn=77fbb51f69117d7b573e17928f1a26ce&chksm=bd0ed5338a795c252d9f33b3cb267ef2554ed83e4373207c013d1da02401f5836765d45bbcba&scene=0&ascene=7&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACgA%2Bix4A44seAEKPHgBllR4AepUeAICVHgDwlR4AOJYeAJ2WHgC1lh4AAAA%3D&lang=zh_CN&pass_ticket=lmz4dXv%2FWib0B0%2B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%2FdJNeVlTua%2FCMp8Ki&wx_header=1
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh-CN;q=0.8,en-US;q=0.6
Cookie: rewardsn=; wxtokenkey=777; wxuin=1156918861; devicetype=android-26; version=26060739; lang=zh_CN; pass_ticket=lmz4dXv/Wib0B0+0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW/dJNeVlTua/CMp8Ki; wap_sid2=CM3c1KcEElwzNkN1N1hyclZxcUVJdWRxcmx2VTJyZ3d6VEI4UWNJQ25CeUIwREdZYXBDNjVTbWtDYWhvRUhQZmNDVjR1QVBiQzRLa3g3ZGJUc3BpcHhLNEhKZzFPc01EQUFBfjDpm+vZBTgNQAE=
Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044109&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL00 &RL=1080*2040&OS=8.0.0&API=26
Q-GUID: c23b47cd4280ad4e1a425962102888cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b"""



items = headers.split("\n")
# print(items)
d = {}
for item in items:
    k, v = item.split(": ", 1)

    d[k] = v.strip()
print(d)
