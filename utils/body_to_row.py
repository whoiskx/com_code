def body_to_row(body=''):
    if '?' in body:
        body = body.split('?')[-1]
        # print(body)
    body_split = body.split('&')
    result = ""
    for r in body_split:
        result += r + '\n'

    print(result)
    return result


def headers_to_dict(headers=''):
    if headers == '':
        return ''
    items = headers.split("\n")
    # print(items)
    d = {}
    for item in items:
        k, v = item.split(": ", 1)
        d[k] = v.strip()
    print(d)
    return d


def main():
    # body_to_row(body)
    headers_to_dict(headers=headers)


if __name__ == '__main__':
    # body = 'r=0.7690273252447204&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142500&sn=77fbb51f69117d7b573e17928f1a26ce&idx=1&scene=0&title=16%25E5%25A4%25A7%25E9%2587%258D%25E7%2582%25B9%25E9%25A1%25B9%25E7%259B%25AE%25E6%259B%259D%25E5%2585%2589%25EF%25BC%2581%25E4%25BD%259B%25E5%25B1%25B1%25E4%25B8%2589%25E6%2597%25A7%25E6%2594%25B9%25E9%2580%25A0%25E5%25AE%25A3%25E4%25BC%25A0%25E5%25A4%25A7%25E7%2589%2587%25E5%2587%25BA%25E7%2582%2589&ct=1530443859&abtest_cookie=BAABAAoACwAMABIACgA%2Bix4A44seAEKPHgBllR4AepUeAICVHgDwlR4AOJYeAJ2WHgC1lh4AAAA%3D&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=349831597094109186&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=030920599jFyODX9v0PULyo0&pass_ticket=lmz4dXv%25252FWib0B0%25252B0lpXZZ8VPthtTPqPnjpwYcH6p5usaQBW%25252FdJNeVlTua%25252FCMp8Ki&is_temp_url=0&item_show_type=undefined&tmp_version=1'

    headers = '''User-Agent:Mozilla/5.0 (Linux; Android 6.0.1; MI 4LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/toolsmp
    action=home&__biz=MjM5MjAxNDM4MA==&scene=124&devicetype=android-23&version=26070333&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=7%2BvwD%2BWPwnX3d72h5qphboLfNyySTbgywgtCJzXjCEVoyqZHjXlPTt6ZGobc9Rw9&wx_header=1
    Accept-Encoding:gzip, deflate
    Accept-Language:zh-CN,en-US;q=0.8
    Cookie:rewardsn=; wxtokenkey=777; wxuin=2148728940; devicetype=android-23; version=26070333; lang=zh_CN; pass_ticket=7%2BvwD%2BWPwnX3d72h5qphboLfNyySTbgywgtCJzXjCEVoyqZHjXlPTt6ZGobc9Rw9; wap_sid2=COyAzIAIElxmNTdwY3BjSUYwcFFaV2pHOWE2VjJUb2VGZ1l2M2NoQ0FTVmJQLVBOeU1JakFYOHlVcFFRSEttMzFVOElFVHpBR195MnZfR0U0Ty1JbFJtVEFuSFh3OUlEQUFBfjDjoYHeBTgMQAo='''
    main()
