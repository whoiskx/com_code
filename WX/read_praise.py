import requests

# 文章url  title： 16大重点项目曝光...
# https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142500&idx=1&sn=77fbb51f69117d7b573e17928f1a26ce&chksm=bd0ed5338a795c252d9f33b3cb267ef2554ed83e4373207c013d1da02401f5836765d45bbcba&scene=0&ascene=7&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACQA%2Bix4A44seAEKPHgBllR4AepUeAICVHgDwlR4AOJYeAECWHgAAAA%3D%3D&lang=zh_CN&pass_ticket=OkFDOiNd7psMLd3HldZ6Kn1ywxmBqa9tVPH5FNCSuqgiovE9Yh7q383n4MGAZp0C&wx_header=1

# 阅读， 点赞url
# token 不一样
# url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=OkFDOiNd7psMLd3HldZ6Kn1ywxmBqa9tVPH5FNCSuqgiovE9Yh7q383n4MGAZp0C&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_vYUG5h8P9mPbLYinp24LriJbd95NwIaRGctnUMTMk3tEnZYyR2eiFd9iHRjwvRtsrBvfyUX3HsbUB9YN&x5=1&f=json"
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=OkFDOiNd7psMLd3HldZ6Kn1ywxmBqa9tVPH5FNCSuqgiovE9Yh7q383n4MGAZp0C&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_mKqWZet%252Bmfd8I1qeeSjLahtEdHFaki3Qf55eKu4unrMtaYluOCNVAUq4JDyH0Bxf8uSDmBekgCKCydnV&x5=1&f=json'
# url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_IoR1FqXdTlesOsvHBeI_4II5vI73Pha-hoAiR_5oPcLK7w5qI3GHXHV6MZHvBr2EloLELILW5ilCtmrC&x5=1&f=json"
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_wKPsRhpxFXdYEnuwp24LriJbd95NwIaRGctnUJcfN8a_O9NEz3VsqAciOg41my3J3D3BuhqdQmcSExLd&x5=1&f=json'
# url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_J7uQz%252FCk9lF38YVtpMc_v8nSLLSlKXzcLUm1ll55TwFi7Kj_4jliYm8h1ifS05ygrNcONYs19x2MNTWk&x5=1&f=json"
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_cI5JtQQiJoNz6IEsnCl8y7O-S7SHCQf3ojBnlSFIysZnPnvO_fBOVv5-gVc4P_3TfjUy45lSmvHbW5NT&x5=1&f=json'
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_HFhZqNHe7Yjbqezommn5vWjyTp1BqiSw2--6GS3FwQmcFI7Qdj2PgV9FkaWJWCjXPSkCypZ_oHr9uW1J&x5=1&f=json'
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=963_%252BhnDVI%252FL0fskfB%252BcnRKHBjfYIQo4W0PIGepOnSOof4XUVjvnUEjzzyXbNdkHNiLYIk7dDFw-WPk6CzXB&x5=1&f=json'
# # 7-4 精简版
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=963_%252BwsoPU9E%252FCxhLtOzLCninA0nfnHTIAhlWLDHeE47zI4jnl2CcjaMSDXwghkq5ENUCphcSiQYs_X299b5'
#
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_jqDK%252B92npDB6ncEBknIu6aWjgyCY_ENcCgh5J8u2XqO2ey0HAP7lw0BzXkPSeaySKbOivS8QuvzbB1Pb'
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_luJbqcqXKERruLHRQ_iNgRz4uJqdit5zoZgmRxO7E1TcsmpExfgnrhjbti0ZCweVy1FZTjBx86cE96Sg'
#
# # 7-6
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_Ckc4nrE%252BKFESCo8tb8Uc5MV3IDkHYPXSkMbkb0HNB8fqAaTT_IBJeWk42VYluDuWWxLUEXdvOSbyWTvq'
#
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=&key=&pass_ticket=&wxtoken=777&devicetype=Windows10&clientversion=6206034e&appmsg_token=&x5=0&f=json'
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=RL8TANw3a2uzGuzxpTGq%25252Fv9ttSNlfhd3Z7C9YYjVarP3ciiyDXggESx5mx63k2%25252Bh&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token=964_MKRUcyweLsTmXZCPb8Uc5MV3IDkHYPXSkMbkb8vWXVEyR_fhK60drmG9LWu7_nGIB3AWqgf3sn2hN7-a&x5=1&f=json'
url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_lDSn8DoRqyCzqkc0sGAjnKF7BcfSO6AdzU6gBh76NQAzdnBnKKIY6NT1W5fxYmgRKMJCriqEDfctPibh'
# headers = {'Host': 'mp.weixin.qq.com', 'Connection': 'keep-alive', 'Content-Length': '978',
#            'Origin': 'https://mp.weixin.qq.com', 'X-Requested-With': 'XMLHttpRequest',
#            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
#            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*',
#            'Referer': 'https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142299&idx=2&sn=e3e403a47fe694a0ec71ab765d0b2043&chksm=bd0ed6cc8a795fdaac756beb8f5f767e46bbe9282153b51c053f508b4317813604f4e88f4a1d&scene=126&ascene=0&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACQA9ix4A44seAEKPHgCzlB4A%2BZQeAGWVHgB6lR4AgJUeAPCVHgAAAA%3D%3D&lang=zh_CN&pass_ticket=a6RM70vbT%2F1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD&wx_header=1',
#            'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh-CN;q=0.8,en-US;q=0.6',
#            'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1156918861; devicetype=android-26; version=26060739; lang=zh_CN; pass_ticket=a6RM70vbT/1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD; wap_sid2=CM3c1KcEElxVWHBDMTJDdUZrVXEzeXp0YzA5V25SM3hINDhtYXFoUUtVZ0VBUVpFQ21QQXZsUDliLV9LNGJ4RFVrTUxwUXc5X3E3dHVjSFA0c0RJRnlSaldYUnF6TU1EQUFBfjDhu9HZBTgNQAE=',
#            'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.7&TBSVC=43610&CO=BK&COVC=044109&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= BKL-AL00 &RL=1080*2040&OS=8.0.0&API=26',
#            'Q-GUID': 'c23b47cd4280ad4e1a425962102888cb', 'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'}
#
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
    # 7-4 精简版
    # 'Cookie': 'wap_sid2=CM3c1KcEElxBLTIzc1N6ZWNPd3hBRUdRUzFqLXp1TUdPa2FrT1hhQkNscHI4ZS1YaTRqQmw1Wk5PMERROTFjUVJaTTJORlgtU0VqRDY4MEJOSUtmRk9TOTJjQ3RrY1FEQUFBfjDPgPvZBTgNQAE='
    # 'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; pgv_si=s5130477568; pgv_info=ssid=s1752605724; rewardsn=; wxtokenkey=777; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=q90l2zowsSLwuhdc39cc5e6cNbxy//Jx4aMMIVsQe3IfV3UMAU3akajcYxmzpPj7; wap_sid2=CM3c1KcEElwwME5Hd09IWUdKRkpDbW1NMXVOMFl1QnljLVhKNTlZZHJuVTJfaDVfNW1vN3g0VHVFV1JJeElCZlR2R2JFV1htaUtaZ0V2VW13d2NXdFc1cVJfcGk3TVFEQUFBfjDRk/vZBTgNQAE='
    # 'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1156918861; devicetype=android-26; version=26060739; lang=zh_CN; pass_ticket=RL8TANw3a2uzGuzxpTGq/v9ttSNlfhd3Z7C9YYjVarP3ciiyDXggESx5mx63k2+h; wap_sid2=CM3c1KcEElxjRjdGRG00NlpqNklnd01rcVVXOEFRYU1PRkFwdGd1aWkxUFZJSXlfenJ6ME11M0lHcGhhT1FmRlpwRnVoS0p3SnFUQ2tzUE5QbjlpNzk2UDlpNDFtOFFEQUFBfjCrk/zZBTgNQAE='
    "Cookie": "wap_sid2=CM3c1KcEElxHbUtVbGpCaktLMDRmaVNiSHhZOEg0UkpGdmRYQjctX3ZDUlVEd0NPdElQQmFDN3p2VEQwb09fc2o5SDJ0STJiSDZKMFpLUUhNeUpWX1VrYUxFdGtwOFFEQUFBfjCylfzZBTgNQAE="
}



body = '__biz=MjM5NjA3Mzg2MA%3D%3D&mid=2651859458&sn=500d5155a48a98a31bf48f386fce23d3&idx=1&title=%25E8%25B7%25AF%25E6%259C%25AB%25E9%2595%25BF%25E5%25AE%2589%25C2%25B7%25E5%258C%2597%25E4%25BA%25AC%25EF%25BC%2588%25E8%258A%2582%25E9%2580%2589%25EF%25BC%2589&is_only_read=1'

# 江南
# body = '__biz=MjM5NjA3Mzg2MA%3D%3D&mid=2651859439&sn=da8dddf93890c0c582c8bb0e09c62064&idx=1&title=%25E5%25BD%2593%25E4%25BD%25A0%25E5%25BC%2580%25E5%2590%25AF%25E4%25B8%2580%25E6%25AE%25B5%25E6%2596%25B0%25E7%2594%259F%25E6%25B4%25BB%25E7%259A%2584%25E6%2597%25B6%25E5%2580%2599%25E9%259C%2580%25E8%25A6%2581%25E4%25BA%259B%25E4%25BB%2580%25E4%25B9%2588&is_only_read=1'
# body = '__biz=MzA4ODE3OTY5NQ%3D%3D&mid=2649707871&sn=508403ef8e9adc1902a9c3ec75b1d17f&idx=1&title=%25E8%2580%2581%25E6%259D%25BF%25E6%2598%25AF%25E9%259C%2580%25E8%25A6%2581%25E7%25AE%25A1%25E7%259A%2584&is_only_read=1'

# guangzhou
# body = '__biz=MjM5ODQ0NTk1Mg%3D%3D&mid=2650806545&sn=82851f004d9271e50e14481b3280fa4c&idx=1&title=%25E5%258D%258E%25E5%25B8%2588%25E5%2586%258D%25E7%258E%25B0%25E6%259A%25B4%25E9%259C%25B2%25E5%258F%2598%25E6%2580%2581%25E7%258B%2582%25EF%25BC%259F%25EF%25BC%2581%25E4%25B8%2580%25E5%2591%25A8%25E4%25B8%25A4%25E4%25B8%25AA%25EF%25BC%2581%25E9%25AB%2598%25E6%25A0%25A1%25E5%25AD%25A6%25E7%2594%259F%25E5%25AE%2589%25E5%2585%25A8%25E9%259A%2590%25E6%2582%25A3%25E4%25B8%258D%25E5%25AE%25B9%25E5%25B0%258F%25E8%25A7%2586%25EF%25BC%2581&is_only_read=1'

# # 君临
# body = '__biz=MzI0MDU1OTc2OA%3D%3D&mid=2247491528&sn=956b758d1ddd5dc1b0c3d7c8288258a4&idx=1&title=%25E7%25A5%259E%25E9%25A9%25AC%25E6%258F%25AD%25E9%259C%25B2%25E5%259B%25BD%25E4%25BC%2581%25E9%2580%25A0%25E5%2581%2587%25E4%25B9%258B%25E8%25B0%259C&is_only_read=1'
# body = '__biz=MzI0MDU1OTc2OA%3D%3D&mid=2247491528&sn=956b758d1ddd5dc1b0c3d7c8288258a4&idx=1&title=%25E7%25A5%259E%25E9%25A9%25AC%25E6%258F%25AD%25E9%259C%25B2%25E5%259B%25BD%25E4%25BC%2581%25E9%2580%25A0%25E5%2581%2587%25E4%25B9%258B%25E8%25B0%259C&is_only_read=1'

# 广州
# body = '__biz=MjM5ODQ0NTk1Mg%3D%3D&appmsg_type=9&mid=2650806545&sn=82851f004d9271e50e14481b3280fa4c&idx=1&scene=38&title=%25E5%258D%258E%25E5%25B8%2588%25E5%2586%258D%25E7%258E%25B0%25E6%259A%25B4%25E9%259C%25B2%25E5%258F%2598%25E6%2580%2581%25E7%258B%2582%25EF%25BC%259F%25EF%25BC%2581%25E4%25B8%2580%25E5%2591%25A8%25E4%25B8%25A4%25E4%25B8%25AA%25EF%25BC%2581%25E9%25AB%2598%25E6%25A0%25A1%25E5%25AD%25A6%25E7%2594%259F%25E5%25AE%2589%25E5%2585%25A8%25E9%259A%2590%25E6%2582%25A3%25E4%25B8%258D%25E5%25AE%25B9%25E5%25B0%258F%25E8%25A7%2586%25EF%25BC%2581&is_only_read=1'

# body = '__biz=MzA4MjEyNTA5Mw%3D%3D&mid=2652567942&sn=0224d013b004ca9f84a316b210a5fc41&idx=1&title=%25E6%2592%25A4%25E5%259B%259E%25E7%259A%2584%25E5%25BE%25AE%25E4%25BF%25A1%25E6%25B6%2588%25E6%2581%25AF%25E7%259C%259F%25E7%259A%2584%25E7%259C%258B%25E4%25B8%258D%25E5%2588%25B0%25EF%25BC%259F78%2520%25E8%25A1%258C%2520Python%2520%25E4%25BB%25A3%25E7%25A0%2581%25E5%25B8%25AE%25E4%25BD%25A0%25E7%259C%258B%25E7%25A9%25BF%25E4%25B8%2580%25E5%2588%2587%25EF%25BC%2581&is_only_read=1'
# body = '__biz=MzI1MzUzNTc0NQ%3D%3D&mid=2247486142&sn=3a02c35e464739ec8896311b55d1ecf8&idx=1&title=%25E8%25BF%2599%25E5%258F%25AF%25E8%2583%25BD%25E6%2598%25AF%25E5%258F%25B2%25E4%25B8%258A%25E6%259C%2580%25E5%2585%25A8%25E7%259A%2584%25E9%25AB%2598%25E6%2595%2588%25E8%25AE%25B0%25E5%25BF%2586%25E6%25B8%2585%25E5%258D%2595&ct=1530665758&abtest_cookie=BAABAAoACwAMABIACgA%2Bix4A44seAEKPHgBllR4AgJUeAPCVHgA4lh4AnZYeALWWHgD6lh4AAAA%3D&devicetype=android-26&is_only_read=1'
# body = '__biz=MjM5MTI2MTI0MA%3D%3D&mid=2655142621&sn=0cff41bfded789b513ee89a7e829a3d0&idx=1&title=6471%25E5%2585%2583%252F%25E3%258E%25A1%25EF%25BC%2581%25E5%258D%2597%25E6%25B5%25B7%25E9%25B8%25BF%25E6%2599%25965.6%25E4%25BA%25BF%25E7%25AB%259E%25E5%25BE%2597%25E4%25B8%2589%25E6%25B0%25B4%25E5%258C%2597%25E6%25B1%259F%25E6%2596%25B0%25E5%258C%25BA2.7%25E4%25B8%2587%25E3%258E%25A1%25E9%259D%2593%25E5%259C%25B0%2520%25E5%2591%25A8%25E8%25BE%25B9%25E5%258D%25961-1.3%25E4%25B8%2587%252F%25E5%25B9%25B3&is_only_read=1'
#
# # 7-6
# body = '__biz=MjM5MTI2MTI0MA%3D%3D&mid=2655142654&sn=1c78ae506bdc7f93038e2e5e102c3dd5&idx=1&title=%25E5%25BC%25A0%25E6%25A7%258E%25E4%25B8%25AD%25E5%25BF%2583%25E6%259E%25A2%25E7%25BA%25BD%25E7%25AB%2599%25E5%25BC%2580%25E6%258C%2582%25E4%25BA%2586%25EF%25BC%259A1%25E6%259D%25A1%25E5%259F%258E%25E8%25BD%25A8%252B5%25E6%259D%25A1%25E5%259C%25B0%25E9%2593%2581%25E4%25BA%25A4%25E6%25B1%2587%25EF%25BC%2581%25E5%2591%25A8%25E8%25BE%25B9%25E6%2588%25BF%25E4%25BB%25B7%25E8%25BF%2598%25E6%2598%25AF%25E4%25B8%2587%25E5%2585%2583%25E8%25B5%25B7%25E6%25AD%25A5...&is_only_read=1'
# body= '__biz=MzIzMjM4OTI1NA==&mid=2247491173&idx=2&sn=d0679daf6792f7dd8deb34701c2845af&is_only_read=17&title=%25E6%25B3%25A8%25E6%2584%258F%2520%257C%2520%25E6%259A%25B4%25E9%259B%25A8%25E5%25B7%25B2%25E5%258F%2591%25E8%25B4%25A7%25EF%25BC%2581%25E6%25B1%259F%25E8%258B%258F%25E8%25BF%2599%25E4%25BA%259B%25E5%259C%25B0%25E6%2596%25B9%25E8%25AF%25B7%25E6%25B3%25A8%25E6%2584%258F%25E6%259F%25A5%25E6%2594%25B6%25EF%25BC%2581'

body = 'r=0.7522563056214981&__biz=MzIzMjM4OTI1NA%3D%3D&appmsg_type=9&mid=2247491173&sn=d0679daf6792f7dd8deb34701c2845af&idx=2&scene=126&title=%25E6%25B3%25A8%25E6%2584%258F%2520%257C%2520%25E6%259A%25B4%25E9%259B%25A8%25E5%25B7%25B2%25E5%258F%2591%25E8%25B4%25A7%25EF%25BC%2581%25E6%25B1%259F%25E8%258B%258F%25E8%25BF%2599%25E4%25BA%259B%25E5%259C%25B0%25E6%2596%25B9%25E8%25AF%25B7%25E6%25B3%25A8%25E6%2584%258F%25E6%259F%25A5%25E6%2594%25B6%25EF%25BC%2581&ct=1530778334&abtest_cookie=BAABAAoACwAMABIACAA%2Bix4AQo8eAGWVHgDwlR4AnZYeALWWHgD6lh4AI5ceAAAA&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=355443170122776576&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0614DRoH1SaTN68PfGhBlkG4&pass_ticket=RL8TANw3a2uzGuzxpTGq%25252Fv9ttSNlfhd3Z7C9YYjVarP3ciiyDXggESx5mx63k2%25252Bh&is_temp_url=0&item_show_type=undefined&tmp_version=1'
# body = 'r=0.8374592525355444&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142654&sn=1c78ae506bdc7f93038e2e5e102c3dd5&idx=1&scene=0&title=%25E5%25BC%25A0%25E6%25A7%258E%25E4%25B8%25AD%25E5%25BF%2583%25E6%259E%25A2%25E7%25BA%25BD%25E7%25AB%2599%25E5%25BC%2580%25E6%258C%2582%25E4%25BA%2586%25EF%25BC%259A1%25E6%259D%25A1%25E5%259F%258E%25E8%25BD%25A8%252B5%25E6%259D%25A1%25E5%259C%25B0%25E9%2593%2581%25E4%25BA%25A4%25E6%25B1%2587%25EF%25BC%2581%25E5%2591%25A8%25E8%25BE%25B9%25E6%2588%25BF%25E4%25BB%25B7%25E8%25BF%2598%25E6%2598%25AF%25E4%25B8%2587%25E5%2585%2583%25E8%25B5%25B7%25E6%25AD%25A5...&ct=1530787738&abtest_cookie=BAABAAoACwAMABIACAA%2Bix4AQo8eAGWVHgDwlR4AnZYeALWWHgD6lh4AI5ceAAAA&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=355600939958173696&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=06143vQvezjCviD202v8BmY7&pass_ticket=RL8TANw3a2uzGuzxpTGq%25252Fv9ttSNlfhd3Z7C9YYjVarP3ciiyDXggESx5mx63k2%25252Bh&is_temp_url=0&item_show_type=undefined&tmp_version=1'
resp = requests.post(url, headers=headers, data=body)
print(resp.status_code)
print(resp.text, type(resp.text))
# with open("resp.txt", 'w', encoding='utf-8') as f:
#     f.write(resp.text)

# {"advertisement_num": 0, "advertisement_info": [],
#  "appmsgstat": {"show": true, "is_login": true, "liked": false, "read_num": 9267, "like_num": 14, "ret": 0,
#                 "real_read_num": 0}, "comment_enabled": 1, "reward_head_imgs": [], "only_fans_can_comment": false,
#  "comment_count": 11, "is_fans": 1, "nick_name": "Zy",
#  "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/FU5rrZrUEmfVdmshOZNraHzV8sVKl1xoGgn4a3lKErmibVbon5Eicb8dybUOzDxJDsVWkEG1XWH5bWnrBdJbaXwiaGZUEIAia4J7\/132",
#  "friend_comment_enabled": 1, "base_resp": {"wxtoken": 777}}
