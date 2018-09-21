# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq


def main():
    count = 0
    while True:
        count += 1
        print(count)
        url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1537499719&ver=1135&signature=9U-2mdKf19P3qCVYU0qWmJSRYaUcFCfAN8QJ0p3aNhqq49Xxm6kNKF8wAsAF3msofeyTeJLgM4VDKZdQU0CwfxpgnCyvKRUg2YuI4zscftsT9CaggrX*fs0mpWoamRWX&new=1'
        r = requests.get(url)
        e = pq(r.text)
        print(e('title').text())


if __name__ == '__main__':
    main()
