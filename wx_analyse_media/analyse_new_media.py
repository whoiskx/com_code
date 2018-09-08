# -*- coding: utf-8 -*-
import datetime
import random
import re
import time
from collections import Counter

import requests
import json
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Account, Backpack
from config import get_mysql_new
from utils import log
from utils import uploads_mysql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
from handle_artiles import handle
import jieba
from verification_code import captch_upload_image
from utils import db

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
            # 'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; LSTMV=0%2C0; LCLKINT=235; SNUID=9A638690ABAEDE83070339C3ACDDE1AD; sct=168',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.cookies = {
            # 'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; LSTMV=0%2C0; LCLKINT=235; SNUID=9A638690ABAEDE83070339C3ACDDE1AD; sct=168',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

        }

        self.db = db

        self.browser = ''
        self.wait = ''

    # def crack_sougou(self, url):
    #     print('------开始处理未成功的URL：{}'.format(url))
    #     # if 'weixin\.sogou\.com' in url:
    #     print('------开始处理搜狗验证码------')
    #     chrome_options = webdriver.ChromeOptions()
    #     # chrome_options.add_argument('--headless')
    #     browser = webdriver.Chrome(chrome_options=chrome_options)
    #     browser.get(url)
    #     time.sleep(2)
    #     try:
    #         wait = WebDriverWait(browser, 10)
    #         img = wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
    #         print('------出现验证码页面------')
    #         location = img.location
    #         size = img.size
    #         left = location['x']
    #         top = location['y']
    #         right = location['x'] + size['width']
    #         bottom = location['y'] + size['height']
    #         screenshot = browser.get_screenshot_as_png()
    #         screenshot = Image.open(BytesIO(screenshot))
    #         captcha = screenshot.crop((left, top, right, bottom))
    #         captcha_path = os.path.join(IMAGE_DIR, CAPTCHA_NAME)
    #         captcha.save(captcha_path)
    #         with open(captcha_path, "rb") as f:
    #             filebytes = f.read()
    #         captch_input = captch_upload_image(filebytes)
    #         print('------验证码：{}------'.format(captch_input))
    #         if captch_input:
    #             input_text = wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
    #             input_text.clear()
    #             input_text.send_keys(captch_input)
    #             submit = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
    #             submit.click()
    #             try:
    #                 print('------输入验证码------')
    #                 error_tips = wait.until(EC.presence_of_element_located((By.ID, 'error-tips'))).text
    #                 if len(error_tips):
    #                     print('------验证码输入错误------')
    #                     return
    #                 wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'login-info')))
    #                 print('------验证码正确------')
    #                 cookies = browser.get_cookies()
    #                 new_cookie = {}
    #                 for items in cookies:
    #                     new_cookie[items.get('name')] = items.get('value')
    #                 self.cookies = new_cookie
    #                 print('------cookies已更新------')
    #                 # if browser:
    #                 #     browser.close()
    #                 return new_cookie
    #             except:
    #                 print('------验证码输入错误------')
    #                 # if browser:
    #                 #     browser.close()
    #     except:
    #         # if browser:
    #         #     browser.close()
    #         print('------未跳转到验证码页面，跳转到首页，忽略------')

    def account_homepage(self, one_cookie):
        # 搜索并进入公众号主页
        search_url = self.url.format(self.name)
        resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)

        if '相关的官方认证订阅号' in resp_search.text:
            log("找不到该公众号: {}".format(self.name))
            return
        e = pq(resp_search.text)
        if self.name in e(".info").eq(0).text():
            account_link = e(".tit").find('a').attr('href')
        elif len(e(".tit").eq(0).text()) > 1:
            log("不能匹配正确的公众号: {}".format(self.name))
            return
        else:
            # 处理验证码
            self.crack_sougou(search_url, one_cookie)
            print("验证完毕")
            # 被跳过的公众号要不要抓取  大概 4次
            return
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

    def run(self, one_cookie):
        self.cookies = one_cookie
        print(one_cookie.cookie)
        self.db = db
        article_detaile = db['newMedia'].find_one({'Account': self.name})
        html_account = self.account_homepage(one_cookie.cookie)
        if html_account:
            html, account_of_homepage = html_account
        else:
            return
        log('start 公众号: ', self.name)
        urls_article = self.urls_article(html)

        account = Account()
        account.name = self.name
        account.account = account_of_homepage
        account.get_account_id()

        articles = []
        backpack_list = []
        for page_count, url in enumerate(urls_article):
            if page_count > 2:
                break
            article = Article()
            log('url:', url)
            article.create(url, self.name)
            log('文章标题:', article.title)
            log("第{}条".format(page_count))

            # 超过9天不管
            if article.time:
                article_date = datetime.datetime.fromtimestamp(int(article.time[:-3]))
                day_diff = datetime.datetime.now() - article_date
                if day_diff.days > 9:
                    break

            entity = JsonEntity(article, account)
            backpack = Backpack()
            backpack.create(entity)
            backpack_list.append(backpack.create_backpack())

            # 所有文章
            article_info = backpack.to_dict()
            articles.append(article_info)
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

        content_all_list = ''
        for article in articles:
            content_all_list += article.get('Content')
        # 分词处理
        key_words_list = []
        seg_list = jieba.cut(''.join(content_all_list), cut_all=False)
        for i in seg_list:
            if len(i) >= 2 and re.match('[\u4e00-\u9fff]+', i):
                key_words_list.append(i)

        # 返回前10个出现频率最高的词
        key_words_counter = Counter(key_words_list).most_common(10)
        key_word = dict()
        key_word['list'] = []
        for k in key_words_counter:
            key_word['list'].append(
                {
                    "times": k[1],
                    "keyword": k[0]
                }
            )
        result = handle(articles)
        result['KeyWord'] = key_word
        print(self.name)
        db['newMedia'].update({'Account': self.name}, {'$set': {'data': result}})
        log('数据抓取完成')

        # 向前端发送成功请求
        # account_id = article_detaile.get('id')
        # status_url = '/api/drafts/updateAnalysisStatusByAnalysisId'
        # params = {
        #     'type': 3,
        #     'analysisId': account_id,
        #     'status': 3,
        # }
        # requests.get(status_url, params=params)

    def crack_sougou(self, url, one_cookie):
        print('------开始处理搜狗验证码------')
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 5)

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
                    # print('------输入验证码------')
                    # error_tips = self.wait.until(EC.presence_of_element_located((By.ID, 'error-tips'))).text
                    # print('aaaaaaaaaaaaaa', error_tips, 'aaaaaaaaa')
                    # if len(error_tips):
                    #     print('------验证码输入错误------')
                    #     return
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'login-info')))
                    print('------验证码正确------')
                    cookies = self.browser.get_cookies()
                    new_cookie = {}
                    for items in cookies:
                        new_cookie[items.get('name')] = items.get('value')
                    self.cookies = new_cookie
                    one_cookie.cookie = new_cookie
                    # db['cookie'].de(new_cookie)
                    print('------cookies已更新------')
                    return new_cookie
                except:
                    print('------验证码输入错误------')
        except:
            print('------未跳转到验证码页面，跳转到首页，忽略------')


if __name__ == '__main__':
    test = AccountHttp()
    test.run()
