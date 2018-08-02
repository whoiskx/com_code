import requests

from setting import test, log
# proxies = { 'https': "http//localhost:1080"}
proxies = {"https": "http://localhost:1080", }
for index, item in enumerate(test['img_herder_merge'].find()):
    # blogger_id = item.get('url').split('com/')[-1]
    try:
        blogger_id = item.get('blogger_id')
        url = item.get('header_url')
        id = item.get('id')
        # if int(id) < 5976:
        #     continue
        # print(id, url)
        log(id, url)
        if not url:
            test['save'].insert({'id': id, 'header_url': ''})
            continue
        resp = requests.get(url, proxies=proxies)
        with open('img_header_6000/{}.png'.format(blogger_id), 'wb') as f:
            f.write(resp.content)
        test['save_img'].insert({'id':id, 'header_url': url})
        # print('save {}'.format(id))
        log('{} save {}'.format(index, id))
    except Exception as e:
        log(e)
        log('=============')
        log(id, blogger_id)
