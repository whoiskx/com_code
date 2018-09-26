# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
import time

import requests
import json
from setting import log
from pyquery import PyQuery as pq
from models import JsonEntity, Article, Account, Backpack
from config import get_mysql_new, log
from utils import uploads_mysql

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from PIL import Image
from io import BytesIO
from verification_code import captch_upload_image

config_mysql = get_mysql_new()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
CAPTCHA_NAME = 'captcha.png'


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.search_name = ''
        self.s = requests.Session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.cookies = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 4)

    def account_homepage(self):
        # 搜索并进入公众号主页
        count = 0
        while True:
            count += 1
            if count > 2:
                break
            log('start account', self.search_name)
            search_url = self.url.format(self.search_name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)
            e = pq(resp_search.text)
            log('响应标题', e('title').text())
            if '搜狗' not in e('title').text():
                log('初始化session')
                self.s = requests.session()
            if self.search_name in e(".info").eq(0).text():
                account_link = e(".tit").find('a').attr('href')
                self.name = e(".tit").text()
                homepage = self.s.get(account_link, cookies=self.cookies)
                if '<title>请输入验证码 </title>' in homepage.text:
                    self.crack_sougou(account_link)
                    homepage = self.s.get(account_link, cookies=self.cookies)
                return homepage.text
            elif len(e(".tit").eq(0).text()) > 1:
                log("不能匹配正确的公众号: {}".format(self.search_name))
                break
            if '相关的官方认证订阅号' in resp_search.text:
                log("找不到该公众号: {}".format(self.search_name))
                break
            else:
                # 处理验证码
                log(search_url)
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
                continue

    def account_list(self):
        # 老版
        # url = 'http://124.239.144.181:7114/Schedule/dispatch?type=8'
        # # url = 'http://183.131.241.60:38011/nextaccount?label=5'
        # resp = requests.get(url)
        # # data 可能为空
        # data_json = resp.text.get('data')
        # data = json.loads(data_json)
        # self.search_name = data.get('name')
        # print(self.search_name)
        # return self.search_name

        url = 'http://183.131.241.60:38011/nextaccount?label=5'
        resp = requests.get(url)
        items = json.loads(resp.text)
        if len(items) == 0:
            return []
        account_all = []
        for item in items:
            account_all.append(item.get('account'))
        log("开始account列表", account_all)
        return account_all

    def urls_article(self, html):
        items = re.findall('"content_url":".*?,"copyright_stat"', html)
        urls = []
        for item in items:
            url_last = item[15:-18].replace('amp;', '')
            url = 'https://mp.weixin.qq.com' + url_last
            urls.append(url)
        return urls

    def run(self):
        while True:
            account_list = self.account_list()
            # account_list = ['sxbzpu', 'rzbotyb', 'ordos-dfkg', 'rencaiguangzhou', 'zygfwx']
            for _account in account_list:
                self.search_name = _account
                html_account = self.account_homepage()
                if html_account:
                    html = html_account
                else:
                    log('找到不到微信号首页: ', _account)
                    continue
                urls_article = self.urls_article(html)

                account = Account()
                account.name = self.name
                account.account = _account
                account.get_account_id()
                if not account.account_id:
                    log("没有account_id")

                entity = None
                backpack_list = []
                for page_count, url in enumerate(urls_article):
                    # if page_count < 35:
                    #     continue
                    article = Article()
                    article.create(url, account)
                    log('文章标题:', article.title)
                    log("第{}条".format(page_count))
                    entity = JsonEntity(article, account)
                    backpack = Backpack()
                    backpack.create(entity)
                    backpack_list.append(backpack.create_backpack())
                    # if page_count == 1:
                    #     break
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
                log("发包")
                if entity:
                    entity.uploads(backpack_list)

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
                    except Exception as e:
                        log('--22222222----验证码输入错误------', e)
            except Exception as e:
                log('------未跳转到验证码页面，跳转到首页，忽略------', e)

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
