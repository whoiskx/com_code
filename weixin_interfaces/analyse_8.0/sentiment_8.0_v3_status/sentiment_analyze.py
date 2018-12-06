# -*- coding: utf-8 -*-
import base64
import pymssql

import redis
from flask import Flask, request
from utils import async, hash_md5, time_strftime
import datetime
import random
import re
import time
import requests
import json
from pyquery import PyQuery as pq
from models import JsonEntity, Article, Account, Backpack
from config import get_mysql_new, get_mysql_old, GetCaptcha_url, GETNER_API_URL, mongo_conn_sentiment, error_result
from utils import log
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

config_mysql = get_mysql_new()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
CAPTCHA_NAME = 'captcha.png'

app = Flask(__name__)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# 多线程driver共享
driver = webdriver.Chrome(chrome_options=chrome_options)


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
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # # 多线程driver共享
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 4)
        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'
        self.status = 4

    @async
    def listen_task(self):
        while True:
            try:
                if not self.driver:
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument('--headless')
                    self.driver = webdriver.Chrome(chrome_options=chrome_options)
                account_char = self.rcon.brpop(self.queue, 0)[1]
                self.name = account_char.decode(encoding="utf-8")
                self.run()
                log("消耗一个account")
            except Exception as e:
                log('error', '重启', e)
                if self.driver:
                    self.driver.quit()
                continue

    def send_info(self, info):
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
        info['message'] = True
        info['status'] = 1

        # 获取头像二进制
        img_find = e(".img-box").find('img').attr('src')
        url_img_get = 'http:' + img_find
        info['ImageUrl'] = url_img_get
        return info
        # self.send_info(info)

    def account_homepage(self, choice=''):
        # 搜索并进入公众号主页
        count = 0
        while True:
            count += 1
            if count > 3:
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
                if choice:
                    account_info = self.uploads_account_info(e)
                    return account_info
                account_link = e(".tit").find('a').attr('href')
                # self.uploads_account_info(e)
                homepage = self.s.get(account_link, cookies=self.cookies)
                if '<title>请输入验证码 </title>' in homepage.text:
                    self.crack_sougou(account_link)
                    homepage = self.s.get(account_link, cookies=self.cookies)
                return homepage.text, self.name
            elif len(e(".tit").eq(0).text()) > 1:
                log("不能匹配正确的公众号: {}".format(self.name))
                break
            if '相关的官方认证订阅号' in resp_search.text:
                log("搜狗找不到该公众号: {}".format(self.name))
                return '搜狗无该账号', self.name
            else:
                log('url cookie 失效', search_url)
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
            url = 'https://mp.weixin.qq.com' + url_last
            # 部分是永久链接
            if '_biz' in url_last:
                url = re.search('http://mp.weixin.qq.*?wechat_redirect', url_last).group()
                urls.append(url)
                continue
            # 可能匹配过多，再次匹配
            if 'content_url' in url:
                item = re.search('"content_url":".*?wechat_redirect', url).group()
                url = item[15:].replace('amp;', '')
            urls.append(url)
        return urls

    def emotion_judge(self, content):
        key_words_list = []
        seg_list = jieba.cut(content)
        for s in seg_list:
            if re.search('[\u4e00-\u9fff]+', s):
                key_words_list.append(s)
        # log(key_words_list)
        with open('positive.txt', 'r', encoding='utf-8') as f:
            positive = f.read()
        with open('nagetive.txt', 'r', encoding='utf-8') as f:
            nagetive = f.read()
        # key_list = list(key_words_counter)
        count_positive = 0
        count_nagetive = 0
        for key in key_words_list:
            if key in positive.split('\n'):
                count_positive += 1
            if key in nagetive.split('\n'):
                count_nagetive += 1
        return count_positive, count_nagetive

    def send_result(self):
        # 向前端发送成功请求
        # article_detaile = db['newMedia'].find_one({'Account': self.name})
        try:
            log("发前端")
            account_id = hash_md5(self.name)
            status_url = 'http://58.56.160.39:38012/MediaManager/api/drafts/updateAnalysisStatusByAnalysisId'
            params = {
                'type': 3,
                'analysisId': account_id,
                # 3 成功 4 失败
                'status': self.status,
            }
            r = requests.get(status_url, params=params)
            log('status_code', r.status_code)
        except Exception as e:
            log("发送前端结果错误", e)

    def run(self, name, choice=''):
        # choice 选择是返回账号主体信息（True） or 分析结果('')
        self.name = name
        html_account = self.account_homepage(choice)
        # 返回账户信息
        if choice:
            return html_account
        if html_account:
            html, account_of_homepage = html_account
        else:
            # self.send_result()
            return
        log('start 公众号: ', self.name)
        urls_article = self.urls_article(html)

        account = Account()
        account.name = self.name
        account.account = account_of_homepage
        account.get_account_id()

        articles = []
        backpack_list = []
        positive_article = 0
        nagetive_article = 0
        for page_count, url in enumerate(urls_article):
            # if page_count > 2:
            #     break
            article = Article()
            log('url:', url)
            article.create(url, self.name)
            log('文章标题:', article.title)
            log("第{}条".format(page_count))

            # 超过7天不管
            if article.time:
                article_date = datetime.datetime.fromtimestamp(int(article.time[:-3]))
                day_diff = datetime.datetime.now().date() - article_date.date()
                if day_diff.days > 6:
                    break
            # 统计文章正负面
            count_positive, count_nagetive = self.emotion_judge(article.content)
            if count_positive > count_nagetive:
                positive_article += 1
            else:
                nagetive_article += 1
            entity = JsonEntity(article, account)
            backpack = Backpack()
            backpack.create(entity)
            backpack_list.append(backpack.create_backpack())
            # 所有文章
            article_info = backpack.to_dict()
            articles.append(article_info)
        log('所有文章抓取完毕')
        content_all_list = ''
        for article in articles:
            content_all_list += article.get('Content')
        log('文章长度', len(content_all_list))
        # 分词处理
        key_words_list = []
        data = {
            "texts": [content_all_list],
        }
        log('请求分词')
        response = requests.post(url=GETNER_API_URL, data=data, timeout=180)
        ner_result = response.json().get('rst')[0]
        if ner_result.get('status') == 'success':
            org_dic = ner_result.get('ner').get('ORG')
            loc_dic = ner_result.get('ner').get('LOC')
            per_dic = ner_result.get('ner').get('PER')
            if org_dic:
                for i in org_dic.items():
                    key_words_list.append(i)
            if loc_dic:
                for i in loc_dic.items():
                    key_words_list.append(i)
            if per_dic:
                for i in per_dic.items():
                    key_words_list.append(i)

        # 返回前20个出现频率最高的词
        key_words = dict()
        key_words['list'] = []
        key_words_list = sorted(key_words_list, key=lambda x: x[1], reverse=True)[:21]
        for k in key_words_list:
            key_words['list'].append(
                {
                    "times": k[1],
                    "keyword": k[0]
                }
            )
        log('分词完成')
        # 处理文章
        result = handle(articles)
        result['KeyWord'] = key_words
        result['ArtPosNeg'] = {'Indicate': {'Positive': positive_article, 'Negative': nagetive_article}}
        result['Success'] = True
        result['Account'] = self.name
        result['Message'] = 'Successful'
        mongo_conn_sentiment().update_one({'Account': self.name},
                                          {'$set': {'Addon': time_strftime(), 'Message': 'Successful', 'Data': result}},
                                          upsert=True)
        log('{} 抓取完成'.format(self.name))
        return result

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
                try:
                    captch_input = ''
                    files = {'img': (CAPTCHA_NAME, open(captcha_path, 'rb'), 'image/png', {})}
                    res = requests.post(url=GetCaptcha_url, files=files)
                    res = res.json()
                    if res.get('Success'):
                        captch_input = res.get('Captcha')
                except Exception as e:
                    log('搜狗验证码验证错误', e)
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
                log(e)
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
            log('------微信验证码处理完成------')


@app.route('/')
def index():
    return 'hello world!'


@app.route('/WeiXinArt/WeiXinInfo')
def info_account():
    name = request.args.get('account')
    account = AccountHttp()
    data = account.run(name, choice=' ')
    return json.dumps(data)


@app.route('/WeiXinArt/WeiXinAdvanceParse')
def advance_find_account():
    name = request.args.get('account')
    account = AccountHttp()
    data = account.run(name)
    return json.dumps(data)


def uploads_status(uploads_id):
    # 分析成功调用
    log('上传ID {}'.format(uploads_id))
    url = 'http://api.test.yunrunyuqing.com:38016/rapidAnalysis/dist/index.html#!/%E6%96%B0%E9%97%BB%E4%BC%A0%E6%92%AD%E5%88%86%E6%9E%90/newsUpdate'
    data = {
        'id': uploads_id,
        'status': '1',
    }
    r = requests.post(url, data=data)
    log('上传结果 {}'.format(r.status_code))


@app.route('/WeiXinArt/WeiXinParse')
def find_account():
    name = request.args.get('account')
    uploads_id = int(request.args.get('id')) if request.args.get('id') else -112313
    search_account = mongo_conn_sentiment().find_one({'Account': name})
    if search_account is not None and search_account.get('Addon') == time_strftime():
        if uploads_id != -112313:
            uploads_status(uploads_id)
        return json.dumps(search_account.get('Data'))
    account = AccountHttp()
    data = account.run(name)
    log('find', name)
    if data:
        analyse_result = dict()
        analyse_result['Success'] = data.get('Success')
        analyse_result['Account'] = data.get('Account')
        analyse_result['Message'] = data.get('Message')
        analyse_result['count'] = data.get('count')
        analyse_result['ArtPubInfo'] = data.get('ArtPubInfo')
        analyse_result['ActiveDegree'] = data.get('ActiveDegree')
        analyse_result['KeyWord'] = data.get('KeyWord')
        analyse_result['ArtPosNeg'] = data.get('ArtPosNeg')
        if uploads_id != -112313:
            uploads_status(uploads_id)
        return json.dumps(analyse_result)
    error_result.update({'Message': "account can't analyze"})
    return json.dumps(error_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10004, threaded=True)
    # uploads_status(10086)