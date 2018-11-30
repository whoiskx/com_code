# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
import time

import requests
import json

from lxml import etree

from pyquery import PyQuery as pq
from models import JsonEntity, Article, Account, Backpack, Ftp
from config import get_mysql_new, GETCAPTCHA_URL, mongo_conn, ADD_COLLECTION, GET_ACCOUNT_FROM_MYSQL, JUDEG
from utils import uploads_mysql, get_log, driver, get_captcha_path, time_strftime, save_name

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
from verification_code import captch_upload_image

current_dir = os.getcwd()
log = get_log('daily_collect')


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.search_name = ''
        self.tags = ''
        self.s = requests.Session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.106 Safari/537.36',
        }
        self.cookies = {'SUID': '4A72170E2613910A000000005BAC759D', 'ABTEST': '3|1538028956|v1', 'SUIR': '1538028956',
                        'IPLOC': 'CN4401', 'SNUID': '5960051C121665C656C04D9E13C88607',
                        'PHPSESSID': '80l6acdo9sq3uj357t00heqpg1', 'seccodeRight': 'success',
                        'SUV': '00F347B50E17724A5BAC759DBEFB6849', 'successCount': '1|Thu, 27 Sep 2018 06:20:59 GMT',
                        'refresh': '1', 'JSESSIONID': 'aaa73Xexaf2BmgEL80Bvw'}
        self.driver = driver
        self.driver.set_page_load_timeout(15)
        self.driver.set_script_timeout(15)
        self.wait = WebDriverWait(self.driver, 5)

    def account_homepage(self):
        # 搜索账号并返回公众号主页
        count = 0
        while True:
            count += 1
            if count > 3:
                log.info('多次账号异常，跳过账号:'.format(self.name))
                return
            log.info('start account {}'.format(self.search_name))
            search_url = self.url.format(self.search_name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)
            e = pq(resp_search.text)
            log.info('当前搜狗标题：{}'.format(e('title').text()))
            if '搜狗' not in e('title').text():
                log.info('初始化session')
                self.s = requests.session()
            if self.search_name == e(".info").eq(0).text().replace('微信号：', ''):
                account_link = e(".tit").find('a').attr('href')
                self.name = e(".tit").eq(0).text()
                homepage = self.s.get(account_link, cookies=self.cookies)
                if '<title>请输入验证码 </title>' in homepage.text:
                    self.crack_sougou(account_link)
                    homepage = self.s.get(account_link, cookies=self.cookies)
                return homepage.text
            elif len(e(".tit").eq(0).text()) > 1:
                log.info("不能匹配正确的公众号: {}".format(self.search_name))
                return
            if '相关的官方认证订阅号' in resp_search.text:
                log.info("找不到该公众号: {}".format(self.search_name))
                return
            if '搜狗' in e('title').text():
                log.info('{} :搜索结果无文字'.format(self.search_name))
                return
            else:
                # 处理验证码
                log.info(search_url)
                log.info('验证之前的cookie'.format(self.cookies))
                try_count = 0
                while True:
                    try_count += 1
                    self.crack_sougou(search_url)
                    if '搜公众号' in self.driver.page_source:
                        log.info('------开始更新cookies------')
                        cookies = self.driver.get_cookies()
                        new_cookie = {}
                        for items in cookies:
                            new_cookie[items.get('name')] = items.get('value')
                        self.cookies = new_cookie
                        log.info('------cookies已更新------'.format(self.cookies))
                        break
                    elif try_count > 4:
                        log.info("浏览器验证失败")
                        break
                log.info("验证完毕")
                time.sleep(2)
                continue

    @staticmethod
    def get_account():
        try:
            url = 'http://10.194.12.106:8002/GetWeixinTask?name=&name_array=&Name_word=&channel=&pageno=1&pagesize=12&local=False&token=082c5e82-a168-4c2e-a8e6-00760225c93a_wechat&page=1&rows=12&sort='
            resp = requests.get(url, timeout=30)
            data = json.loads(resp.text).get('weixin')
            account_list = []
            for account_info in data:
                account_list.append(account_info.get('account'))
            return account_list
        except Exception as e:
            log.info(e)

    @staticmethod
    def urls_article(html):
        collection_name = 'run_counts'
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
            # 有的文章链接被包含在里面，需再次匹配
            if 'content_url' in url:
                item = re.search('"content_url":".*?wechat_redirect', url).group()
                url = item[15:].replace('amp;', '')
            urls.append(url)
        return urls

    @staticmethod
    def save_to_mysql(entity):
        # 上传数据库
        # log.info('开始上传mysql')
        sql = '''   
                INSERT INTO 
                    account_http(article_url, addon, account, account_id, author, id, title) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)
        '''
        _tuple = (
            entity.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author,
            entity.id,
            entity.title
        )
        try:
            config_mysql = get_mysql_new()
            uploads_mysql(config_mysql, sql, _tuple)
        except Exception as e:
            log.info('数据库上传错误 {}'.format(e))
        # log.info('上传mysql完成')

    @staticmethod
    def save_to_mongo(entity):
        db = mongo_conn()
        entity['collection'] = time_strftime()
        db['daily_collection'].insert(entity)

    @staticmethod
    def create_xml(infos, file_name):
        # log.info('创建xml文件')
        if not os.path.exists(os.path.join(current_dir, 'xml')):
            os.mkdir('xml')
        data = etree.Element("data")
        for k, v in infos.items():
            sub_tag = etree.SubElement(data, k)
            if 'time' in k:
                sub_tag.text = v
                continue
            title_txt = str(v)
            title_txt = etree.CDATA(title_txt)
            sub_tag.text = title_txt
        # dataxml = etree.tostring(data, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=True,
        #                          standalone=None)
        # print(dataxml.decode("utf-8"))
        file_name = os.path.join(current_dir, 'xml', file_name)
        etree.ElementTree(data).write(file_name, encoding='utf-8', pretty_print=True)
        # log.info('完成xml文件')

    def get_tags(self):
        url = 'http://10.194.12.107:8002/GetTag?account={}'.format(self.search_name)
        resp = requests.get(url)
        log.info(resp.text)
        return resp.text

    @staticmethod
    def dedup(account_name):
        date_today = str(datetime.date.today().strftime('%Y%m%d'))
        bottom_url = 'http://60.190.238.178:38010/search/common/weixin/select?sort=Time%20desc&Account={}&rows=2000&starttime=20180430&endtime={}&fl=id,CrawlerType'.format(
            account_name, date_today)
        get_ids = requests.get(bottom_url, timeout=21)
        ids = get_ids.text
        if ids:
            results = json.loads(ids).get('results')
            for item in results:
                if item.get('CrawlerType') == '2' or item.get('CrawlerType') == 2:
                    replace_id = item.get('ID')
                    ids = ids.replace(replace_id, '____')
        return ids

    def run(self):
        count = 0
        while True:
            count += 1
            log.info('第{}次'.format(count))
            # ADD_COLLECTION 补采账号  get_account 日常采集； 使用account_list 兼容单个账号和账号列表
            account_list = ADD_COLLECTION if ADD_COLLECTION else self.get_account()
            if account_list is None:
                log.info('调度队列为空，休眠5秒')
                time.sleep(5)
            for account_name in account_list:
                try:
                    self.search_name = account_name
                    html_account = self.account_homepage()
                    if html_account:
                        html = html_account
                    else:
                        log.info('{}|找到不到微信号'.format(account_name))
                        continue
                    urls_article = self.urls_article(html)
                    # 确定account信息
                    account = Account()
                    account.name = self.name
                    account.account = account_name
                    account.tags = self.get_tags()
                    account.get_account_id()
                    if not account.account_id:
                        log.info('没有account_id'.format(self.name))
                        break
                    # 判重
                    ids = self.dedup(account_name) if JUDEG else ''
                    entity = None
                    backpack_list = []
                    ftp_list = []
                    ftp_info = None
                    for page_count, url in enumerate(urls_article):
                        # if page_count < 15:
                        #     continue
                        article = Article()
                        try:
                            article.create(url, account)
                        except RuntimeError as run_error:
                            log.info('找不到浏览器 {}'.format(run_error))
                        log.info('第{}条 文章标题: {}'.format(page_count, article.title))
                        log.info("当前文章url: {}".format(url))
                        entity = JsonEntity(article, account)
                        log.info('当前文章ID: {}'.format(entity.id))
                        if entity.id in ids and JUDEG is True:
                            log.info('当前文章已存在，跳过0')
                            # continue
                        backpack = Backpack()
                        backpack.create(entity)
                        backpack_list.append(backpack.create_backpack())
                        # self.save_to_mysql(entity)
                        # self.save_to_mongo(entity.to_dict())
                        # if page_count >= 3:
                        #     break
                    log.info("开始发包")
                    if entity and backpack_list:
                        entity.uploads(backpack_list)
                        log.info("发包完成")
                except Exception as e:
                    log.exception("解析公众号错误 {}".format(e))
                    if 'chrome not reachable' in str(e):
                        raise RuntimeError('chrome not reachable')
            # if ADD_COLLECTION:
            #     break

    def crack_sougou(self, url):
        log.info('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            log.info('------开始处理搜狗验证码------')
            self.driver.get(url)
            time.sleep(2)
            if '搜公众号' in self.driver.page_source:
                log.info('浏览器页面正常' + '直接返回')
                return
            try:
                img = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
                log.info('------出现验证码页面------')
                location = img.location
                size = img.size
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                screenshot = self.driver.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                captcha = screenshot.crop((left, top, right, bottom))
                captcha_path = get_captcha_path()
                captcha.save(captcha_path)
                captcha_name = os.path.basename(captcha_path)
                try:
                    captch_input = ''
                    files = {'img': (captcha_name, open(captcha_path, 'rb'), 'image/png', {})}
                    res = requests.post(url=GETCAPTCHA_URL, files=files)
                    res = res.json()
                    if res.get('Success'):
                        captch_input = res.get('Captcha')
                except Exception as e:
                    log.info('搜狗验证码获取失败'.format(e))
                    with open(captcha_path, "rb") as f:
                        filebytes = f.read()
                    captch_input = captch_upload_image(filebytes)
                    # log.info('------验证码：{}------'.format(captch_input))
                log.info('------验证码：{}------'.format(captch_input))
                if captch_input:
                    input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                    input_text.clear()
                    input_text.send_keys(captch_input)
                    submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                    submit.click()
                    time.sleep(2)
                    try:
                        if '搜公众号' not in self.driver.page_source:
                            log.info('验证失败')
                            return
                        log.info('------验证码正确------')
                    except Exception as e:
                        log.info('--22222222----验证码输入错误------ {}'.format(e))
            except Exception as e:
                log.info('------未跳转到验证码页面，跳转到首页，忽略------ {}'.format(e))

        elif re.search('mp\.weixin\.qq\.com', url):
            log.info('------开始处理微信验证码------')
            cert = random.random()
            image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
            respones = self.s.get(image_url, cookies=self.cookies)
            captch_input = captch_upload_image(respones.content)
            log.info('------验证码：{}------'.format(captch_input))
            data = {
                'cert': cert,
                'input': captch_input
            }
            r = self.s.post(image_url, cookies=self.cookies, data=data)
            log.info('------cookies已更新------{}'.format(r.status_code))


if __name__ == '__main__':
    # test = None
    while True:
        try:
            test = AccountHttp()
            log.info("初始化")
            test.run()
            if ADD_COLLECTION:
                log.info('补采完成')
                break
        except Exception as error:
            log.exception('获取账号错误，重启程序{}'.format(error))
        # finally: # 会导致程序崩溃
        #     driver.quit(