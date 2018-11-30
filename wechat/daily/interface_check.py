# -*- coding: utf-8 -*-
import requests


def main():
    new_media_1 = 'http://182.245.126.226:8312/WeiXinArt/AddAccount?account=zyjwgjjw'
    new_media_2 = 'http://182.245.126.226:8312/WeiXinArt/PublishTimes?accountid=8f80744ba71688f9521bb8c612bdf8d6'

    sentment_analyse_1 = 'http://182.245.126.226:21012/WeiXinArt/WeiXinInfo?account=zcsr91'
    sentment_analyse_2 = 'http://182.245.126.226:21012/WeiXinArt/WeiXinParse?account=iXianYanSuiYu'

    urls = [new_media_1, new_media_2, sentment_analyse_1, sentment_analyse_2]
    for url in urls:
        r = requests.get(url)
        print(r.status_code)
        print(r.text)


if __name__ == '__main__':
    main()
