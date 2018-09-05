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
        self.key = 'd5621295fbc9e973b422e3f8d94c0f5ef33d85ddb70f6ce96e60943cdcaf3926a59427f029d41f362747c9be06054cf41a8398b8c7204aa04390124718343d0860fe53f9299a81997fbf59780fea1480'
        self.name = ''

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
        index_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzIzMDQyMjcxOA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=7d7541a666827f1ca6520bc3e141daf59bce65406d0d42547ed92aec2ce68ff8a16df00226ff3c5a95825d6c9f142c9e9290157ac337e4f06605422b018db5e49afbeb0182e0cd0a6834f5e461144158&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=QukIbv2L%2BF2U%2FCZzd3v66%2FOC4csWnrugWhRMuAyKIGcDjBInCr9SlHiYMfXP9kCL&winzoom=1'
        index_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzIzMDQyMjcxOA==&scene=124#wechat_redirect'
        self.set_key_uin()
        _biz_list = self.biz_list()
        if _biz_list:
            for biz in _biz_list:
                self._biz = biz

        self.create_url()
        log(self.url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            # 'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; tvfe_boss_uuid=19cb1313d3f0ac88; pt2gguin=o0574613576; rewardsn=; wxtokenkey=777; lang=zh_CN; mm_lang=zh_CN; pgv_si=s5298735104; wxuin=1156918861; sig=h018fd7149ab47774d880d8e735d77a368b6565a86e6a652e6be3e091cc5e401791df435fe84ae9cfc2; devicetype=Windows10; version=6206034e; pass_ticket=QukIbv2L+F2U/CZzd3v66/OC4csWnrugWhRMuAyKIGcDjBInCr9SlHiYMfXP9kCL; wap_sid2=CM3c1KcEElxJN1FKdGFSQ3lsOW5zSnNIZVFTTkpJQTVXNUlxVVAzaGRMQnVsT01LSnQ0WjN2QklacXFiWTJoYlk5RktQZzQwalEwSzJQem45bTFVcHFiU3VlWWszTXdEQUFBfjCTlb3cBTgNQJVO'
        }
        resp = requests.get(self.url, headers=headers)
        match_url = re.search('var msgList =.*?\';', resp.text).group()
        escape_url = html.unescape(match_url)

        # todo 内容里面包含 mp.weixin 链接去重 name：一个程序员的日常
        urls = re.findall('mp.weixin.qq.com.*?#wechat_redirect', escape_url)
        prefix = 'https://mp.weixin.qq.com/s?'
        backpack_list = []
        article_count = 0
        for article_count, url in enumerate(urls):
            # if article_count < 3:
            #     continue
            url = prefix + url.replace('amp;', '').replace(r'mp.weixin.qq.com\\/s?', '')
            log('article', url)
            # 匹配出错跳过
            if 'content_url' in url:
                continue
            article = Article()
            article.create(url)
            log("catch {}".format(article.title))
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
            sql = '''   
                INSERT INTO 
                    account_http(article_url, addon, account, account_id, author, id, title) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)
            '''
            _tuple = (
                entity.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author, entity.id,
                entity.title
            )
            uploads_mysql(config_mysql, sql, _tuple)
            # if article_count == 30:
            #     break
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
