# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
import time
import threading
import multiprocessing
from multiprocessing import Pool

import requests
import json

from lxml import etree
from pyquery import PyQuery as pq
from selenium import webdriver

from models import JsonEntity, Article, Account, Backpack, Ftp
from config import get_mysql_new, GETCAPTCHA_URL, mongo_conn, ADD_COLLECTION, GET_ACCOUNT_FROM_MYSQL, JUDEG
from utils import uploads_mysql, get_log, get_captcha_path, time_strftime, save_name, abuyun_proxy, \
    captch_upload_image

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from PIL import Image
from io import BytesIO

# from verification_code import captch_upload_image

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
        self.cookies = {}

        # 使用单一driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # self.driver = driver
        self.driver.set_page_load_timeout(20)
        self.driver.set_script_timeout(20)
        self.wait = WebDriverWait(self.driver, 5)
        self.proxies = abuyun_proxy()

    def account_homepage(self):
        # 搜索账号并返回公众号主页
        count = 0
        while True:
            count += 1
            if count > 25:
                log.info('多次账号异常，跳过账号:{}'.format(self.name))
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
                # 从搜狗页面获取微信历史页
                account_link = e(".tit").find('a').attr('href')
                self.name = e(".tit").eq(0).text()
                count_proxy = 0
                while True:
                    if self.proxies is False:
                        homepage = self.s.get(account_link, cookies=self.cookies)
                        loop_count = 0
                        while True:
                            loop_count += 1
                            if loop_count >= 4:
                                log.info('微信历史页多次验证失败{}'.format(self.search_name))
                                break
                            if '<title>请输入验证码 </title>' in homepage.text:
                                self.crack_sougou(account_link)
                                homepage = self.s.get(account_link)
                            else:
                                break
                        return homepage.text
                    count_proxy += 1
                    if count_proxy > 100:
                        log.error('未能获取有效代理:账号退出{}'.format(self.search_name))
                        return
                    try:
                        log.info('当前代理 {}'.format(self.proxies))
                        homepage = self.s.get(account_link, cookies=self.cookies, proxies=self.proxies)
                        if '<title>请输入验证码 </title>' in homepage.text:
                            # write(homepage.text)
                            log.info('历史页需要输入验证码，重新获取代理 {}'.format(count_proxy))
                            self.proxies = abuyun_proxy()
                            continue
                        else:
                            return homepage.text
                    except Exception as _e:
                        log.info('使用代理异常:{}'.format(_e))
                        self.proxies = abuyun_proxy()

                # if '<title>请输入验证码 </title>' in homepage.text:
                #     # self.crack_sougou(account_link)
                #     count_proxy = 0
                #     while True:
                #         count_proxy += 1
                #         if count_proxy > 5:
                #             break
                #         try:
                #             log.info(self.proxies)
                #             homepage = self.s.get(account_link, cookies=self.cookies, proxies=self.proxies)
                #             break
                #         except Exception as e:
                #             log.info('重新获取代理:{}'.format(e))
                #             self.proxies = abuyun_proxy()
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
                # while True:
                #     try_count += 1
                # lock.acquire()
                self.crack_sougou(search_url)
                # lock.release()
                # if lock.acquire():
                #     try:
                #         self.crack_sougou(search_url)
                #     except Exception as e:
                #         log.info(e)
                #     finally:
                #         lock.release()
                # if '搜公众号' in self.driver.page_source:
                log.info('------开始更新cookies------')
                cookies = self.driver.get_cookies()
                new_cookie = {}
                for items in cookies:
                    new_cookie[items.get('name')] = items.get('value')
                self.cookies = new_cookie
                log.info('------cookies已更新------'.format(self.cookies))
                # break
                # elif try_count > 4:
                #     log.info("浏览器验证失败")
                #     break
                # log.info("验证完毕")
                # time.sleep(2)
                # continue

    @staticmethod
    def get_account():
        # 老版
        # url = 'http://124.239.144.181:7114/Schedule/dispatch?type=8'
        # # url = 'http://183.131.241.60:38011/nextaccount?label=5'
        # resp = requests.get(url, timeout=30)
        # # data 可能为空
        # data_json = resp.text.get('data')
        # data = json.loads(data_json)
        # self.search_name = data.get('name')
        # print(self.search_name)
        # return self.search_name
        # 重点采集接口
        # account_all = []
        # try:
        #     url = 'http://183.131.241.60:38011/nextaccount?label=5'
        #     resp = requests.get(url, timeout=21)
        #     items = json.loads(resp.text)
        #     if len(items) == 0:
        #         return []
        #     for item in items:
        #         account_all.append(item.get('account'))
        #     log.info("开始account列表 {}".format(account_all))
        # except Exception as e:
        #     log.info('获取账号列表错误 {}'.format(e))
        #     time.sleep(5)
        # 统计账号
        collection_name = 'run_counts'
        try:
            url = 'http://dispatch.yunrunyuqing.com:38082/ScheduleDispatch/dispatch?type=8'
            resp = requests.get(url, timeout=30)
            data = json.loads(resp.text).get('data')
            if not data:
                # 即返回None
                return
            account = json.loads(data).get('account')
            db = mongo_conn()
            result = db[collection_name].find({})
            if result.count() == 0:
                db[collection_name].insert({'account_count': 1, 'article_count': 0,
                                            'start': time_strftime(), 'end': None, 'save_name': save_name()})
                log.info("插入mongo成功")
            else:
                updated = False
                for item in db[collection_name].find():
                    if item.get('save_name') == save_name():
                        count = item.get('account_count') + 1  # if item.get('account_count') else 0
                        log.info(item)
                        db[collection_name].update({'save_name': save_name()},
                                                   {'$set': {'account_count': count, 'end': time_strftime()}},
                                                   upsert=True)
                        updated = True
                        log.info("更新mongo成功")
                        break
                if updated is False:
                    log.info('找不到save_name，需要插入')
                    db[collection_name].insert({'account_count': 1, 'article_count': 0,
                                                'start': time_strftime(), 'end': None, 'save_name': save_name()})
                    log.info("插入mongo成功")
        except Exception as e:
            log.info('调度获取account出错：{}'.format(e))
            return None
        return [account]

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
        # 统计文章数量
        count_article = len(urls)
        log.info('文章数量:{}'.format(count_article))
        try:
            if count_article == 0:
                return urls
            db = mongo_conn()
            result = db[collection_name].find({})
            if result.count() == 0:
                db[collection_name].insert({'save_name': save_name(), 'account_count': 1, 'article_count': 0,
                                            'start': time_strftime(), 'end': None})
                log.info('插入文章数成功')
            for item in db[collection_name].find():
                if item.get('save_name') == save_name():
                    count = count_article + item.get('article_count') if item.get('article_count') else count_article
                    db[collection_name].update({'save_name': save_name()},
                                               {'$set': {'article_count': count}}, upsert=True)
                    log.info('更新文章数量成功')
        except Exception as e:
            log.exception(e)
        return urls

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
        # 获取标签
        url = 'http://183.131.241.60:38011/GetTag?account={}'.format(self.search_name)
        resp = requests.get(url, timeout=30)
        log.info('账号: {} 获取标签结果：{}'.format(self.search_name, resp.text))
        return resp.text

    @staticmethod
    def dedup(account_name):
        date_today = str(datetime.date.today().strftime('%Y%m%d'))
        bottom_url = 'http://60.190.238.178:38010/search/common/weixin/select?sort=Time%20desc&Account={}&rows=2000&starttime=20181101&endtime={}&fl=id,CrawlerType'.format(
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
            # ADD_COLLECTION 补采账号  get_account 日常采集； 使用account_list 兼容单个账号和账号列表
            account_list = ADD_COLLECTION if ADD_COLLECTION else self.get_account()
            # length = len(threading.enumerate())  # 枚举返回个列表
            log.info('当前运行的线程数为：{}'.format(threading.active_count()))
            log.info('当前运行的进程：{}'.format(multiprocessing.current_process().name))
            count += 1
            log.info('第{}次'.format(count))
            if account_list is None:
                log.info('调度队列为空，休眠5秒')
                time.sleep(5)
                continue
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
                    # 判重
                    ids = self.dedup(account_name) if JUDEG else ''
                    entity = None
                    backpack_list = []
                    ftp_list = []
                    ftp_info = None
                    for page_count, url in enumerate(urls_article):
                        try:
                            article = Article()
                            article.create(url, account, self.proxies)

                            log.info('第{}条 文章标题: {}'.format(page_count, article.title))
                            log.info("当前文章url: {}".format(url))
                            entity = JsonEntity(article, account)
                            log.info('当前文章ID: {}'.format(entity.id))

                            article_date = datetime.datetime.fromtimestamp(int(str(article.time)[:-3]))
                            day_diff = datetime.date.today() - article_date.date()
                            if day_diff.days >= 6:
                                log.info('超过7天的文章不采集')
                                break
                            if entity.id in ids and JUDEG is True:
                                log.info('当前文章已存在，跳过')
                                # if page_count >= 20:
                                #     log.info('超过20篇文章，跳出')
                                #     break
                                continue
                            backpack = Backpack()
                            backpack.create(entity)
                            backpack_list.append(backpack.create_backpack())
                            # self.save_to_mysql(entity)
                            # self.save_to_mongo(entity.to_dict())
                            # ftp包
                            ftp_info = Ftp(entity)
                            name_xml = ftp_info.hash_md5(ftp_info.url)
                            log.info('当前文章xml: {}'.format(name_xml))
                            self.create_xml(ftp_info.ftp_dict(), name_xml)
                            ftp_list.append(name_xml)
                        except Exception as run_error:
                            log.info('微信解析文章错误 {}'.format(run_error))
                            continue
                    log.info("开始发包")
                    # todo 发包超时，修改MTU
                    if ftp_info is not None:
                        entity.uploads_ftp(ftp_info, ftp_list)
                        log.info("ftp发包完成")
                    if entity and backpack_list:
                        # entity.uploads(backpack_list)
                        entity.uploads_datacenter_relay(backpack_list)
                        entity.uploads_datacenter_unity(backpack_list)
                        log.info("数据中心，三合一，发包完成")
                except Exception as e:
                    log.exception("解析公众号错误 {}".format(e))
                    if 'chrome not reachable' in str(e):
                        raise RuntimeError('chrome not reachable')
            if ADD_COLLECTION:
                break

    def crack_sougou(self, url):
        log.info('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            log.info('------开始处理搜狗验证码------')
            self.driver.get(url)
            time.sleep(6)
            if '搜公众号' in self.driver.page_source:
                log.info('浏览器页面正常' + '直接返回')
                log.info('title {}'.format(self.driver.title))
                return
            # test
            # while True:
            #     for i in range(30):
            #         self.driver.get(url)
            #         if '搜公众号' in self.driver.page_source:
            #             log.info('浏览器页面正常' + '直接返回')
            #             log.info('title{}'.format(self.driver.title))
            #             continue
            #         else:
            #             break
            #
            #         time.sleep(0.3)
            #     if '搜公众号' in self.driver.page_source:
            #         log.info('浏览器页面正常' + '直接返回')
            #         log.info('title{}'.format(self.driver.title))
            #         continue
            #     break
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
                    # raise RuntimeError
                    captch_input = ''
                    files = {'img': (captcha_name, open(captcha_path, 'rb'), 'image/png', {})}
                    res = requests.post(url=GETCAPTCHA_URL, files=files, timeout=30)
                    res = res.json()
                    if res.get('Success'):
                        captch_input = res.get('Captcha')
                except Exception as e:
                    log.info('本地识别搜狗验证码获取异常，使用打码平台：{}'.format(e))
                    with open(captcha_path, "rb") as f:
                        filebytes = f.read()
                    captch_input = captch_upload_image(filebytes)
                    # log.info('------验证码：{}------'.format(captch_input))
                log.info('------验证码：{}------'.format(captch_input))
                if captch_input:
                    input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                    input_text.clear()
                    input_text.send_keys(captch_input)
                    time.sleep(1)

                    # from selenium.webdriver.common.keys import Keys
                    # self.driver.find_element_by_id("submit").send_keys(Keys.ENTER)
                    # log.info(driver.find_element_by_id("submit"))
                    #
                    # log.info('已经点击元素')
                    submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                    # time.sleep(1)
                    # self.driver.save_screenshot("click_after.png")
                    submit.click()
                    time.sleep(2)
                    # self.driver.save_screenshot("click_before.png")
                    # try:
                    if '搜公众号' not in self.driver.page_source:
                        # log.info('当前页面{}'.format(self.driver.page_source))
                        log.info('搜公众号 不在页面中验证失败')
                        log.info('title{}'.format(self.driver.title))
                        return
                    log.info('------验证码正确------')
                    # except Exception as e:
                    #     log.info('--22222222----验证码输入错误------ {}'.format(e))
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


def main():
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
            if test.driver:
                test.driver.quit()
                # log.info('当前浏览器已关闭')
                # chrome_options = webdriver.ChromeOptions()
                # chrome_options.add_argument('--headless')
                # test.driver = webdriver.Chrome(chrome_options=chrome_options)


def thread_main():
    thread_list = []
    lock = threading.Lock()

    for i in range(2):
        t = threading.Thread(target=main)
        t.start()
        time.sleep(5)
        thread_list.append(t)

    for t in thread_list:
        t.join()
    log.info('完成')


if __name__ == '__main__':
    # 多线程版
    # thread_list = []
    # lock = threading.Lock()
    #
    # for i in range(5):
    #     t = threading.Thread(target=main)
    #     t.start()
    #     time.sleep(5)
    #     thread_list.append(t)
    #
    # for t in thread_list:
    #     t.join()
    # log.info('完成')

    # main()

    log.info("The number of CPU is:" + str(multiprocessing.cpu_count()))
    proces_list = []
    for i in range(4):
        proc = multiprocessing.Process(target=thread_main)
        proc.start()
        time.sleep(5)
        proces_list.append(proc)
    for p in proces_list:
        p.join()
    log.info('完成')
    # 使用进程池  结果单一进程运行
    # p = Pool(4)
    # for i in range(5):
    #     p.apply_async(main)
    # print('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    # log.info('完成')
