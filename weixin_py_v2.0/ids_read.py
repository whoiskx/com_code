# -*- coding: UTF-8 -*-
import datetime
import pymssql
import re
import requests
from setting import log
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Acount, Backpack
from config import get_mysql_new, get_mysql_old
from utils import uploads_mysql

config_mysql = get_mysql_new()


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''

    def account_homepage(self, name):
        name = name or '大鼎豫剧'
        # 搜索并进入公众号主页
        search_url = self.url.format(name)
        headers = {
            'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; sct=132; SNUID=568165754F4B3BFC4E8ADF104FB7AB4F; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw'
        }
        resp_search = requests.get(search_url, headers=headers)
        e = pq(resp_search.text)
        account_link = e(".tit").find('a').attr('href')
        account = e('em_weixinhao').text()
        if account_link:
            homepage = requests.get(account_link)
            # 出现验证码
        else:
            # 搜狗暂无该订阅号
            return ''
        # print(resp.text)
        # html = homepage.text

        # account = pq(homepage.text)('.profile_account').text().replace('微信号: ', '')
        return homepage.text, account

    def get_name(self):
        with open('ids.txt', 'r', encoding='utf-8') as f:
            name_all = f.read()
        id_list = name_all.split("\n")
        _config_mysql = get_mysql_old()
        db = pymssql.connect(**_config_mysql)
        cursor = db.cursor()
        name_list = []
        for count, name in enumerate(id_list):
            sql_select = "SELECT * from WXAccount where ID={}".format(name)
            cursor.execute(sql_select)
            data = cursor.fetchone()
            if data:
                name_list.append(data[2])
            else:
                print(count, data)
        cursor.close()
        db.close()
        print(name_list)
        return name_list

    def run(self):
        name_list = self.get_name()
        for name in name_list:
            # name = '大鼎豫剧'
            self.name = name
            _tuple = self.account_homepage(name)
            if _tuple:
                html, _account = self.account_homepage(name)
            else:
                continue
            # 所有文章链接
            items = re.findall('"content_url":".*?,"copyright_stat"', html)
            backpack_list = []
            for page_count, item in enumerate(items):
                url_last = item[15:-18].replace('amp;', '')
                url = 'https://mp.weixin.qq.com' + url_last
                article = Article()
                article.create(url, self.name)
                account = Acount()
                # account 读文件跟信源搜索不一样
                account.name = article.author
                account.account = self.name
                account.get_account_id()
                entity = JsonEntity(article, account)
                backpack = Backpack()
                backpack.create(entity)
                backpack_list.append(backpack.create_backpack())
                log('catch {} successul'.format(account.name))

                # 上传数据库
                sql = '''   
                    INSERT INTO 
                        account_http(article_url, addon, account, account_id, author, id, title) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s)
                '''
                _tuple = (
                    article.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author, entity.id,
                    entity.title
                )
                uploads_mysql(config_mysql, sql, _tuple)
                if page_count == 30:
                    break

            log("发包")
            if entity:
                entity.uploads(backpack_list)
                log("uploads successful")


if __name__ == '__main__':
    test = AccountHttp()
    test.run()
