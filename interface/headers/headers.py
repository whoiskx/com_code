# -*- coding: utf-8 -*-
import base64
import pymssql

import pymysql
import redis
from flask import Flask, request

from utils import db, async, hash_md5
import random
import re
import time

import requests
import json
from pyquery import PyQuery as pq
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
        # chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 4)
        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'
        self.status = 4

        self.count = 0

    def account_homepage(self):
        # 搜索并进入公众号主页
        count = 0
        while True:
            if count == 2:
                break
            log('start', self.name)
            search_url = self.url.format(self.name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)
            e = pq(resp_search.text)
            log(e('title').text())
            if '搜狗' not in e('title').text():
                log('初始化session')
                self.s = requests.session()

            if self.name in e(".info").eq(0).text():
                img_find = e(".img-box").find('img').attr('src')
                url_img_get = 'http:' + img_find
                return url_img_get

                # 搜索页面有account，公众号主页有account，确保找到account
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

    def handle_img(self, img_b, image_id):
        url_img = 'http://47.99.50.93:8009/SaveImage'
        data_img = {'content': base64.b64encode(img_b), 'account_id': image_id}
        r = requests.post(url_img, data=data_img)
        log('头像上传结果:', r.status_code)
        # 更新数据库
        config_mysql_old = get_mysql_old()
        db = pymssql.connect(**config_mysql_old)
        cursor = db.cursor()
        path = 'Images/' + str(image_id // 1000) + '/' + str(image_id)
        try:
            sql_insert = """UPDATE  WXAccount SET ImageUrl='{}' WHERE ID='{}'""".format(path, image_id)
            cursor.execute(sql_insert)
            db.commit()
            log('更新数据成功', image_id)
        except Exception as e:
            log('更新数据错误', e)
            db.rollback()

    def run(self):
        url_img = self.account_homepage()
        if url_img:
            print(url_img)
            resp = requests.get(url_img)
            img_b = resp.content
            image_id = self.account
            self.handle_img(img_b, int(image_id))
        else:
            # self.send_result()
            return
        log('完成 公众号: ', self.name)

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


account = AccountHttp()


@app.route('/save/images')
def save_images():
    name = request.args.get('account')
    mysql_config = get_mysql_old()
    db = pymssql.connect(**mysql_config)
    cursor = db.cursor()
    sql_select = """
            select id from wxaccount where account=%s 
    """
    cursor.execute(sql_select, (name,))
    info = list(cursor.fetchmany(1))[0]
    account_id = info[0]
    account.name = name
    account.account = account_id
    account.run()
    return '完成'


if __name__ == '__main__':
    # t = Task()
    # t.listen_task()
    app.run(port=8077)
    import threading
