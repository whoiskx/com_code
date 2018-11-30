# -*- coding: utf-8 -*-
import datetime
import html
from models import *
from models import Account
import time
import re
from config import get_mysql_new
from utils import uploads_mysql

config_mysql = get_mysql_new()
from add_accountid import uploads_account_info_params

def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('mobile_log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


class Mobile(object):
    def __init__(self):
        self.url = ''
        self.url_match = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={}&uin={}&key={}'
        self._biz = ''
        self.uin = ''
        self.key = ''
        self.name = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }


    def create_url(self):
        self.url = self.url_match.format(self._biz, self.uin, self.key)
        log('账号主页', self.url)
        # # 增源
        resp = requests.get(self.url, headers=self.headers)
        e = pq(resp.text)
        name = e('.profile_nickname').text()
        account = 'hepancom'
        biz = self._biz
        feature = e('.profile_owner_info').text().replace('已认证 ', '')
        certification = e('.profile_desc').text()
        # uploads_account_info_params(name, account, biz, feature, certification)


    @staticmethod
    def biz_list():
        return ['MzAxMDU0MDYwMQ==']

        url = 'http://183.131.241.60:38011/nextaccount?label=5'
        r = requests.get(url)
        info_list = json.loads(r.text)
        _biz_list = []
        for info in info_list:
            _biz_list.append(info.get('biz'))
        return _biz_list

    def set_key_uin(self):
        self.uin = 'MTE1NjkxODg2MQ%3D%3D'
        self.key = '098f2de2d8c4a2c5c1bb12aa071585ba6fa96fb336b5de2c866e4bad8f46f93754eac96043944f6e552c1a7c19c89ad35002d9ffb1ff0948614024aeb573011bfbdd1745b6959e80b1c1af4d7040f018'
        return

        url = 'http://183.131.241.60:38011/outkey'
        while True:
            r = requests.get(url)
            key_uin = r.text.split('|')
            if len(key_uin) == 2:
                self.uin, self.key = key_uin
                log('取到key')
                log(self.key)
                log(self.uin)
                break
            else:
                log('取不到key')
                time.sleep(10)
                self.uin = ''
                self.key = ''

    def urls_article(self, resp):
        match_url = re.search('var msgList =.*?\';', resp.text).group()
        escape_url = html.unescape(match_url)
        urls_serach = re.findall('content_url.*?mp.weixin.qq.com.*?#wechat_redirect', escape_url)
        prefix = 'https://mp.weixin.qq.com/s?'
        urls = []
        for url in urls_serach:
            url = prefix + url.replace('amp;', '').replace(r'content_url":'
                                                           r'"http:\\/\\/mp.weixin.qq.com\\/s?', '')
            urls.append(url)
        return urls

    def run(self):
        self.set_key_uin()
        while True:
            _biz_list = self.biz_list()
            if _biz_list:
                entity = None
                for biz in _biz_list:
                    try:
                        self._biz = biz
                        self.create_url()
                        print('添加成功')
                        # self.url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA4OTEwNDUwMA==&uin=MTE1NjkxODg2MQ==&key=2e15abc1cc63c6472b3f9e24b445b1c19bb7dcee55cf4eb76c5363872c0f2f760899356828e84a3aeeb272cb0565257c52ac612c186648dbb4226484e2f04530a140a103860689fe7656df0d53f08ab5'
                        resp = requests.get(self.url, headers=self.headers)
                        # 响应结果为空即key失效
                        if len(resp.text) == 0:
                            log('key失效，获取新的key', self.url)
                            self.set_key_uin()
                            resp = requests.get(self.url, headers=self.headers)
                        else:
                            log('key有效，当前链接', self.url)
                        urls = self.urls_article(resp)

                        # 构建account
                        article = Article()
                        article.create(urls[0])
                        log("文章标题 {}".format(article.title))
                        # article.title = article.title.replace('【', '')
                        # article.title = article.title.replace('】', '')
                        # article.title = article.title.replace('！', '')

                        log(article.title)
                        account = Account()
                        account.name = article.author
                        # account.name = '中央纪委国家监委网站'
                        account.account = article.account
                        # account.account = 'gh_a78ef1e3d11e'
                        account.get_account_id()
                        account.account_id = 126774166
                        if not account.account:
                            log("错误，找不到account")

                        backpack_list = []
                        article_count = 0
                        for article_count, url in enumerate(urls):
                            log('文章链接', url)
                            article = Article()
                            article.create(url)
                            article.title = article.title.replace('.', '')
                            if '！' in article.title:
                                article.title = article.title.replace('！', '')
                            log("文章标题 {}".format(article.title))
                            entity = JsonEntity(article, account)
                            backpack = Backpack()

                            # 文章为分享,正则匹配不到时间，会异常
                            try:
                                backpack.create(entity)
                            except Exception as e:
                                log('share error', e)
                                continue
                            backpack_list.append(backpack.create_backpack())

                            # 上传数据库
                            sql = '''
                            INSERT INTO
                                account_http(article_url, addon, account, account_id, author, id, title)
                            VALUES
                                (%s, %s, %s, %s, %s, %s, %s)
                                    '''
                            _tuple = (
                                entity.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author,
                                entity.id,
                                entity.title
                            )
                            uploads_mysql(config_mysql, sql, _tuple)
                            # if article_count == 4:
                            #     break
                        log('采集账号：{} 所有文章完毕，共{}条文章'.format(self.name, article_count + 1))

                        log("发包")
                        if entity:
                            entity.uploads(backpack_list)
                            log("uploads successful")
                        print("end")
                        # 迭代一个账号
                        break
                    except Exception as e:
                        log('account error', e)
                        continue


def main():
    test = Mobile()
    # print(test.biz_list())
    test.run()


if __name__ == '__main__':
    # l = ['hepancom', 'nacsh688',  'stbjzz', 'stjjjc', 'wxcoupon', 'yxsh0796'] # 'st_rainbow',
    # info_dict = dict
    # ll = ['MzIyMjA0NTg1MQ==', 'MzIyMjA0NTg1MQ==', 'MzA5NzQ4MDU3MQ==', 'MzUzMTkwODc3OQ==','MzA5NTAzNTUwNQ==', 'MzA3NTM2ODk2Mg==']
    # ll = ['MzIyMjA0NTg1MQ==']
    main()
