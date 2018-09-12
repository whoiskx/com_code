# -*- coding: utf-8 -*-
import re
import time

from pyquery import PyQuery as pq
import requests
from config import get_mysql_old, log
import pymssql


def uploads_account_info(self, e):
    url = ''
    info = dict()
    info['name'] = e(".tit").text()
    info['account'] = self.name
    show_list = e("dl")
    features, certified = '', ''
    for show in show_list:
        if '功能介绍' in pq(show).text():
            features = pq(show).text().replace('功能介绍：\n', '')
        if '认证' in pq(show).text():
            certified = pq(show).text().split('\n')[-1]
    info['features'] = features
    info['certified'] = certified
    count_loop = 0
    while True:
        # 查询
        count_loop += 1
        if count_loop > 4:
            break
        url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(self.name)
        result1 = requests.get(url_public)
        info_image = result1.json()
        image_url = info_image.get("imageUrl")
        image_id = info_image.get("id")
        if not image_id:
            # 增源
            config_mysql_old = get_mysql_old()
            db = pymssql.connect(**config_mysql_old)
            cursor = db.cursor()
            account_link = e(".tit").find('a').attr('href')
            homepage = self.s.get(account_link, cookies=self.cookies)
            # var biz = "MzU0MDUxMjM4OQ==" || ""
            biz_find = re.search('var biz = ".*?"', homepage.text)
            biz = ''
            if biz_find:
                biz = biz_find.group().replace('var biz = ', '')
            info["biz"] = biz
            try:
                sql_insert = """
                        INSERT INTO WXAccount(Name, Account, CollectionTime, Biz, Feature, Certification)
                        VALUES ('{}', '{}', GETDATE(), '{}', '{}', '{}')""".format(info.get('name'),
                                                                                   info.get('account'),
                                                                                   info.get('biz'),
                                                                                   info.get('features'),
                                                                                   info.get('certified'))
                cursor.execute(sql_insert)
                db.commit()
                log('插入数据成功', info.get('name'))
                log("当前账号id为0 需要添加{}".format(self.name))
            except Exception as e:
                log('插入数据错误', e)
                db.rollback()
                continue
            time.sleep(5)
            continue

def uploads_account_info(self, e):
    url = ''
    info = dict()
    info['name'] = e(".tit").text()
    info['account'] = self.name
    show_list = e("dl")
    features, certified = '', ''
    for show in show_list:
        if '功能介绍' in pq(show).text():
            features = pq(show).text().replace('功能介绍：\n', '')
        if '认证' in pq(show).text():
            certified = pq(show).text().split('\n')[-1]
    info['features'] = features
    info['certified'] = certified
    count_loop = 0
    while True:
        # 查询
        count_loop += 1
        if count_loop > 4:
            break
        url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(self.name)
        result1 = requests.get(url_public)
        info_image = result1.json()
        image_url = info_image.get("imageUrl")
        image_id = info_image.get("id")
        if not image_id:
            # 增源
            config_mysql_old = get_mysql_old()
            db = pymssql.connect(**config_mysql_old)
            cursor = db.cursor()
            account_link = e(".tit").find('a').attr('href')
            homepage = self.s.get(account_link, cookies=self.cookies)
            # var biz = "MzU0MDUxMjM4OQ==" || ""
            biz_find = re.search('var biz = ".*?"', homepage.text)
            biz = ''
            if biz_find:
                biz = biz_find.group().replace('var biz = ', '')
            info["biz"] = biz
            try:
                sql_insert = """
                        INSERT INTO WXAccount(Name, Account, CollectionTime, Biz, Feature, Certification)
                        VALUES ('{}', '{}', GETDATE(), '{}', '{}', '{}')""".format(info.get('name'),
                                                                                   info.get('account'),
                                                                                   info.get('biz'),
                                                                                   info.get('features'),
                                                                                   info.get('certified'))
                cursor.execute(sql_insert)
                db.commit()
                log('插入数据成功', info.get('name'))
                log("当前账号id为0 需要添加{}".format(self.name))
            except Exception as e:
                log('插入数据错误', e)
                db.rollback()
                continue
            time.sleep(5)
            continue

