import requests

# 文章url  title： 16大重点项目曝光...
# https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142500&idx=1&sn=77fbb51f69117d7b573e17928f1a26ce&chksm=bd0ed5338a795c252d9f33b3cb267ef2554ed83e4373207c013d1da02401f5836765d45bbcba&scene=0&ascene=7&devicetype=android-26&version=26060739&nettype=WIFI&abtest_cookie=BAABAAoACwAMABIACQA%2Bix4A44seAEKPHgBllR4AepUeAICVHgDwlR4AOJYeAECWHgAAAA%3D%3D&lang=zh_CN&pass_ticket=OkFDOiNd7psMLd3HldZ6Kn1ywxmBqa9tVPH5FNCSuqgiovE9Yh7q383n4MGAZp0C&wx_header=1

# 阅读， 点赞url
# token 不一样
# # 7-4 精简版
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=963_%252BwsoPU9E%252FCxhLtOzLCninA0nfnHTIAhlWLDHeE47zI4jnl2CcjaMSDXwghkq5ENUCphcSiQYs_X299b5'
#
#
# # 7-6
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_Ckc4nrE%252BKFESCo8tb8Uc5MV3IDkHYPXSkMbkb0HNB8fqAaTT_IBJeWk42VYluDuWWxLUEXdvOSbyWTvq'
#
url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_lDSn8DoRqyCzqkc0sGAjnKF7BcfSO6AdzU6gBh76NQAzdnBnKKIY6NT1W5fxYmgRKMJCriqEDfctPibh'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
    # 7-4 精简版
    # 'Cookie': 'wap_sid2=CM3c1KcEElxBLTIzc1N6ZWNPd3hBRUdRUzFqLXp1TUdPa2FrT1hhQkNscHI4ZS1YaTRqQmw1Wk5PMERROTFjUVJaTTJORlgtU0VqRDY4MEJOSUtmRk9TOTJjQ3RrY1FEQUFBfjDPgPvZBTgNQAE='

    "Cookie": "wap_sid2=CM3c1KcEElxHbUtVbGpCaktLMDRmaVNiSHhZOEg0UkpGdmRYQjctX3ZDUlVEd0NPdElQQmFDN3p2VEQwb09fc2o5SDJ0STJiSDZKMFpLUUhNeUpWX1VrYUxFdGtwOFFEQUFBfjCylfzZBTgNQAE="
}


body = 'r=0.7522563056214981&__biz=MzIzMjM4OTI1NA%3D%3D&appmsg_type=9&mid=2247491173&sn=d0679daf6792f7dd8deb34701c2845af&idx=2&scene=126&title=%25E6%25B3%25A8%25E6%2584%258F%2520%257C%2520%25E6%259A%25B4%25E9%259B%25A8%25E5%25B7%25B2%25E5%258F%2591%25E8%25B4%25A7%25EF%25BC%2581%25E6%25B1%259F%25E8%258B%258F%25E8%25BF%2599%25E4%25BA%259B%25E5%259C%25B0%25E6%2596%25B9%25E8%25AF%25B7%25E6%25B3%25A8%25E6%2584%258F%25E6%259F%25A5%25E6%2594%25B6%25EF%25BC%2581&ct=1530778334&abtest_cookie=BAABAAoACwAMABIACAA%2Bix4AQo8eAGWVHgDwlR4AnZYeALWWHgD6lh4AI5ceAAAA&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=355443170122776576&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0614DRoH1SaTN68PfGhBlkG4&pass_ticket=RL8TANw3a2uzGuzxpTGq%25252Fv9ttSNlfhd3Z7C9YYjVarP3ciiyDXggESx5mx63k2%25252Bh&is_temp_url=0&item_show_type=undefined&tmp_version=1'
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
