headers = """r=0.9039583323000335&__biz=MjM5MTI2MTI0MA%3D%3D&appmsg_type=9&mid=2655142299&sn=e3e403a47fe694a0ec71ab765d0b2043&idx=2&scene=126&title=%25E4%25B8%2580%25E5%2591%25A8%25E6%25A6%259C%25E5%258D%2595%25EF%25BC%259A%25E7%25A6%2585%25E5%259F%258E%25E5%25BC%25A0%25E6%25A7%258E%25E5%258D%2595%25E7%259B%2598%25E5%25BC%2582%25E5%2586%259B%25E7%25AA%2581%25E8%25B5%25B7%2520%25E4%25B8%2589%25E6%25B0%25B4%25E9%25AB%2598%25E6%2598%258E%25E7%258B%25AC%25E5%258D%25A0%25E6%25A6%259C%25E5%258D%25956%25E5%25B8%25AD&ct=1530008232&abtest_cookie=BAABAAoACwAMABIACQA9ix4A44seAEKPHgCzlB4A%2BZQeAGWVHgB6lR4AgJUeAPCVHgAAAA%3D%3D&devicetype=android-26&version=26060739&is_need_ticket=0&is_need_ad=1&comment_id=342523003080310784&is_need_reward=1&both_ad=0&reward_uin_count=18&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=2812znOYhwcKXd2gXkA4QdeX&pass_ticket=a6RM70vbT%25252F1puB8hBNui9DI31hoKz7BRZdIrL7SuUwv5IYX7H4wgITOG3QJKceCD&is_temp_url=0&item_show_type=undefined&tmp_version=1"""



items = headers.split("\n")
# print(items)
d = {}
for item in items:
    k, v = item.split(": ", 1)

    d[k] = v.strip()
print(d)
