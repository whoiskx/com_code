# -*- coding: utf-8 -*-
import collections

import pymysql
from flask import Flask, request

import random
import re
import time

import requests
import json
from pyquery import PyQuery as pq
from config import get_mysql_new, get_mysql_old, GetCaptcha_url
from utils import log, captch_upload_image
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

app = Flask(__name__)


# log = log().info


class AccountHttp(object):
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
        self.cookies = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 4)
        self.browser.set_page_load_timeout(15)
        self.browser.set_script_timeout(15)
        self.count = 0
        self.BASE_DIR = r'D:\WXSchedule\Images'
        self.account_id = ''
        self.find = False

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

            if self.name == e(".info").eq(0).text().replace('微信号：', ''):
                info = self.uploads_account_info(e)

                self.find = True

                return info

                # 搜索页面有account，公众号主页有account，确保找到account
            elif len(e(".tit").eq(0).text()) > 1:
                log("不能匹配正确的公众号: {}".format(self.name))
                return '搜狗找不到该账号'
            if '相关的官方认证订阅号' in resp_search.text:
                log("找不到该公众号: {}".format(self.name))
                return '搜狗找不到该账号'
            else:
                # 处理验证码
                log(search_url)
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
                continue

    def uploads_account_info(self, e):
        info = dict()
        info['Name'] = e(".tit").text()
        info['Account'] = self.name
        show_list = e("dl")
        features, certified = '', ''
        for show in show_list:
            if '功能介绍' in pq(show).text():
                features = pq(show).text().replace('功能介绍：\n', '')
            if '认证' in pq(show).text():
                certified = pq(show).text().split('\n')[-1]
        info['Feature'] = features
        info['Certification'] = certified
        # info['Message'] = True
        # info['Status'] = 1

        # 获取头像二进制
        img_find = e(".img-box").find('img').attr('src')
        url_img_get = 'http:' + img_find
        info['ImageUrl'] = url_img_get
        return info

    def run(self):
        self.find = False
        info = self.account_homepage()
        if self.find and info:
            return info

    def run_uploads(self):
        self.find = False
        info = self.account_homepage()
        if self.find and info:
            return info

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
                captch_input = ''
                # log('start')
                files = {'img': (CAPTCHA_NAME, open(captcha_path, 'rb'), 'image/png', {})}
                res = requests.post(url=GetCaptcha_url, files=files)
                # log('end')
                res = res.json()
                if res.get('Success'):
                    captch_input = res.get('Captcha')
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
                raise RuntimeError

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


@app.route('/WeiXinInfo')
def get_account_info():
    all_account = request.args.get('account')
    if ',' in all_account:
        account_list = all_account.split(',')
        log(account_list)
    else:
        account_list = [all_account]
        log(account_list)
    info_list = []
    for account_name in account_list:
        account.name = account_name
        info = account.run()
        if info:
            info_list.append(info)
    count = len(info_list)
    if count == 0:
        status = 0
        msg = 'Fail'
    else:
        status = count
        msg = 'Successful'
    resutlt = collections.OrderedDict(status=status, msg=msg, totalCount=count, data=info_list)
    return json.dumps(resutlt)


@app.route('/WeiXinAccountUploads')
def get_account_info():
    all_account = request.args.get('account')
    if ',' in all_account:
        account_list = all_account.split(',')
        log(account_list)
    else:
        account_list = [all_account]
        log(account_list)
    info_list = []
    for account_name in account_list:
        account.name = account_name
        info = account.run_uploads()
        if info:
            info_list.append(info)
    count = len(info_list)
    if count == 0:
        status = 0
        msg = 'Fail'
    else:
        status = count
        msg = 'Successful'
    resutlt = collections.OrderedDict(status=status, msg=msg, totalCount=count, data=info_list)
    return json.dumps(resutlt)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=10009)
    except Exception as e:
        log('服务器错误 ', e)
        if account.browser:
            account.browser.quit()
        account = AccountHttp()