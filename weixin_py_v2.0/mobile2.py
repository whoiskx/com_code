# -*- coding: utf-8 -*-
import datetime
import html
from send_backpack import *
from config import get_mysql_new
from utils import uploads_mysql

config_mysql = get_mysql_new()


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

    @staticmethod
    def biz_list():
        url = 'http://183.131.241.60:38011/nextaccount?label=5'
        r = requests.get(url)
        info_list = json.loads(r.text)
        _biz_list = []
        for info in info_list:
            _biz_list.append(info.get('biz'))
        return _biz_list

    def set_key_uin(self):
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

    def run(self):
        self.set_key_uin()
        while True:
            _biz_list = self.biz_list()
            if _biz_list:
                for biz in _biz_list:
                    try:
                        self._biz = biz
                        self.create_url()
                        resp = requests.get(self.url, headers=self.headers)
                        # 响应结果为空即key失效
                        if len(resp.text) == 0:
                            log('key失效，获取新的链接', self.url)
                            self.set_key_uin()
                            resp = requests.get(self.url, headers=self.headers)
                        else:
                            log('key有效，链接', self.url)
                        match_url = re.search('var msgList =.*?\';', resp.text).group()
                        escape_url = html.unescape(match_url)

                        urls = re.findall('content_url.*?mp.weixin.qq.com.*?#wechat_redirect', escape_url)
                        prefix = 'https://mp.weixin.qq.com/s?'
                        backpack_list = []
                        article_count = 0
                        for article_count, url in enumerate(urls):
                            url = prefix + url.replace('amp;', '').replace(r'content_url":'
                                                                           r'"http:\\/\\/mp.weixin.qq.com\\/s?', '')
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
                            # # if article_count == 30:
                            # #     break
                        log('采集账号：{} 所有文章完毕，共{}条文章'.format(self.name, article_count + 1))

                        log("发包")
                        if entity:
                            entity.uploads(backpack_list)
                            log("uploads successful")
                    except Exception as e:
                        log('account error', e)
                        continue


def main():
    test = Mobile()
    # print(test.biz_list())
    test.run()


if __name__ == '__main__':
    main()
