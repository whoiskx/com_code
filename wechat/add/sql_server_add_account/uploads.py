# -*- coding: utf-8 -*-
import pymssql
import re
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from pyquery import PyQuery as pq
from config import log, get_mysql_old


class UploadsSqlServer(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.s = requests.session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 4)

    def run(self):
        search_url = self.url.format(self.account)
        print(search_url)
        resp_search = self.s.get(search_url, headers=self.headers)
        if '相关的官方认证订阅号' in resp_search.text:
            log("找不到该公众号: {}".format(self.name))
            return
        e = pq(resp_search.text)
        info = dict()
        info['name'] = e(".tit").text()
        info['account'] = self.account
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
            count_loop += 1
            if count_loop > 2:
                break
            config_mysql_old = get_mysql_old()
            db = pymssql.connect(**config_mysql_old)
            cursor = db.cursor()
            account_link = e(".tit").find('a').attr('href')
            homepage = self.s.get(account_link, headers=self.headers)
            # var biz = "MzU0MDUxMjM4OQ==" || ""
            biz_find = re.search('var biz = ".*?"', homepage.text)
            biz = ''
            if biz_find:
                biz = biz_find.group().replace('var biz = ', '').replace('"', '')
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


if __name__ == '__main__':
    # 通过account 上传,修改参数 self.account，修改header里面的cookie
    test = UploadsSqlServer()
    test.headers.update({"Cookie":'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; LSTMV=0%2C0; LCLKINT=235; weixinIndexVisited=1; SNUID=632DC8D8E2E6944AC73055A1E32B1409; JSESSIONID=aaaOQz-tRsFTI7chK4Bvw; sct=317'})
    test.account = 'daokouTB'
    test.run()
