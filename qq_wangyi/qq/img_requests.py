import requests
import pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun

for i, urls in enumerate(urun.qq_img.find()):
    try:
        # if i > 4:
        #     break
        url = urls.get('url')
        html = requests.get(url)
        with open("img_qq\{}".format(url[-30:-15] + '.jpg'), 'wb') as file:
            file.write(html.content)
        print('第{}次'.format(i))
    except Exception as e:
        print(e, i)
        continue
