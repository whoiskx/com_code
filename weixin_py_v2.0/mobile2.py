# -*- coding: utf-8 -*-
import datetime

import requests
import re
import html
from send_backpack import *
from config import get_mysql_new
from utils import uploads_mysql

config_mysql = get_mysql_new()


class Mobile(object):
    def __init__(self):
        self.url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
                   'action=home&__biz={}&uin={}&key={}'
        self._biz = 'MzU3NTQ5NDgwOQ=='
        self.uin = 'MTE1NjkxODg2MQ%3D%3D'
        self.key = '92b9bc849106aad7953d61c37ce85387f59ff02c56c7334397741b111c16b66fb69fa387049674a565fd854264c9a389d1af0e978ab6c22886528437fa0137d9ef4e48bc8c76142ed56a9e37e2bbf060'
        self.name = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

    def create_url(self):
        url = 'http://183.131.241.60:38011/nextaccount?label=5'
        self.url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
                   'action=home&__biz={}&uin={}&key={}'.format(self._biz, self.uin, self.key)
        log('index account', self.url)

    def biz_list(self):
        url = 'http://183.131.241.60:38011/nextaccount?label=5'
        r = requests.get(url)
        info_list = json.loads(r.text)
        _biz_list = []
        for info in info_list:
            _biz_list.append(info.get('biz'))
        return _biz_list

    def set_key_uin(self):
        if self.key and self.uin:
            return
        url = 'http://183.131.241.60:38011/outkey'
        r = requests.get(url)
        key_uin = r.text.split('|')
        if len(key_uin) == 2:
            self.uin, self.key = key_uin
            self.url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
                       'action=home&__biz={}&uin={}&key={}'.format(self._biz, self.uin, self.key)
        else:
            self.uin = ''
            self.key = ''

    def run(self):
        # self.set_key_uin()
        # _biz_list = self.biz_list()
        # if _biz_list:
        #     for biz in _biz_list:
        #         self._biz = biz
        #         self.create_url()
        #         log(self.url)
                self._biz = 'MzIzMDQyMjcxOA=='

                self.url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
                           'action=home&__biz={}&uin={}&key={}'.format(self._biz, self.uin, self.key)
                resp = requests.get(self.url, headers=self.headers)
                # 响应结果为空
                if len(resp.text) == 0:
                    self.set_key_uin()
                    resp = requests.get(self.url, headers=self.headers)
                    log('response 为空')
                    # break

                match_url = re.search('var msgList =.*?\';', resp.text).group()
                escape_url = html.unescape(match_url)

                # todo 内容里面包含 mp.weixin 链接去重 name：一个程序员的日常
                urls = re.findall('content_url.*?mp.weixin.qq.com.*?#wechat_redirect', escape_url)
                prefix = 'https://mp.weixin.qq.com/s?'
                backpack_list = []
                article_count = 0
                for article_count, url in enumerate(urls):
                    # if article_count < 3:
                    #     continue
                    url = prefix + url.replace('amp;', '').replace(r'content_url":"http:\\/\\/mp.weixin.qq.com\\/s?', '')
                    log('文章链接', url)
                    article = Article()
                    article.create(url)
                    log("文章标题 {}".format(article.title))
                    account = Acount()
                    # account 读文件跟信源搜索不一样
                    account.name = article.author
                    account.account = article.account
                    account.get_account_id()
                    entity = JsonEntity(article, account)
                    backpack = Backpack()

                    # 文章为分享
                    try:
                        backpack.create(entity)
                    except Exception as e:
                        log(e)
                        continue
                    backpack_list.append(backpack.create_backpack())

                    # 上传数据库
                    # sql = '''
                    #     INSERT INTO
                    #         account_http(article_url, addon, account, account_id, author, id, title)
                    #     VALUES
                    #         (%s, %s, %s, %s, %s, %s, %s)
                    # '''
                    # _tuple = (
                    #     entity.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author,
                    #     entity.id,
                    #     entity.title
                    # )
                    # uploads_mysql(config_mysql, sql, _tuple)
                    # # if article_count == 30:
                    # #     break
                #     break
                # break
                log('采集{}成功，共{}条文章'.format(self.name, article_count + 1))

                log("发包")
                if entity:
                    entity.uploads(backpack_list)
                    log("uploads successful")


def main():
    test = Mobile()
    test.run()


if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-