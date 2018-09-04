# -*- coding: utf-8 -*-

# 处理验证码
import datetime
import hashlib
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO


def crack_sougou(self, url):
    print('------开始处理未成功的URL------')
    self.browser.get(url)
    time.sleep(3)
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
        captcha.save('captcha.png')
        with open("captcha.png", "rb") as f:
            filebytes = f.read()
        captch_result = self.captch_upload_image(filebytes)
        captch_input = captch_result.get('Result')
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


# 识别验证码
def captch_upload_image(self, filebytes):
    url = 'http://api.dytry.com/ocr.json'
    paramKeys = ['username',
                 'password',
                 'typeid',
                 'softid',
                 'softkey'
                 ]
    paramDict = {
        "username": "uruntest",
        "password": "0763!@#",
        "typeid": 9999,
        "softid": 1107,
        "softkey": "34af19d2ee35e938dbbdc0336eb730cb"
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
    response = requests.post(url, params='', data=bs, headers=headers)
    requests.utils.dict_from_cookiejar(response.cookies)
    return response.json()