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

    headers = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: no-cache
    Connection: keep-alive
    Cookie: SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; LSTMV=0%2C0; LCLKINT=235; SNUID=9A638690ABAEDE83070339C3ACDDE1AD; sct=179; PHPSESSID=qvdgtcif7omomgook8bb7vs8n2; SUIR=9A638690ABAEDE83070339C3ACDDE1AD; refresh=1
    Host: weixin.sogou.com
    Pragma: no-cache
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'''
    main()
