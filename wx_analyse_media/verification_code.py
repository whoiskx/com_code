# -*- coding: utf-8 -*-
import hashlib
import random
import re
import time

import requests
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import os

# 打码平台参数配置
# 接口URL
DYTRY_APIURL = 'http://api.dytry.com/ocr.json'
# 用户名
DYTRY_USERNAME = 'uruntest'
# 用户密码
DYTRY_PASSWORD = '0763!@#'
# 题目类型
DYTRY_TYPEID = 9999
# 软件ID
DYTRY_SOFTID = 1107
# 软件KEY
DYTRY_SOFTKEY = '34af19d2ee35e938dbbdc0336eb730cb'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
CAPTCHA_NAME = 'captcha.png'


# 识别验证码
def captch_upload_image(filebytes):
    """
    :param filebytes: 待识别图像的二进制数据
    :return: 验证码识别后的字符串
    """

    paramKeys = ['username', 'password', 'typeid', 'softid', 'softkey']
    paramDict = {
        "username": DYTRY_USERNAME,
        "password": DYTRY_PASSWORD,
        "typeid": DYTRY_TYPEID,
        "softid": DYTRY_SOFTID,
        "softkey": DYTRY_SOFTKEY,
    }

    timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')
    boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
    boundarystr = '\r\n--%s\r\n' % (boundary)

    bs = b''
    for key in paramKeys:
        bs = bs + boundarystr.encode('ascii')
        param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
        # print param
        bs = bs + param.encode('utf8')
    bs = bs + boundarystr.encode('ascii')

    header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/jpeg\r\n\r\n' % (
        'sample')
    bs = bs + header.encode('utf8')

    bs = bs + filebytes
    tailer = '\r\n--%s--\r\n' % (boundary)
    bs = bs + tailer.encode('ascii')

    headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
               'Connection': 'Keep-Alive',
               'Expect': '100-continue',
               }
    response = requests.post(url=DYTRY_APIURL, params='', data=bs, headers=headers)
    requests.utils.dict_from_cookiejar(response.cookies)
    captch_input = response.json().get('Result')
    return captch_input


def crack_sougous(self, url):
    print('------开始处理未成功的URL：{}'.format(url))
    if re.search('weixin\.sogou\.com', url):
        print('------开始处理搜狗验证码------')
        self.browser.get(url)
        time.sleep(2)
        try:
            img = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
            print('------出现验证码页面------')
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
            print('------验证码：{}------'.format(captch_input))
            if captch_input:
                input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                input_text.clear()
                input_text.send_keys(captch_input)
                submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                submit.click()
                try:
                    print('------输入验证码------')
                    error_tips = self.wait.until(EC.presence_of_element_located((By.ID, 'error-tips'))).text
                    if len(error_tips):
                        print('------验证码输入错误------')
                        return
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'login-info')))
                    print('------验证码正确------')
                    cookies = self.browser.get_cookies()
                    new_cookie = {}
                    for items in cookies:
                        new_cookie[items.get('name')] = items.get('value')
                    self.cookies = new_cookie
                    print('------cookies已更新------')
                    return new_cookie
                except:
                    print('------验证码输入错误------')
        except:
            print('------未跳转到验证码页面，跳转到首页，忽略------')
    elif re.search('mp\.weixin\.qq\.com', url):
        print('------开始处理微信验证码------')
        cert = random.random()
        image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
        respones = self.s.get(image_url, cookies=self.cookies)
        captch_input = captch_upload_image(respones.content)
        print('------验证码：{}------'.format(captch_input))
        data = {
            'cert': cert,
            'input': captch_input
        }
        respones = self.s.post(image_url, cookies=self.cookies, data=data)
        self.cookies = requests.utils.dict_from_cookiejar(respones.cookies)
        print('微信cookies:', self.cookies)
        print('------cookies已更新------')
