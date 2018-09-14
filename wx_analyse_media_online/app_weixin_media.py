# -*- coding: utf-8 -*-
import base64
import pymssql

import redis
from flask import Flask, request
import thulac

from utils import db, async, hash_md5
import datetime
import random
import re
import time
from collections import Counter

import requests
import json
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Account, Backpack
from config import get_mysql_new, get_mysql_old
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
import jieba.posseg

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
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
        self.cookies = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 4)

        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'

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

    def send_info(self, info, path):
        loop_count = 0
        while True:
            loop_count += 1
            if loop_count > 3:
                break
            send_info = dict()
            send_info['account'] = info.get('account', '')
            send_info['name'] = info.get('name', '')
            # send_info['imageUrl'] = path
            send_info['imageUrl'] = info.get('imageUrl', '')
            send_info['message'] = info.get('message', True)
            send_info['feature'] = info.get('features', '')
            send_info['certification'] = info.get('certified', '')
            send_info['status'] = 3
            send_url = 'http://58.56.160.39:38012/MediaManager/api/weixinInfo/add'
            r = requests.post(send_url, data=json.dumps(send_info))
            if r.status_code == 200:
                log("发送weixininfo成功")
                break

    def handle_img(self, img_b, image_id, info, path):
        url_img = 'http://47.99.50.93:8009/SaveImage'
        data_img = {'content': base64.b64encode(img_b), 'account_id': image_id}
        r = requests.post(url_img, data=data_img)
        log('头像上传:', r.status_code)
        # 更新数据库
        config_mysql_old = get_mysql_old()
        db = pymssql.connect(**config_mysql_old)
        cursor = db.cursor()
        try:
            sql_insert = """UPDATE  WXAccount SET ImageUrl='{}' WHERE ID='{}'""".format(path, image_id)
            cursor.execute(sql_insert)
            db.commit()
            log('更新数据成功', info.get('name'))
        except Exception as e:
            log('更新数据错误', e)
            db.rollback()

    def uploads_account_info(self, e):
        info = dict()
        info['name'] = e(".tit").text()
        info['account'] = self.name
        show_list = e("dl")
        features, certified = '', ''
        for show in show_list:
            if '功能介绍' in pq(show).text():
                features = pq(show).text().replace('功能介绍：\n', '')
            if '认证' in pq(show).text():
                certified = pq(show).text().split('\n')[-1]
        info['features'] = features
        info['certified'] = certified
        info['message'] = True
        info['status'] = 0

        # 获取头像二进制
        img_find = e(".img-box").find('img').attr('src')
        url_img_get = 'http:' + img_find
        info['imageUrl'] = url_img_get
        path = ''
        self.send_info(info, path)


        # r_img = requests.get(url_img_get)
        # img_b = r_img.content
        #
        # count_loop = 0
        # while True:
        #     # 查询
        #     count_loop += 1
        #     if count_loop > 4:
        #         break
        #     url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(self.name)
        #     result1 = requests.get(url_public)
        #     info_image = result1.json()
        #     image_url = info_image.get("imageUrl")
        #     image_id = info_image.get("id")
        #     if not image_id:
        #         # 增源
        #         config_mysql_old = get_mysql_old()
        #         db = pymssql.connect(**config_mysql_old)
        #         cursor = db.cursor()
        #         account_link = e(".tit").find('a').attr('href')
        #         homepage = self.s.get(account_link, cookies=self.cookies)
        #         # var biz = "MzU0MDUxMjM4OQ==" || ""
        #         biz_find = re.search('var biz = ".*?"', homepage.text)
        #         biz = ''
        #         if biz_find:
        #             biz = biz_find.group().replace('var biz = ', '')
        #         info["biz"] = biz
        #         try:
        #             sql_insert = """
        #                     INSERT INTO WXAccount(Name, Account, CollectionTime, Biz, Feature, Certification)
        #                     VALUES ('{}', '{}', GETDATE(), '{}', '{}', '{}')""".format(info.get('name'),
        #                                                                                info.get('account'),
        #                                                                                info.get('biz'),
        #                                                                                info.get('features'),
        #                                                                                info.get('certified'))
        #             cursor.execute(sql_insert)
        #             db.commit()
        #             log('插入数据成功', info.get('name'))
        #             log("当前账号id为0 需要添加{}".format(self.name))
        #         except Exception as e:
        #             log('插入数据错误', e)
        #             db.rollback()
        #             continue
        #         time.sleep(5)
        #         continue
        #         # add_account(name,info account, url, collectiontime, biz)
        #         # time.sleep(6)
        #         # find = get_account(account)
        #         # if not find:
        #         #     tinfoime.sleep(6)
        #         # Images/126767/126767400.jpg
        #     path = 'Images/' + str(image_id // 1000) + '/' + str(image_id)
        #     self.send_info(info, path)

            # 假设账号已存在
            # url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(self.name)
            # result1 = requests.get(url_public)
            # info_image = result1.json()
            # image_url = info_image.get("imageUrl")
            # image_id = info_image.get("id")
            # if image_url:
            #     # 有头像 判断图片有效 默认ID一定有
            #     # url2 = 'http://60.190.238.188:38016/{}'.format(image_url)
            #     url2 = 'http://183.131.241.60:38011/QueryWeChatImage?id={}'.format(image_id)
            #     r_img = requests.get(url2)
            #     if 'Images/0/0.jpg' in r_img.text:
            #         log('账号:{} 头像失效'.format(self.name))
            #
            #         # 保存图像
            #         self.handle_img(img_b, image_id, info, path)
            #         # url_img = 'http://47.99.50.93:8009/SaveImage'
            #         # data_img = {'content': base64.b64encode(img_b), 'account_id': image_id}
            #         # r = requests.post(url_img, data=data_img)
            #         # log('头像上传:', r.status_code)
            #     break
            # else:
            #     # 没有头像
            #     # 保存头像
            #     if info_image.get('id'):
            #         # url_save = 'http://183.131.241.60:38011/SaveImage/{}'.format(info_image.get('id'))
            #         # requests.post(url_save)
            #         log('保存头像')
            #         self.handle_img(img_b, image_id, info, path)
            #     break

    def account_homepage(self):
        # 搜索并进入公众号主页
        while True:
            search_url = self.url.format(self.name)
            referer = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=1565&sst0=1536470115264&lkt=0%2C0%2C0'.format(
                self.name)
            self.headers['Referer'] = referer
            self.url = 'http://weixin.sogou.com/weixin?query={}'.format(self.name)
            # self.url = 'http://weixin.sogou.com/weixin'
            # params = {
            #     'query': self.name
            # }
            resp_search = self.s.get(self.url, headers=self.headers, cookies=self.cookies)
            if '相关的官方认证订阅号' in resp_search.text:
                log("找不到该公众号: {}".format(self.name))
                break
            e = pq(resp_search.text)

            if self.name in e(".info").eq(0).text():
                account_link = e(".tit").find('a').attr('href')
                self.uploads_account_info(e)
            elif len(e(".tit").eq(0).text()) > 1:
                log("不能匹配正确的公众号: {}".format(self.name))
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
                # 被跳过的公众号要不要抓取  大概 4次
                continue
            account_match = re.search(r'微信号：\w*', e.text())
            account_search = account_match.group().replace('微信号：', '') if account_match else ''

            homepage = self.s.get(account_link, cookies=self.cookies)
            if '<title>请输入验证码 </title>' in homepage.text:
                self.crack_sougou(account_link)
                # log("出现验码")
                # log('------开始处理微信验证码------')
                # cert = random.random()
                # image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
                # respones = self.s.get(image_url, )
                # captch_input = captch_upload_image(respones.content)
                # log('------验证码：{}------'.format(captch_input))
                # data = {
                #     'cert': cert,
                #     'input': captch_input
                # }
                # respones = self.s.post(image_url, data=data, cookies=self.cookies)
                # self.cookies = requests.utils.dict_from_cookiejar(respones.cookies)
                # log('adffa', self.cookies)
                homepage = self.s.get(account_link, cookies=self.cookies)
                # log('破解验证码之后')
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

    def run(self):
        log("fadfsdf", self.cookies)
        html_account = self.account_homepage()
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
            # if page_count > 2:
            #     break
            article = Article()
            log('url:', url)
            article.create(url, self.name)
            log('文章标题:', article.title)
            log("第{}条".format(page_count))

            # 超过9天不管
            if article.time:
                article_date = datetime.datetime.fromtimestamp(int(article.time[:-3]))
                day_diff = datetime.datetime.now().date() - article_date.date()
                if day_diff.days > 6:
                    break

            entity = JsonEntity(article, account)
            backpack = Backpack()
            backpack.create(entity)
            backpack_list.append(backpack.create_backpack())

            # 所有文章
            article_info = backpack.to_dict()
            articles.append(article_info)

        content_all_list = ''
        for article in articles:
            content_all_list += article.get('Content')
        # with open('all_character.txt', 'w', encoding='utf-8') as f:
        #     f.write(content_all_list)
        # 分词处理

        key_words_list = []
        thu1 = thulac.thulac()
        seg_list = thu1.cut(''.join(content_all_list), text=False)
        for s in seg_list:
            if (
                    len(s[0]) >= 2
                    and re.search('[\u4e00-\u9fff]+', s[0])
                    and s[1] in ['n', 'np', 'ns', 'ni', 'nz']
            ):
                key_words_list.append(s[0])

        # 返回前10个出现频率最高的词
        key_words_counter = Counter(key_words_list).most_common(20)
        key_word = dict()
        key_word['list'] = []
        for k in key_words_counter:
            key_word['list'].append(
                {
                    "times": k[1],
                    "keyword": k[0]
                }
            )
        # 处理文章
        result = handle(articles)
        result['KeyWord'] = key_word

        # 正负判断
        with open('positive.txt', 'r', encoding='utf-8') as f:
            positive = f.read()
        with open('nagetive.txt', 'r', encoding='utf-8') as f:
            nagetive = f.read()
        # key_list = list(key_words_counter)
        log(len(Counter(key_words_list).most_common()))
        count_positive = 0
        count_nagetive = 0
        for key in Counter(key_words_list).most_common():
            k, c = key
            if k in positive.split('\n'):
                count_positive += c
                # log(k)

            if k in nagetive.split('\n'):
                count_nagetive += c
                # log('k2', k)
        log(count_positive)

        log(count_nagetive)
        result['ArtPosNeg'] = {'Indicate': {'Positive': count_positive, 'Negative': count_nagetive}}
        result['Success'] = True
        result['Account'] = self.name
        result['Message'] = ''

        log('====', self.name)
        db['newMedia'].update({'Account': self.name}, {'$set': {'data': result}})
        log('数据抓取完成')

        # 向前端发送成功请求
        # article_detaile = db['newMedia'].find_one({'Account': self.name})

        account_id = hash_md5(self.name)
        status_url = 'http://58.56.160.39:38012/MediaManager/api/drafts/updateAnalysisStatusByAnalysisId'
        params = {
            'type': 3,
            'analysisId': account_id,
            'status': 3,
        }
        r = requests.get(status_url, params=params)
        log('status_code', r.status_code)

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
                        # log('------输入验证码------')
                        # error_tips = self.wait.until(EC.presence_of_element_located((By.ID, 'error-tips'))).text
                        # if len(error_tips):
                        #     log('---1111111---验证码输入错误------')
                        #     return
                        # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'login-info')))
                        if '搜公众号' not in self.browser.page_source:
                            log('验证失败')
                            return
                        log('------验证码正确------')
                        # cookies = self.browser.get_cookies()
                        # new_cookie = {}
                        # for items in cookies:
                        #     new_cookie[items.get('name')] = items.get('value')
                        # self.cookies = new_cookie
                        # log('------cookies已更新------', self.cookies)
                        # return new_cookie
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
            respones = self.s.post(image_url, cookies=self.cookies, data=data)
            # self.cookies = requests.utils.dict_from_cookiejar(respones.cookies)
            log('------cookies已更新------')


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'

    @async
    def listen_task(self):
        account = AccountHttp()
        while True:
            account_char = self.rcon.brpop(self.queue, 0)[1]
            account.name = account_char.decode(encoding="utf-8")
            account.run()
            # if account.browser:
            #     account.browser.quit()
            log("消耗一个account")

    def prodcons(self, account):
        self.rcon.lpush(self.queue, account)
        log("lpush {} -- {}".format(self.queue, account))


@app.route('/')
def index():
    return 'hello world!'


@app.route('/WeiXinArt/AddAccount')
def add_account():
    account = request.args.get('account')
    task = Task()
    task.prodcons(account)
    _id = hash_md5(account)
    add_on = datetime.datetime.now()
    db['newMedia'].update({'id': _id}, {'$set': {'id': _id, 'Account': account, 'add_on': add_on}, }, True)
    return _id


@app.route('/WeiXinArt/PublishTimes')
def find_account():
    accountid = request.args.get('accountid')
    log('find', accountid)
    item = db['newMedia'].find_one({'id': accountid, })
    if item:
        result = item.get('data', 'catch unfinished')
        return json.dumps(result)
    else:
        error_result.update({'Message': "account not found"})
        return json.dumps(error_result)


if __name__ == '__main__':
    # t = Task()
    # t.listen_task()
    account = AccountHttp()
    t = AccountHttp()
    if t.browser:
        t.browser.close()
    t.listen_task(account)

    app.run(host='0.0.0.0', port=8008)
