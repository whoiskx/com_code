# -*- coding: utf-8 -*-
import requests

urls = [
    {'舆情公众号信息': 'http://182.245.126.226:21012/WeiXinArt/WeiXinInfo?account=zcsr91'},
    {'舆情公众号分析': 'http://182.245.126.226:21012/WeiXinArt/WeiXinParse?account=iXianYanSuiYu'},

    {'中信新媒体公众号信息': 'http://182.245.126.226:8312/WeiXinArt/AddAccount?account=zyjwgjjw'},
    {'中信新媒体公众号分析': 'http://182.245.126.226:8312/WeiXinArt/PublishTimes?accountid=8f80744ba71688f9521bb8c612bdf8d6'},

]

def main():
    for url_info in urls:
        url = list(url_info.values())[0]
        r = requests.get(url)
        if r.status_code != 200:
            print(url_info)
            print(r.text)


if __name__ == '__main__':
    main()
