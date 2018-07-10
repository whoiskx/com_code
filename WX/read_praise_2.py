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

# # 点赞阅读
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_lDSn8DoRqyCzqkc0sGAjnKF7BcfSO6AdzU6gBh76NQAzdnBnKKIY6NT1W5fxYmgRKMJCriqEDfctPibh'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
#     # 7-4 精简版
#     # 'Cookie': 'wap_sid2=CM3c1KcEElxBLTIzc1N6ZWNPd3hBRUdRUzFqLXp1TUdPa2FrT1hhQkNscHI4ZS1YaTRqQmw1Wk5PMERROTFjUVJaTTJORlgtU0VqRDY4MEJOSUtmRk9TOTJjQ3RrY1FEQUFBfjDPgPvZBTgNQAE='
#
#     "Cookie": "wap_sid2=CM3c1KcEElxHbUtVbGpCaktLMDRmaVNiSHhZOEg0UkpGdmRYQjctX3ZDUlVEd0NPdElQQmFDN3p2VEQwb09fc2o5SDJ0STJiSDZKMFpLUUhNeUpWX1VrYUxFdGtwOFFEQUFBfjCylfzZBTgNQAE="
# }
#
#
# body = 'r=0.7522563056214981&__biz=MzIzMjM4OTI1NA%3D%3D&appmsg_type=9&mid=2247491173&sn=d0679daf6792f7dd8deb34701c2845af&idx=2&scene=126&title=%25E6%25B3%25A8%25E6%2584%258F%2520%257C%2520%25E6%259A%25B4%25E9%259B%25A8%25E5%25B7%25B2%25E5%258F%2591%25E8%25B4%25A7%25EF%25BC%2581%25E6%25B1%259F%25E8%258B%258F%25E8%25BF%2599%25E4%25BA%259B%25E5%259C%25B0%25E6%2596%25B9%25E8%25AF%25B7%25E6%25B3%25A8%25E6%2584%258F%25E6%259F%25A5%25E6%2594%25B6%25EF%25BC%2581&ct=1530778334&abtest_cookie=BAABAAoACwAMABIACAA%2Bix4AQo8eAGWVHgDwlR4AnZYeALWWHgD6lh4AI5ceAAAA&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=355443170122776576&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0614DRoH1SaTN68PfGhBlkG4&pass_ticket=RL8TANw3a2uzGuzxpTGq%25252Fv9ttSNlfhd3Z7C9YYjVarP3ciiyDXggESx5mx63k2%25252Bh&is_temp_url=0&item_show_type=undefined&tmp_version=1'
# resp = requests.post(url, headers=headers, data=body)
# print(resp.status_code)
# print(resp.text, type(resp.text))


# with open("resp.txt", 'w', encoding='utf-8') as f:
#     f.write(resp.text)

# {"advertisement_num": 0, "advertisement_info": [],
#  "appmsgstat": {"show": true, "is_login": true, "liked": false, "read_num": 9267, "like_num": 14, "ret": 0,
#                 "real_read_num": 0}, "comment_enabled": 1, "reward_head_imgs": [], "only_fans_can_comment": false,
#  "comment_count": 11, "is_fans": 1, "nick_name": "Zy",
#  "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/FU5rrZrUEmfVdmshOZNraHzV8sVKl1xoGgn4a3lKErmibVbon5Eicb8dybUOzDxJDsVWkEG1XWH5bWnrBdJbaXwiaGZUEIAia4J7\/132",
#  "friend_comment_enabled": 1, "base_resp": {"wxtoken": 777}}


url = 'https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142727&idx=1&sn=c5660969bffbb4d457ab20c1afc0477e&chksm=bd0ed4108a795d06397791a9c29d1e49ab174b1a1079e56ab187b611a8d8ffacc3168c2c160b&scene=38#wechat_redirect'
url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=&wxtoken=777&devicetype=Windows10&clientversion=6206034e&appmsg_token=964_rPjB%252F8VIsCoD9s1rb3p6o6yge9un4MU29wHptKttecXFPgEFZY1mssSnTIdpy3RKI37Dnmct58zwcckw&x5=0&f=json'
headers = {
    'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=0QQd74P4gWVbFP0gnug/0bqx6VcpYJxz++oBuoL5PxG+afchlU8FCnxqsL4Qp4yG; rewardsn=; wxtokenkey=777; wap_sid2=CM3c1KcEElx1VU9rMXVSWEZ5Ukd0Z3dLRjlMeDJ5eG1xbnVJeHZFa25xZU5NY2VVME8yaDFLRUFPQ3lpMFg0TTN1N0dseERnOFpwNzVLS05TT3hKWFFkN1hxMGRoY1FEQUFBfjCS9IraBTgNQJVO',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',

}
body = 'r=0.5466906942840168&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142713&sn=15e63b88471042f179f22ec8ed2bd2c9&idx=3&scene=38&title=3917%25E5%2585%2583%252F%25E3%258E%25A1%25E8%25B5%25B7%25E6%258B%258D%25EF%25BC%2581%25E7%259F%25B3%25E6%25B9%25BE%25E9%2580%25BE3%25E4%25B8%2587%25E3%258E%25A1%25E9%259D%2593%25E5%259C%25B0%25E6%258C%2582%25E7%2589%258C%2520%25E8%25B7%259D%25E7%25A6%25BB%25E5%259C%25B0%25E9%2593%2581%25E7%25AB%2599500%25E7%25B1%25B3&ct=1530961639&abtest_cookie=&devicetype=Windows10&version=6206034e&is_need_ticket=0&is_need_ad=0&comment_id=358518509531070466&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=09102s62HSlwykFKiTB9ZNGs&pass_ticket=&is_temp_url=0&item_show_type=undefined&tmp_version=1'


# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=iSR4uBuHoRw0mTnUpACxqgWxbLamZxEJ%25252BlEbO%25252FDP68nnh1DNi7htRpxv8SHH994O&wxtoken=777&devicetype=android-19&clientversion=26060532&appmsg_token=964_VX3ULmeqWY8Mdcea0B4ZM_5e7dIjaR3hIaoO-toVsMHudsNa_j5vYMVVh4usdkCtQF9sffysMzAtq2fE&x5=0&f=json'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=0QQd74P4gWVbFP0gnug/0bqx6VcpYJxz++oBuoL5PxG+afchlU8FCnxqsL4Qp4yG; rewardsn=; wxtokenkey=777; wap_sid2=CM3c1KcEElx1VU9rMXVSWEZ5Ukd0Z3dLRjlMeDJ5eG1xbnVJeHZFa25xZU5NY2VVME8yaDFLRUFPQ3lpMFg0TTN1N0dseERnOFpwNzVLS05TT3hKWFFkN1hxMGRoY1FEQUFBfjCS9IraBTgNQJVO'
}
# body = 'r=0.5466906942840168&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142713&sn=15e63b88471042f179f22ec8ed2bd2c9&idx=3&scene=38&title=3917%25E5%2585%2583%252F%25E3%258E%25A1%25E8%25B5%25B7%25E6%258B%258D%25EF%25BC%2581%25E7%259F%25B3%25E6%25B9%25BE%25E9%2580%25BE3%25E4%25B8%2587%25E3%258E%25A1%25E9%259D%2593%25E5%259C%25B0%25E6%258C%2582%25E7%2589%258C%2520%25E8%25B7%259D%25E7%25A6%25BB%25E5%259C%25B0%25E9%2593%2581%25E7%25AB%2599500%25E7%25B1%25B3&ct=1530961639&abtest_cookie=&devicetype=Windows10&version=6206034e&is_need_ticket=0&is_need_ad=0&comment_id=358518509531070466&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=09102s62HSlwykFKiTB9ZNGs&pass_ticket=&is_temp_url=0&item_show_type=undefined&tmp_version=1'
body = 'r=0.8824220742098987&__biz=MzA4MzQ1ODcwMA%3D%3D&appmsg_type=9&mid=2652022824&sn=e6081e0ce24730d033900d87b9a7e54a&idx=1&scene=38&title=HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F&ct=1530678251&abtest_cookie=&devicetype=android-19&version=26060532&is_need_ticket=0&is_need_ad=1&comment_id=353764053111308295&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0911UFRffQFHQtKGVMXqmYK8&pass_ticket=iSR4uBuHoRw0mTnUpACxqgWxbLamZxEJ%25252BlEbO%25252FDP68nnh1DNi7htRpxv8SHH994O&is_temp_url=0&item_show_type=undefined&tmp_version=1'

body = '__biz=MzA4MzQ1ODcwMA%3D%3D&mid=2652022824&sn=e6081e0ce24730d033900d87b9a7e54a&idx=1&title=HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F&is_only_read=1'




url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=iSR4uBuHoRw0mTnUpACxqgWxbLamZxEJ%25252BlEbO%25252FDP68nnh1DNi7htRpxv8SHH994O&wxtoken=777&devicetype=android-19&clientversion=26060532&appmsg_token=964_VX3ULmeqWY8Mdcea0B4ZM_5e7dIjaR3hIaoO-toVsMHudsNa_j5vYMVVh4usdkCtQF9sffysMzAtq2fE&x5=0&f=json'

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': "rewardsn=; wxuin=1979347311; devicetype=android-19; version=26060532; lang=zh_CN; pass_ticket=iSR4uBuHoRw0mTnUpACxqgWxbLamZxEJ+lEbO/DP68nnh1DNi7htRpxv8SHH994O; wap_sid2=CO/i6a8HElxiUEdGZFpac2U2U01wcVF0QVZsR0lIZUt5VDA1ZXg4VlVZemFJVHJhRjRzbWFhM3VwQmJmWldNVV9Va002em43eERvVks1RXFod3I1VTJhS2FmckxXc1FEQUFBfjDxrovaBTgNQAE=; wxtokenkey=777"
}

body = '__biz=MzA4MzQ1ODcwMA%3D%3D&appmsg_type=9&mid=2652022824&sn=e6081e0ce24730d033900d87b9a7e54a&idx=1&scene=38&title=HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F&ct=1530678251&abtest_cookie=&devicetype=android-19&version=26060532&is_need_ticket=0&is_need_ad=1&comment_id=353764053111308295&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0911UFRffQFHQtKGVMXqmYK8&pass_ticket=iSR4uBuHoRw0mTnUpACxqgWxbLamZxEJ%25252BlEbO%25252FDP68nnh1DNi7htRpxv8SHH994O&is_temp_url=0&item_show_type=undefined&tmp_version=1'
body = '__biz=MzIzMjM4OTI1NA==&mid=2247491173&idx=2&sn=d0679daf6792f7dd8deb34701c2845af&is_only_read=17&title=%2520%25E6%25B3%25A8%25E6%2584%258F%2520%257C%2520%25E6%259A%25B4%25E9%259B%25A8%25E5%25B7%25B2%25E5%258F%2591%25E8%25B4%25A7%25EF%25BC%2581%25E6%25B1%259F%25E8%258B%258F%25E8%25BF%2599%25E4%25BA%259B%25E5%259C%25B0%25E6%2596%25B9%25E8%25AF%25B7%25E6%25B3%25A8%25E6%2584%258F%25E6%259F%25A5%25E6%2594%25B6%25EF%25BC%2581'
resp = requests.post(url, headers=headers, data=body)
print(resp.text)
with open('praise.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)
