import json
import time
import requests
from setting import log


class Article(object):
    def __init__(self):
        self.url = ''
        self.title = ''
        self.content = ''
        # 作者即公众号名称
        self.author = ''
        self.From = ''
        self.time = ''

        self.readnum = ''
        self.likenum = ''


class Acount(object):
    def __init__(self):
        # 接口取
        self.account_id = None
        # account.account
        # 微信号(英文)
        self.account = ''
        # 公众号(中文)
        self.name = ''


class JsonEntity(object):

    def __init__(self, article, account):
        self.url = article.url
        self.title = article.title
        self.content = article.content
        # 公总号名字
        self.author = article.author
        self.From = article.author
        self.time = article.time

        self.views = article.readnum
        self.praises = article.likenum

        self.account_id = str(account.account_id)
        self.site_id = account.account_id
        self.topic_id = 0
        # 采集时间
        self.addon = str(int(time.time()))

        self.task_id = str(account.account_id)
        self.task_name = '微信_' + account.name

        self.account = account.account
        self.id = self.hash_md5(article.title + self.time)

    @staticmethod
    def hash_md5(s):
        import hashlib
        m = hashlib.md5()
        m.update(s.encode(encoding='utf-8'))
        return m.hexdigest()

    def uploads(self, backpack_list):
        if backpack_list:
            sever1 = 'http://115.231.251.252:26016/'
            sever2 = 'http://60.190.238.168:38015/'
            body = json.dumps(backpack_list)
            # 保证发送成功
            count = 0
            while True:
                if count > 2:
                    break
                try:
                    log('start uploads')
                    r = requests.post(sever1, data=body)
                    if r.status_code == 200:
                        log('uploads server1 successful')
                except Exception as e:
                    log('uploads http error1', e)
                try:
                    r2 = requests.post(sever2, data=body)
                    if r2.status_code == 200:
                        log('uploads server2 successful')
                        break
                except Exception as e:
                    log('uploads http error2', e)
                count += 1
            print('uploads over')


