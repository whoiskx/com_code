# -*- coding: UTF-8 -*-
import datetime
import re
import time
import pymysql
import requests
import json
from setting import log
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Acount

MYSQL_HOST = '121.28.84.254'
MYSQL_PORT = 7101
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'YunRun2018!@#'
MYSQL_DATABASE = 'test'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'passwd': MYSQL_PASSWORD,
    'db': MYSQL_DATABASE,
    'charset': 'utf8'
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()


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
        backpack = []
        for page_count, item in enumerate(items):
            log('start')
            url_last = item[15:-18].replace('amp;', '')
            article = Article()

            article.url = 'https://mp.weixin.qq.com' + url_last
            # article.url = 'https://mp.weixin.qq.com/s?timestamp=1535704373&src=3&ver=1&signature=uulJZSS6rD01od4FwW9jJf2U85LjnH9BxezUEyuqJOWmCkhhmv1z22W2vK**KA0II-A-KBkXwdm6ZE0d46Jx3v-mh3U56Ee*i5V5ur7Fil*hJscU-9mjLyHiUZNKr-cFjXdO1pzSzdqdevKPuUh4rTLy-hJCb4FTTWu6nxAVH0c='
            resp_article = requests.get(article.url)
            e_aritile = pq(resp_article.text)
            article.title = e_aritile('.rich_media_title').text().replace(' ', '')
            article.content = e_aritile("#js_content").text().replace('\n', '')
            article.author = self.name
            article_timestramp_before = re.search('var ct=".*?"', resp_article.text).group()
            article_timestramp = re.search('\d+', article_timestramp_before).group()
            article.time = article_timestramp + '000'

            account = Acount()
            account.name = self.name
            account.account = account_alp
            account.account_id = ''
            get_account_id = 'http://60.190.238.178:38010/search/common/wxaccount/select?token=9ef358ed-b766-4eb3-8fde-a0ccf84659db&account={}'.format(
                account.account)
            url_resp = requests.get(get_account_id)
            json_obj = json.loads(url_resp.text)
            results = json_obj.get('results')
            if results:
                # todo 没有accountID 怎么做
                for i in results:
                    account.account_id = i.get('AccountID')
                    break

            wx_entity = JsonEntity(article, account)
            wx_dict = {
                'ID': wx_entity.id,
                'Account': wx_entity.account,
                'TaskID': wx_entity.task_id,
                'TaskName': wx_entity.task_name,
                'AccountID': wx_entity.account_id,
                'SiteID': int(wx_entity.site_id),
                'TopicID': 0,
                'Url': wx_entity.url,
                'Title': wx_entity.title,
                'Content': wx_entity.content,
                'Author': wx_entity.author,
                # 'Praises': praise_num,
                # 'Views': read_num,
                'Time': int(wx_entity.time),
                'AddOn': int(wx_entity.addon + '000'),
            }

            uploads_body = {
                "headers": {
                    "topic": "weixin",
                    "key": wx_entity.id,
                    "timestamp": int(time.time()),
                }
            }
            uploads_body.update({'body': json.dumps(wx_dict)})
            backpack.append(uploads_body)

            # 上传数据库
            cursor.execute(
                ''' INSERT INTO 
                        account_http(article_url, addon, account, account_id, author, id, title) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s)''',
                (article.url, datetime.datetime.now(), wx_entity.account,
                 wx_entity.account_id, wx_entity.author, wx_entity.id, wx_entity.title))
            db.commit()
            time.sleep(1)
            if page_count == 30:
                break

        log("发包")
        if wx_entity:
            wx_entity.uploads(backpack)


if __name__ == '__main__':
    test = AccountHttp()
    test.run()
