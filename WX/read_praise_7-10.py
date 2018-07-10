import requests

url = 'https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=&wxtoken=777&devicetype=Windows10&clientversion=6206034e&appmsg_token=964_BDgLTndnIplMJjH6_45re_j6SJT035R_3UXydF7jeqaWyt7hkiXCfjQI-rXDGqaSzaUJuBZOVvZvFIWp&x5=0&f=json'
url = 'https://mp.weixin.qq.com/mp/getappmsgext?uin=MTE1NjkxODg2MQ%253D%253D&key=9971a8088dcd256b45024091673ea487b92f44c48ce59a094176db8180faa68880fa10b3c10204c01a1fd4943247820ab1f812d78d70ca904e68a27e982eac5de4bb634b05323f6d23f689ed47964b8a&pass_ticket=feqjm7ppkTXA2TQ3%25252Fj9OItlQ5GGKP8fyj00ASzbR6AlQp30X%25252F1qkGmaYOrFtriEr&wxtoken=777&devicetype=Windows%26nbsp%3B10&clientversion=6206034e&appmsg_token=964_tRT6XOaMhP98239thIFA5GzIax9cS3HjLPOCvCPa4EYF0iVbA4lg1T0n9ykqACeyrq6MIZ6e8sBgDPuE&x5=0&f=json'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=feqjm7ppkTXA2TQ3/j9OItlQ5GGKP8fyj00ASzbR6AlQp30X/1qkGmaYOrFtriEr; wap_sid2=CM3c1KcEElxwVzIwYllIS2ZyS3dnMlNXdnV6OGY1ZE5GYldsWkVvRTNPZXRBYkdRdzdENFNTY0ZBMDlmQkE1M3dQaDFYXzlNVTlkRGFBVVA3VkpRVV9uUjM3VGFrTVFEQUFBfjCsoZDaBTgNQJVO; rewardsn=; wxtokenkey=777',
}


body = 'r=0.5108980467915514&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142733&sn=3cf23ca5c181ea5d35e95ffddd436a39&idx=1&scene=38&ct=1531134171&abtest_cookie=&devicetype=Windows10&version=6206034e&is_need_ticket=0&is_need_ad=0&comment_id=361413112454217728&is_need_reward=1&both_ad=0&reward_uin_count=21&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=1009mo3dDoIjUDFzoKzG8yIs&pass_ticket=&is_temp_url=0&item_show_type=undefined&tmp_version=1'

body = '__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142733&sn=3cf23ca5c181ea5d35e95ffddd436a39&idx=1title=%25E4%25B8%2580%25E5%259B%25BE%25E7%259C%258B%25E6%2587%2582%25E9%2599%2590%25E8%25B4%25AD%25E4%25B8%258B%25E7%259A%2584%25E4%25BD%259B%25E5%25B1%25B1%25E6%2588%25BF%25E4%25BB%25B7%25E3%2580%2581%25E5%259C%25B0%25E4%25BB%25B7%25EF%25BC%258C%25E4%25B8%2587%25E5%2585%2583%25E4%25BB%25A5%25E4%25B8%258B%25E7%259A%2584%25E9%2583%25BD%25E4%25B8%258D%25E5%25A4%259A%25E4%25BA%2586%25E2%2580%25A6%25E2%2580%25A6&is_only_read=1'
# title = 'HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F'
#
# body = '__biz=MjM5NzAwNjQyMA%3D%3D&mid=2650849884&idx=1&sn=2c74884f44e7a61e6981599bcd1144f6&is_only_read=1&title={}'.format(title)
body = 'r=0.5323953470777887&__biz=MjM5NzAwNjQyMA%3D%3D&appmsg_type=9&mid=2650849884&sn=2c74884f44e7a61e6981599bcd1144f6&idx=1&scene=38&title=HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F&ct=1530686651&abtest_cookie=&devicetype=Windows%2010&version=6206034e&is_need_ticket=0&is_need_ad=0&comment_id=353904981944107009&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=1010BEGjhsKrGgPLe3Ymwqq5&pass_ticket=feqjm7ppkTXA2TQ3%25252Fj9OItlQ5GGKP8fyj00ASzbR6AlQp30X%25252F1qkGmaYOrFtriEr&is_temp_url=0&item_show_type=undefined&tmp_version=1'
resp = requests.post(url, headers=headers, data=body)

print(resp.text)
