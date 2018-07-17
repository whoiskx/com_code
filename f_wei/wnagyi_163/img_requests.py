import requests
import pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)

urun = conn.urun

for i, urls in enumerate(urun.wangyi.find()):
    try:
# url = 'https://necaptcha.nosdn.127.net/7ea63f88acc74cdea836e99fb21c469e@2x.jpg'
        if i > 4:
            break
        url = urls.get('url')
        html = requests.get(url)
        import os

        with open("img\{}".format(url[-15:]), 'wb') as file:
            file.write(html.content)
        print('ee')
    except Exception as e:
        print(e)
        continue