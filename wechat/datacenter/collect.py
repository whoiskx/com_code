# -*- coding: utf-8 -*-
import datetime
import random
import re
import time

import requests
import json
from setting import log
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Account, Backpack
from config import get_mysql_new
from utils import uploads_mysql
from verification_code import captch_upload_image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os

config_mysql = get_mysql_new()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
CAPTCHA_NAME = 'captcha.png'


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.s = requests.Session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.cookies = {'SUID': '72CF2A3B3320910A000000005BA45F01', 'ABTEST': '7|1537498880|v1', 'SUIR': '1537498880',
                        'IPLOC': 'CN4401', 'SNUID': '3B866372494D3F10939F743B4999FAA9',
                        'PHPSESSID': '1cik33mlj941crb2sjuqhglnd4', 'seccodeRight': 'success',
                        'SUV': '003F41133B2ACF725BA45F0162ABE037', 'successCount': '1|Fri, 21 Sep 2018 03:06:24 GMT',
                        'refresh': '1', 'JSESSIONID': 'aaaxuFjoJWjoo66765Bvw'}
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 4)

        # self

    def account_homepage(self):
        # 搜索并进入公众号主页
        count = 0
        while True:
            search_url = self.url.format(self.name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)

            if '相关的官方认证订阅号' in resp_search.text:
                log("找不到该公众号: {}".format(self.name))
                return
            e = pq(resp_search.text)
            if self.name in e(".tit").eq(0).text():
                account_link = e(".tit").find('a').attr('href')
            elif len(e(".tit").eq(0).text()) > 1:
                log("不能匹配正确的公众号: {}".format(self.name))
                return
            else:
                log(search_url)
                # log(resp_search.text)
                log('验证之前的cookie', self.cookies)
                try_count = 0
                while True:
                    try_count += 1
                    self.crack_sougou(search_url)
                    if '搜公众号' in self.driver.page_source:
                        log('------cookies更新------')
                        cookies = self.driver.get_cookies()
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
            account_match = re.search(r'微信号：\w*', e.text())
            account_search = account_match.group().replace('微信号：', '') if account_match else ''

            homepage = self.s.get(account_link, cookies=self.cookies)
            if '<title>请输入验证码 </title>' in homepage.text:
                print("出现验码")
                print('------开始处理微信验证码------')
                cert = random.random()
                image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
                respones = self.s.get(image_url, )
                captch_input = captch_upload_image(respones.content)
                print('------验证码：{}------'.format(captch_input))
                data = {
                    'cert': cert,
                    'input': captch_input
                }
                respones = self.s.post(image_url, data=data, cookies=self.cookies)
                cookies = requests.utils.dict_from_cookiejar(respones.cookies)
                print('adffa', cookies)
                homepage = self.s.get(account_link, cookies=self.cookies)
                print('破解验证码之后')
            account = pq(homepage.text)('.profile_account').text().replace('微信号: ', '')
            # 搜索页面有account，公众号主页有account，确保找到account
            return homepage.text, account or account_search

    def urls_article(self, html):
        items = re.findall('"content_url":".*?,"copyright_stat"', html)
        urls = []
        for item in items:
            url_last = item[15:-18].replace('amp;', '')
            url = 'https://mp.weixin.qq.com' + url_last
            urls.append(url)
        return urls

    def run(self):
        # self.set_name()
        # while True:
        account_list = ['江西政读',]
        entity = None
        backpack_list = []
        for name in account_list:
            self.name = name
            html_account = self.account_homepage()
            if html_account:
                html, account_of_homepage = html_account
            else:
                continue
            log('start 公众号: ', self.name)
            urls_article = self.urls_article(html)

            account = Account()
            account.name = self.name
            account.account = account_of_homepage
            account.get_account_id()
            account.account_id = 126774646

            for page_count, url in enumerate(urls_article):
                # if page_count < 35:
                #     continue
                article = Article()
                article.create(url, self.name)
                log('文章标题:', article.title)
                log("第{}条".format(page_count))

                entity = JsonEntity(article, account)
                backpack = Backpack()
                backpack.create(entity)
                backpack_list.append(backpack.create_backpack())
                import pymongo
                conn = pymongo.MongoClient('mongo')
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
                if page_count == 4:
                    break

        log("发包")
        if entity:
            # entity.uploads(backpack_list)
            # entity.uploads_datacenter_relay(backpack_list)
            entity.uploads_datacenter_unity(backpack_list)
            print('end')

    def crack_sougou(self, url):
        log('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            log('------开始处理搜狗验证码------')
            self.driver.get(url)
            time.sleep(2)
            if '搜公众号' in self.driver.page_source:
                for i in range(30):
                    self.driver.get(url)
                    log('浏览器页面正常')
                    if '搜公众号' not in self.driver.page_source:
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
                screenshot = self.driver.get_screenshot_as_png()
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
                        if '搜公众号' not in self.driver.page_source:
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
    test = AccountHttp()
    test.run()
