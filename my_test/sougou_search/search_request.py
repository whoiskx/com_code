import requests


proxys = {'http': 'http://117.127.0.196:80', 'https': 'https://117.127.0.196:80', }


def send_requset():
    for i in range(10):
        url = 'http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%B9%BF%E5%B7%9E%E5%85%AC%E5%AE%89&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=356811&sst0=1528771011156&lkt=0%2C0%2C0'
        url = 'https://weibo.com/login.php'
        resp = requests.get(url, proxies=proxys)
        print(resp.status_code)
        resp.encoding = "utf-8"
        with open("sougou_{}.html".format(i), "w", encoding="utf-8") as f:
            f.write(resp.text)
        # print(resp.text)


if __name__ == '__main__':
    send_requset()
