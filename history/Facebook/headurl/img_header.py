import requests

from setting import test
# proxies = { 'https': "http//localhost:1080"}
proxies = {"https": "http://localhost:1080", }
for index, item in enumerate(test['img_header_url_8000'].find()):
    # blogger_id = item.get('url').split('com/')[-1]
    try:
        blogger_id = item.get('post_id')
        url = item.get('header_url')
        id = item.get('id')
        if int(id) < 15000:
            continue
        print(id, url)
        if not url:
            test['save'].insert({'id': id, 'header_url': ''})
            continue
        resp = requests.get(url, proxies=proxies)
        with open('img_header/{}.png'.format(blogger_id), 'wb') as f:
            f.write(resp.content)
        test['save'].insert({'id':id, 'header_url': url})
        print('save {}'.format(id))
    except Exception as e:
        print(e)
        print('=============')
        print(id, blogger_id)
