# -*- coding: utf-8 -*-
import os
import sys
import re
import json
import time
import hashlib
import random
import requests
import datetime
import urllib.parse
from io import BytesIO
from PIL import Image
from lxml import etree
from SougouWeixin.config import *
from fake_useragent import UserAgent
from SougouWeixin.sqlserver_util import my_sqlserver
from SougouWeixin.captch_dytry import captch_upload_image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SougouWexin(object):
    def __init__(self, url):
        self.url = url
        # 待发包的数据
        self.need_send_all = []
        # 已查到的微信号字典
        self.account_find_all = {}
        # 该新闻关键词查询下有多少条新闻
        self.news_totals_all = 0
        # 已请求次数
        self.requests_totals_all = 0

        # requests相关配置
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        self.s = requests.session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.cookies = {}

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 5)

    # 获取随机User-Agent
    def get_ua(self):
        user_agent = UserAgent().random
        print('Get User-Agent:', user_agent)
        return user_agent

    # 查找相关新闻，全部
    def get_news_all(self, search_key):
        while 1:
            params = {
                'query': search_key,
                'type': 1,
                'ie': 'utf8',
            }
            referer_param = urllib.parse.urlencode({'query': search_key})
            referer = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=input&_sug_=y&_sug_type_=&' + referer_param
            self.headers['Referer'] = referer
            response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            news_total_text = response.text
            if re.search('以下内容来自微信公众号', news_total_text):
                result = ''
                html = etree.HTML(news_total_text)
                account_name = html.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a')
                if len(account_name):
                    result = account_name[0].text
                return result
            else:
                self.crack_sougou(response.url)

    # 处理验证码
    def crack_sougou(self, url):
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
                        print('---2222222---验证码输入错误------')
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
            print('------cookies已更新------')

    # 退出selenium
    def quit(self):
        self.browser.quit()
        print('关闭selnium')

    # 开始运行
    def run(self, search_key):
        return self.get_news_all(search_key)


if __name__ == '__main__':
    url = 'https://weixin.sogou.com/weixin'
    sougou_weixin = SougouWexin(url)
    ls = ['gh_5deb3f31ca4c', 'gh_3dadf54229b8', 'mmc-yishu', 'aixuexizixishi',
           'gh_6486ae83ed39', 'FDWHSCC1314', 'Dubai_Property', 'binggansang', 'cy__520sxl', 'gh_ea1a3db26321',
           'dzyxshzzb', 'PoemLawLiterature', 'hejinfu0606', 'WL-lanlan90', 'zui-kaizhou', 'shudongvivi',
           'jianhu17357515591', 'xy164110901', 'jdzfhk', 'fsshccyglyxgs', 'gh_ccc140cd53fa', 'laosunblog',
           'gh_eb4627ac5dff', 'Terracotta1979', 'SC5046', 'gh_c7cf0416f680', 'qyxbhxx', 'pushan-love',
           'gh_887cecdf76ca', 'gh_033db5fe9c20', 'gh_74b3b2fdd663', 'zju52share', 'jsqjzjjy', 'gh_7439fb177533',
           'Ocean_Warriors', 'futela2018', 'wxnmgltxgbdyzj', 'hjs353', 'Q2blockchain', 'ysy8456', 'gh_3ca6d5ac0bd1',
           'xiaoymsp', 'itASti-TM', 'gh_3b63b4d4ca99', 'xhgczj_123', 'huangtai260', 'enkin8888', 'ZhuHaikjk',
           'wyh2568780976', 'PSTE421261262', 'chaoShanLife520', 'nina17688399260', 'cqww11', 'NIB_DZ_Channel',
           'sixiangcd', 'gh_cb860056b87d', 'Mhuihui0-0', 'hnsxsfzydszdsyb', 'gh_d7252418f9e6', 'gh_2219b94b95b1',
           'jingshenjianbing', 'dgdjsh', 'gh_b7373d9ff0b2', 'gh_698dc9c1bdbb', 'yinyangchashe1', 'gh_f930f004e9ae',
           'gh_d30ee2c6a470', 'gh_ccbdb46e998f', 'gh_5c6abae06e1f', 'gh_7d73a0f8a224']

    for i in range(len(ls)):
        print('---{}---开始：{}'.format(i, ls[i]))
        result = sougou_weixin.run(ls[i])
        print('---{}---结束：{}：{}'.format(i, ls[i], result))
        time.sleep(0.5)
    sougou_weixin.quit()
