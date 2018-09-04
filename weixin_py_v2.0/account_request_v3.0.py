# -*- coding: UTF-8 -*-
import datetime
import re
import time
import pymysql
import requests
import json
from setting import log
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Acount, Backpack
from config import get_mysql_new, log


config_mysql = get_mysql_new()


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = '' or '大鼎豫剧'

    def account_homepage(self):
        # 搜索并进入公众号主页
        search_url = self.url.format(self.name)
        headers = {
            'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; sct=132; SNUID=568165754F4B3BFC4E8ADF104FB7AB4F; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw'
        }
        resp_search = requests.get(search_url, headers=headers)
        e = pq(resp_search.text)
        account_link = e(".tit").find('a').attr('href')

        homepage = requests.get(account_link)
        account = pq(homepage.text)('.profile_account').text().replace('微信号: ', '')
        return homepage.text, account

    def get_name(self):
        url = 'http://124.239.144.181:7114/Schedule/dispatch?type=8'
        resp = requests.get(url)
        # data 可能为空
        data_json = resp.text.get('data')
        data = json.loads(data_json)
        self.name = data.get('name')
        # print(self.name)
        # return self.name

    def run(self):
        # self.name = self.get_name()
        html, account_alp = self.account_homepage()
        # 所有文章链接
        items = re.findall('"content_url":".*?,"copyright_stat"', html)
        backpack_list = []
        for page_count, item in enumerate(items):
            log('start')
            url_last = item[15:-18].replace('amp;', '')
            url = 'https://mp.weixin.qq.com' + url_last
            article = Article()
            article.create(url, self.name)

            account = Acount()
            account.name = self.name
            account.account = account_alp
            account.get_account_id()

            entity = JsonEntity(article, account)
            backpack = Backpack()
            backpack.create(entity)
            backpack_list.append(backpack.create_backpack())

            # 上传数据库
            db = pymysql.connect(**config_mysql)
            cursor = db.cursor()
            cursor.execute(
                ''' INSERT INTO 
                        account_http(article_url, addon, account, account_id, author, id, title) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s)''',
                (article.url, datetime.datetime.now(), entity.account,
                 entity.account_id, entity.author, entity.id, entity.title))
            db.commit()
            cursor.close()
            db.close()
            if page_count == 30:
                break

        log("发包")
        if entity:
            entity.uploads(backpack)


if __name__ == '__main__':
    test = AccountHttp()
    test.run()
