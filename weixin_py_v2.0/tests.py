# -*- coding: utf-8 -*-
#
# def t():
#     return 0
#
# p = t()
# print(p)
#
# s = 'NDAyNzE2MzQ1Ng==|9068b8cf3c4b19e45129213ddbfd60a0a4b10387abb2db3296048c71611f4c428b902eeefd2b0f6141cd9defbec3f54b603f7ba42281a66422c8b69bed0942a773e931c42b379547337bc4643f6d48d3'
# key_uin = s.split('|')
# if key_uin:
#     uin, key = key_uin
#     print(uin)
#     print(key)
# import json
#
# import requests
#
# url = 'http://183.131.241.60:38011/nextaccount?label=5'
# r = requests.get(url)
# info_str = r.text
# info_list= json.loads(info_str)
# for info in info_list:
#     _biz = info.get('biz')
# 
# s = 'content_url":"http:\\/\\/mp.weixin.qq.com\\/s?__biz=MzIzMDQyMjcxOA==&amp;mid=2247486157&amp;idx=1&amp;sn=6c582fa94c4a0da0821a0fc624dd17cc&amp;chksm=e8b2eb1cdfc5620ac7edbd655113f0725875b4fbcdb5777e4bacaa40c57993535985112742d0&amp;scene=27#wechat_redirect'
# url = s.replace('amp;', '').replace('content_url":"http:\\/\\/mp.weixin.qq.com\\/s?', '')
# print(url)
import time

import requests

# url = 'http://183.131.241.60:38011/outkey'
# _biz = ''
# while True:
#     r = requests.get(url)
#     print(r.text)
#     key_uin = r.text.split('|')
#     if len(key_uin) == 2:
#         uin, key = key_uin
#         url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
#                    'action=home&__biz={}&uin={}&key={}'.format(_biz, uin, key)
#         break
#     else:
#         print('none')
#         uin = ''
#         key = ''
# for i in range(2):
#     s = requests.Session()
#     r = s.get('https://mp.weixin.qq.com/profile?src=3&timestamp=1536203019&ver=1&signature=NHsz0BdTJaHizbwPPaEODtFV*unABNSLtg*PGevDLZ4dk6dzGAcREd9LbWW3pKjIwCc9Oq8evkihia9XfLP6Xg==')
#     with open('code.html', 'w', encoding='utf-8') as f:
#         f.write(r.text)
#     if '验证码' in r.text:
#         print('find')
#     cc = r.cookies.get_dict()
#     print(cc)

# with open('ids.txt', 'r', encoding='utf-8') as f:
#     name_all = f.read()
# id_list = name_all.split("\n")
# print(id_list)

# import pymongo
#
# conn = pymongo.MongoClient('mongodb://120.78.237.213:27017')
# urun = conn.weCaht
url = 'http://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d1%26s_from%3dinput%26query%3d%E6%99%9A%E8%81%8A%E4%BC%B4%E5%A4%9C%26ie%3dutf8%26_sug_%3dn%26_sug_type_%3d'
url = 'http://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d1%26s_from%3dinput%26query%3d%E6%99%9A%E8%81%8A%E4%BC%B4%E5%A4%9C%26ie%3dutf8%26_sug_%3dn%26_sug_type_%3d'
headers = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate',
           'Referer': 'http://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d1%26s_from%3dinput%26query%3d%E6%99%9A%E8%81%8A%E4%BC%B4%E5%A4%9C%26ie%3dutf8%26_sug_%3dn%26_sug_type_%3d',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
           'Connection': 'keep-alive',
           'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; LSTMV=0%2C0; LCLKINT=235; SNUID=9A638690ABAEDE83070339C3ACDDE1AD; sct=179; PHPSESSID=qvdgtcif7omomgook8bb7vs8n2; SUIR=9A638690ABAEDE83070339C3ACDDE1AD; refresh=1',
           'Host': 'weixin.sogou.com', 'Pragma': 'no-cache', 'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}
headers['Referer'] = url

r = requests.get(url, headers=headers)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import os

browser = webdriver.Chrome()
browser.get(url)
time.sleep(2)
wait = WebDriverWait(browser, 10)
try:
    img = wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
    print('------出现验证码页面------')
    location = img.location
    size = img.size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((left, top, right, bottom))

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, 'images')
    CAPTCHA_NAME = 'captcha.png'

    captcha_path = os.path.join(IMAGE_DIR, CAPTCHA_NAME)
    captcha.save(captcha_path)
    with open(captcha_path, "rb") as f:
        filebytes = f.read()

    from verification_code import captch_upload_image
    captch_input = captch_upload_image(filebytes)
    print('------验证码：{}------'.format(captch_input))
    if captch_input:
        input_text = wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
        input_text.clear()
        input_text.send_keys(captch_input)
        submit = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit.click()
        try:
            print('------输入验证码------')
            error_tips = wait.until(EC.presence_of_element_located((By.ID, 'error-tips'))).text
            if len(error_tips):
                print('------验证码输入错误------')

                print("结束")
                # return
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'login-info')))
            print('------验证码正确------')
            cookies = browser.get_cookies()
            new_cookie = {}
            for items in cookies:
                new_cookie[items.get('name')] = items.get('value')
            cookies = new_cookie
            print('------cookies已更新------')
            print(new_cookie)
            print("结束222")
            # return new_cookie
        except:
            print('------验证码输入错误------')
except Exception as e:
    print(e)
    print('------未跳转到验证码页面，跳转到首页，忽略------')

# print(r.text)
