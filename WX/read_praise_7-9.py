import requests
url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_VX3ULmeqWY8Mdcea0B4ZM_5e7dIjaR3hIaoO-toVsMHudsNa_j5vYMVVh4usdkCtQF9sffysMzAtq2fE'
url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_023kkPvBzbt3c%2BHlx9PDfAaUHXTOPQ2WLvWtqnOzvzimGoXs743kD2LzaU70o-sUOeWo3zXfvKfGh6pU'
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=&wxtoken=777&devicetype=Windows10&clientversion=6206034e&appmsg_token=964_023kkPvBzbt3c%252BHlx9PDfAaUHXTOPQ2WLvWtqnOzvzimGoXs743kD2LzaU70o-sUOeWo3zXfvKfGh6pU&x5=0&f=json'

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',

    'Cookie': 'wap_sid2=CO/i6a8HElxiUEdGZFpac2U2U01wcVF0QVZsR0lIZUt5VDA1ZXg4VlVZemFJVHJhRjRzbWFhM3VwQmJmWldNVV9Va002em43eERvVks1RXFod3I1VTJhS2FmckxXc1FEQUFBfjDxrovaBTgNQAE=; wxtokenkey=777',

}
body = '__biz=MzA4MzQ1ODcwMA%3D%3D&mid=2652022824&sn=e6081e0ce24730d033900d87b9a7e54a&idx=1&title=HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F&is_only_read=1'
# resp = requests.post(url, headers=headers, data=body)
#
# print(resp.text)
#
url = 'https://mp.weixin.qq.com/mp/getappmsgext?appmsg_token=964_023kkPvBzbt3c%2BHlx9PDfAaUHXTOPQ2WLvWtqnOzvzimGoXs743kD2LzaU70o-sUOeWo3zXfvKfGh6pU'
# url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=&wxtoken=777&devicetype=Windows10&clientversion=6206034e&appmsg_token=964_j0exUvIkeR%252Bxt0z6qOux2361Q3cvjZI2QdK7-COU78DO-3bt2RZg_yCfXivcypU-lDwh3qjJqmvACkuQ&x5=0&f=json'

# headers = {
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
#
#     # 'Cookie': 'wap_sid2=CM3c1KcEElx4UkVwd01LSkVpRG43cGkyRWllQU43cnQzVC0wVHg2ZmVhaktnYklrdU1wYk9LNTVDbWhLOVFZNmFPTXotbzJ5QzFXMlYyOWNhWDFRQ0JtUUJudGJwOFFEQUFBfjDVgIzaBTgNQJVO',
#     # 'Cookie': 'wap_sid2=CO/i6a8HElxiUEdGZFpac2U2U01wcVF0QVZsR0lIZUt5VDA1ZXg4VlVZemFJVHJhRjRzbWFhM3VwQmJmWldNVV9Va002em43eERvVks1RXFod3I1VTJhS2FmckxXc1FEQUFBfjDxrovaBTgNQAE=',
#     # 'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=Emjbw5j0EcMmuH0PbJ6XMzvm0Nupy+h2cIV+qSqXQwvRpQmcRt/locItf6i3aVeb; wap_sid2=CM3c1KcEElx4UkVwd01LSkVpRG43cGkyRWllQU43cnQzVC0wVHg2ZmVhaktnYklrdU1wYk9LNTVDbWhLOVFZNmFPTXotbzJ5QzFXMlYyOWNhWDFRQ0JtUUJudGJwOFFEQUFBfjDVgIzaBTgNQJVO; rewardsn=; wxtokenkey=777',
#     'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=Emjbw5j0EcMmuH0PbJ6XMzvm0Nupy+h2cIV+qSqXQwvRpQmcRt/locItf6i3aVeb; rewardsn=; wxtokenkey=777; wap_sid2=CM3c1KcEElxvS250ZndKYjduUWZ4aE52RFdZYUMyLWd4N0tLb2lYT2VaWmNDbnBhM2xWTHJhbjNnTEZIYV9rZk5ka1JsV2xmUEdSTnBxT3ltWFJ6UnNFbzhpZGVTY1FEQUFBfjDdyozaBTgNQJVO',
#
#
#
# }
# body = '__biz=MjM5MTI2MTI0MA%3D%3D&mid=2655142727&sn=c5660969bffbb4d457ab20c1afc0477e&idx=1&title=%25E9%25AB%2598%25E4%25BB%25B7%25E5%259C%25B0%25E6%2589%258E%25E5%25A0%2586%25E5%25BE%2585%25E5%2585%25A5%25E5%25B8%2582%25EF%25BC%2581%25E4%25B8%258B%25E5%258D%258A%25E5%25B9%25B4%25E4%25BD%259B%25E5%25B1%25B176%25E4%25B8%25AA%25E6%2596%25B0%25E7%259B%2598%25E6%259B%259D%25E5%2585%2589%25EF%25BC%258C%25E5%2585%25A5%25E6%2589%258B%25E5%2589%258D%25E5%25BF%2585%25E7%259C%258B...&is_only_read=1'
# body='r=0.8824220742098987&__biz=MzA4MzQ1ODcwMA%3D%3D&appmsg_type=9&mid=2652022824&sn=e6081e0ce24730d033900d87b9a7e54a&idx=1&scene=38&title=HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F&ct=1530678251&abtest_cookie=&devicetype=android-19&version=26060532&is_need_ticket=0&is_need_ad=1&comment_id=353764053111308295&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0911UFRffQFHQtKGVMXqmYK8&pass_ticket=iSR4uBuHoRw0mTnUpACxqgWxbLamZxEJ%25252BlEbO%25252FDP68nnh1DNi7htRpxv8SHH994O&is_temp_url=0&item_show_type=undefined&tmp_version=1'
# body = 'r=0.17272295762831358&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142713&sn=09d64bdb54be176f0bbdba784f136c77&idx=5&scene=38&title=2924%25E5%2585%2583%252F%25E3%258E%25A1%25E8%25B5%25B7%25E6%258B%258D%25EF%25BC%2581%25E5%25A4%25A7%25E6%25B2%25A5%25E6%258C%2582%25E7%2589%258C3771%25E3%258E%25A1%25E2%2580%259C%25E8%259A%258A%25E5%259E%258B%25E2%2580%259D%25E5%2595%2586%25E6%259C%258D%25E5%259C%25B0&ct=1530961639&abtest_cookie=&devicetype=Windows10&version=6206034e&is_need_ticket=0&is_need_ad=0&comment_id=358518510403485699&is_need_reward=1&both_ad=0&reward_uin_count=21&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0916xahm8TCyb7cClpZieyhp&pass_ticket=&is_temp_url=0&item_show_type=undefined&tmp_version=1'
# body = 'r=0.8894111189713811&__biz=MjM5Nzg2MDM0OQ%3D%3D&appmsg_type=9&mid=2651709115&sn=1ace1b9ec4ffc8f54d17a429f06abc8d&idx=1&scene=38&title=%25E5%2586%258D%25E6%259D%25A5%25E7%2582%25B9%25E9%25AA%259A%25E8%25AF%259D&ct=1531060730&abtest_cookie=&devicetype=Windows10&version=6206034e&is_need_ticket=0&is_need_ad=0&comment_id=360180975759654912&is_need_reward=1&both_ad=0&reward_uin_count=21&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0917cU217uqm4P9YOYjuyLBZ&pass_ticket=&is_temp_url=0&item_show_type=undefined&tmp_version=1'
resp = requests.post(url, headers=headers, data=body)

print(resp.text)
