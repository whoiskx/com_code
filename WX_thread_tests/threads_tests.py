# -*- coding: utf-8 -*-
import base64
import pymssql

import redis
from flask import Flask, request
import thulac

from utils import db, async, hash_md5
import random
import re
import time

import requests
import json
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Account, Backpack
from config import get_mysql_new, get_mysql_old
from utils import log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
from verification_code import captch_upload_image

config_mysql = get_mysql_new()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
CAPTCHA_NAME = 'captcha.png'

app = Flask(__name__)
error_result = {
    'Success': False,
    'Account': None,
    'Message': "",
    'count': 0,
    'ArtPubInfo': None,
    'ActiveDegree': None,
    'ArtPosNeg': None,
    'KeyWord': None
}


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.db = db
        self.s = requests.session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        self.cookies = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 4)
        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'
        self.status = 4

        self.count = 0

    @async
    def listen_task(self, account):
        while True:
            #     try:
            account_char = self.rcon.brpop(self.queue, 0)[1]
            account.name = account_char.decode(encoding="utf-8")
            account.run()
            # if account.browser:
            #     account.browser.quit()
            log("消耗一个account")
        # except Exception as e:
        #     log('error', '重启', e)
        #     if account.browser:
        #         account.browser.quit()
        #     account = AccountHttp()
        #     continue

    def account_homepage(self):
        # 搜索并进入公众号主页
        count = 0
        while True:
            if count == 2:
                break
            log('start', self.name)
            search_url = self.url.format(self.name)
            # referer = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=1565&sst0=1536470115264&lkt=0%2C0%2C0'.format(
            #     self.name)
            # self.headers['Referer'] = referer
            # self.url = 'http://weixin.sogou.com/weixin?query={}'.format(self.name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)
            e = pq(resp_search.text)
            log(e('title').text())
            if '搜狗' not in e('title').text():
                log('初始化session')
                self.s = requests.session()

            if self.name in e(".info").eq(0).text():
                account_link = e(".tit").find('a').attr('href')
                account_match = re.search(r'微信号：\w*', e.text())
                account_search = account_match.group().replace('微信号：', '') if account_match else ''

                homepage = self.s.get(account_link, cookies=self.cookies)
                if '<title>请输入验证码 </title>' in homepage.text:
                    self.crack_sougou(account_link)
                    homepage = self.s.get(account_link, cookies=self.cookies)
                    # log('破解验证码之后')
                account = pq(homepage.text)('.profile_account').text().replace('微信号: ', '')
                # 搜索页面有account，公众号主页有account，确保找到account
                return homepage.text, account or account_search
            elif len(e(".tit").eq(0).text()) > 1:
                log("不能匹配正确的公众号: {}".format(self.name))
                break
            if '相关的官方认证订阅号' in resp_search.text:
                log("找不到该公众号: {}".format(self.name))
                break
            else:
                # 处理验证码
                log(search_url)
                # log(resp_search.text)
                log('验证之前的cookie', self.cookies)
                try_count = 0
                while True:
                    try_count += 1
                    self.crack_sougou(search_url)
                    if '搜公众号' in self.browser.page_source:
                        log('------cookies更新------')
                        cookies = self.browser.get_cookies()
                        new_cookie = {}
                        for items in cookies:
                            new_cookie[items.get('name')] = items.get('value')
                        self.cookies = new_cookie
                        log('------cookies已更新------', self.cookies)
                        break
                    elif try_count > 6:
                        log("浏览器验证失败")
                        break

                log("验证完毕")
                time.sleep(2)
                # 被跳过的公众号要不要抓取  大概 4次
                continue

    def set_name(self):
        url = 'http://124.239.144.181:7114/Schedule/dispatch?type=8'
        resp = self.s.get(url)
        data_json = resp.text.get('data')
        if len(data_json) == 0:
            return ''
        data = json.loads(data_json)
        self.name = data.get('name')

    def urls_article(self, html):
        items = re.findall('"content_url":".*?,"copyright_stat"', html)
        urls = []
        for item in items:
            url_last = item[15:-18].replace('amp;', '')
            # 部分是永久链接
            if '_biz' in url_last:
                url = re.search('http://mp.weixin.qq.*?wechat_redirect', url_last).group()
                urls.append(url)
                continue
            url = 'https://mp.weixin.qq.com' + url_last
            # # 再次匹配
            # if len(url) > 260:
            #     item = re.search('"content_url":".*?wechat_redirect', url).group()
            #     url = item[15:].replace('amp;', '')
            urls.append(url)
        return urls

    def run(self):
        log("fadfsdf", self.cookies)
        html_account = self.account_homepage()
        if html_account:
            html, account_of_homepage = html_account
        else:
            # self.send_result()
            return
        log('start 公众号: ', self.name)
        urls_article = self.urls_article(html)

        account = Account()
        account.name = self.name
        account.account = account_of_homepage
        account.get_account_id()

        articles = []
        backpack_list = []
        self.count += 1
        print(self.count)
        for page_count, url in enumerate(urls_article):
            # if page_count > 2:
            #     break
            article = Article()
            log('url:', url)
            article.create(url, self.name)
            log('文章标题:', article.title)
            log("第{}条".format(page_count))

            # 超过9天不管
            # if article.time:
            #     article_date = datetime.datetime.fromtimestamp(int(article.time[:-3]))
            #     day_diff = datetime.datetime.now().date() - article_date.date()
            #     if day_diff.days > 6:
            #         break

            entity = JsonEntity(article, account)
            backpack = Backpack()
            backpack.create(entity)
            backpack_list.append(backpack.create_backpack())

            # 所有文章
            article_info = backpack.to_dict()
            articles.append(article_info)
        log('所有文章抓取完毕')
        print(self.count)

    def crack_sougou(self, url):
        log('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            log('------开始处理搜狗验证码------')
            self.browser.get(url)
            time.sleep(2)
            if '搜公众号' in self.browser.page_source:
                for i in range(30):
                    self.browser.get(url)
                    log('浏览器页面正常')
                    if '搜公众号' not in self.browser.page_source:
                        break
            try:
                img = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
                log('------出现验证码页面------')
                location = img.location
                size = img.size
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                screenshot = self.browser.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                captcha = screenshot.crop((left, top, right, bottom))
                captcha_path = os.path.join(IMAGE_DIR, CAPTCHA_NAME)
                captcha.save(captcha_path)
                with open(captcha_path, "rb") as f:
                    filebytes = f.read()
                captch_input = captch_upload_image(filebytes)
                log('------验证码：{}------'.format(captch_input))
                if captch_input:
                    input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                    input_text.clear()
                    input_text.send_keys(captch_input)
                    submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                    submit.click()
                    time.sleep(2)
                    try:
                        if '搜公众号' not in self.browser.page_source:
                            log('验证失败')
                            return
                        log('------验证码正确------')
                    except:
                        log('--22222222----验证码输入错误------')
            except Exception as e:
                log('------未跳转到验证码页面，跳转到首页，忽略------')

        elif re.search('mp\.weixin\.qq\.com', url):
            log('------开始处理微信验证码------')
            cert = random.random()
            image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
            respones = self.s.get(image_url, cookies=self.cookies)
            captch_input = captch_upload_image(respones.content)
            log('------验证码：{}------'.format(captch_input))
            data = {
                'cert': cert,
                'input': captch_input
            }
            self.s.post(image_url, cookies=self.cookies, data=data)
            log('------cookies已更新------')


if __name__ == '__main__':
    # t = Task()
    # t.listen_task()
    account = AccountHttp()
    account.listen_task(account)
    import threading
