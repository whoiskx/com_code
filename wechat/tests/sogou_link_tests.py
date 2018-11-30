# -*- coding: utf-8 -*-

#
# def main():
#     url = 'mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MjAxNDM4MA==&f=json&offset=19&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=7%2BvwD%2BWPwnX3d72h5qphboLfNyySTbgywgtCJzXjCEVoyqZHjXlPTt6ZGobc9Rw9&wxtoken=&appmsg_token=978_nm2EiPgLT97nD6iBPEuOpGikQxH296kcLED_bg~~&x5=1&f=json '
#
#
# if __name__ == '__main__':
#     main()
import json

import requests

# url = 'https://api.shenjian.io/?appid=0add495ae0f872a8835885e318129b27'
# params = {
#     'url':'https://mp.weixin.qq.com/s?src=11&timestamp=1539768806&ver=1188&signature=2x8XpPlGqQtx5lfP9q9ziZjV7sneRuCWbUcj4XpY1J9w7OVmo3S8eGa-F-ycJL1y-XBKfT5lWhYEEqOvk-TCrm8MBJs*pQAt54AH-nE8FyPGdnsi5o*7V9jmQj-mBASK&new=1',
#     'account':'gh_dedca6e20f16',
# }
# r = requests.get(url, params=params)
# print(r.status_code)
# print(r.text)

# # result = 'http:\/\/mp.weixin.qq.com\/s?__biz=MzA4NjY4MzkxNw==&mid=2652946868&idx=8&sn=d4be06a9eb34c6944fa22a538cda1a30&scene=0#wechat_redirect'
#
# result = '{"error_code":0,"data":{"article_origin_url":"http:\/\/mp.weixin.qq.com\/s?__biz=MzA4NjY4MzkxNw==&mid=2652946868&idx=8&sn=d4be06a9eb34c6944fa22a538cda1a30&scene=0#wechat_redirect"},"reason":"success"}'
# result_dict = json.loads(result)
# print(result_dict)
# proxies = {"https": "http://localhost:1080", }
# r = requests.get('https://www.facebook.com/chcsscg/about/?ref=page_internal', proxies=proxies)
# print(r.status_code)
# print(r.text)
# with open('tt.html', 'w', encoding='utf-8') as f:
#     f.write(r.text)

url = 'http://219.234.5.17:521/bizapi/getgurl'  #?username={}&password={}&biz={}&url={}'.format('test1', 'test443', 'MzA4NDI3NjcyNA==', 'https://mp.weixin.qq.com/s?timestamp=1539827127&src=3&ver=1&signature=z6IqAHh68MPes0DiExU5NZO5JdZ*K66T9ghbZNHDjVIkDa5xsJbkPlK5x0V97zqPRjJH3KzpUVwxwc2DJ5f-gCEJ5979qspXDozbXenZ4KGOmMA5VvxNqnhyf5VXR5T7psWn51jwTDYdautp4zod9WRo32pnTSrAQmhZPMvh9aE=')
print(url)
params = {
    'username': 'test1',
    'password': 'test443',
    'biz': 'MzU3MjQ1MjE1MA==',
    # 'url': 'https://mp.weixin.qq.com/s?timestamp=1539827127&src=3&ver=1&signature=z6IqAHh68MPes0DiExU5NZO5JdZ*K66T9ghbZNHDjVIkDa5xsJbkPlK5x0V97zqPRjJH3KzpUVwxwc2DJ5f-gCEJ5979qspXDozbXenZ4KGOmMA5VvxNqnhyf5VXR5T7psWn51jwTDYdautp4zod9WRo32pnTSrAQmhZPMvh9aE=',
    # 'url': 'https://mp.weixin.qq.com/s?src=11&timestamp=1539768806&ver=1188&signature=OI6tYxxr486M3eofRIcra1eExD9PT8YTJPXq9JXaLfOr8S49tp8Ky0FKcO0VV*EG5CMhoswD-uLzCcHKdzdPrH4ZIqOnpR74thKfnh-DgGx0zodJz3pu2Rwr033yVecA&new=1'
    'url': 'https://mp.weixin.qq.com/s?src=11&timestamp=1539768806&ver=1188&signature=XW3BdR2tZ4fORhunnMtTO3**DWLyJY-ulQmHrhuZLJZTFyCFp5NNdefvTWAP*RP2V6jw9GYUXZqcED*jo1bbcEoKTTnZHbXkGOD*Q8azS7dtwuXj8NRY8qHwB5oU0Ikn&new=1'
}
r = requests.get(url, params=params)
print(r.status_code)
print(r.text)
print(json.loads(r.text))# 54305267