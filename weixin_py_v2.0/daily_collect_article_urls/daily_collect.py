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
from config import get_mysql_new, GetCaptcha_url, mongo_conn, ADD_COLLECTION
from utils import uploads_mysql, get_log, driver, get_captcha_path, time_strftime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from PIL import Image
from io import BytesIO
from verification_code import captch_upload_image

current_dir = os.getcwd()

log = get_log('daily_collect').info


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.search_name = ''
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
                log('多次账号异常，跳过账号:'.format(self.name))
                return
            log('start account {}'.format(self.search_name))
            search_url = self.url.format(self.search_name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)
            e = pq(resp_search.text)
            log('当前搜狗标题：{}'.format(e('title').text()))
            if '搜狗' not in e('title').text():
                log('初始化session')
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
                log("不能匹配正确的公众号: {}".format(self.search_name))
                return
            if '相关的官方认证订阅号' in resp_search.text:
                log("找不到该公众号: {}".format(self.search_name))
                return
            else:
                # 处理验证码
                log(search_url)
                log('验证之前的cookie'.format(self.cookies))
                try_count = 0
                while True:
                    try_count += 1
                    self.crack_sougou(search_url)
                    if '搜公众号' in self.driver.page_source:
                        log('------开始更新cookies------')
                        cookies = self.driver.get_cookies()
                        new_cookie = {}
                        for items in cookies:
                            new_cookie[items.get('name')] = items.get('value')
                        self.cookies = new_cookie
                        log('------cookies已更新------'.format(self.cookies))
                        break
                    elif try_count > 4:
                        log("浏览器验证失败")
                        break
                log("验证完毕")
                time.sleep(2)
                continue

    @staticmethod
    def account_list():
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
        account_all = []
        try:
            url = 'http://183.131.241.60:38011/nextaccount?label=5'
            resp = requests.get(url, timeout=21)
            items = json.loads(resp.text)
            if len(items) == 0:
                return []
            for item in items:
                account_all.append(item.get('account'))
            log("开始account列表 {}".format(account_all))
        except Exception as e:
            log('获取账号列表错误 {}'.format(e))
            time.sleep(5)
        return account_all

    @staticmethod
    def urls_article(html):
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
        db = mongo_conn()
        result = db['count'].find()
        if result.count() == 0:
            db['count'].insert({'article_count': count_article})
        else:
            for item in db['count'].find():
                count = item.get('article_count') + count_article
                db['count'].update({'article_count': item.get('article_count')},
                                   {'$set': {'article_count': count}}, upsert=True)
        return urls

    @staticmethod
    def save_to_mysql(entity):
        # 上传数据库
        # log('开始上传mysql')
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
            log('数据库上传错误 {}'.format(e))
        # log('上传mysql完成')

    @staticmethod
    def save_to_mongo(entity):
        db = mongo_conn()
        entity['collection'] = time_strftime()
        db['daily_collection'].insert(entity)

    @staticmethod
    def create_xml(infos, file_name):
        # log('创建xml文件')
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
        # log('完成xml文件')

    @staticmethod
    def dedup(account_name):
        date_today = str(datetime.date.today().strftime('%Y%m%d'))
        bottom_url = 'http://60.190.238.178:38010/search/common/weixin/select?sort=Time%20desc&Account={}&rows=2000&starttime=20180430&endtime={}&fl=id'.format(
            account_name,
            date_today)
        get_ids = requests.get(bottom_url, timeout=21)
        ids = get_ids.text
        return ids

    def run(self):
        try:
            urls_article = [
                'https://mp.weixin.qq.com/s?src=11&timestamp=1541559601&ver=1229&signature=ixTsG-RvK8H58t6D-CpW6olWI8hA52Wz-FRb12ZcrNG-lxR20YutoyLYUr-RB3w8WHjE1petjDcbbxZVxTChvPWM27qszWu0Z3zonjx8SEQB5mmgm1O9Eu*5qsFhnBCH&new=1'
            ]
            entity = None
            backpack_list = []
            ftp_list = []
            ftp_info = None
            for page_count, url in enumerate(urls_article):
                # if page_count < 15:
                #     continue
                html = requests.get(url)
                # 确定account信息
                name = pq(html.text)('#js_name').text()
                account_name = pq(html.text)('.profile_meta_value').eq(0).text()
                log('---{}---{}---'.format(name, account_name))
                account = Account()
                account.name = name
                account.account = account_name
                account.get_account_id()
                article = Article()
                try:
                    article.create(url, account)
                except RuntimeError as run_error:
                    log('找不到浏览器 {}'.format(run_error))
                log('第{}条 文章标题: {}'.format(page_count, article.title))
                log("当前文章url: {}".format(url))
                entity = JsonEntity(article, account)
                log('当前文章ID: {}'.format(entity.id))
                # if entity.id in ids:
                #     log('当前文章已存在，跳过')
                #     continue
                backpack = Backpack()
                backpack.create(entity)
                backpack_list.append(backpack.create_backpack())
                # self.save_to_mysql(entity)
                self.save_to_mongo(entity.to_dict())
                # ftp包
                ftp_info = Ftp(entity)
                name_xml = ftp_info.hash_md5(ftp_info.url)
                log('当前文章xml: {}'.format(name_xml))
                self.create_xml(ftp_info.ftp_dict(), name_xml)
                ftp_list.append(name_xml)
                # if page_count >= 3:
                #     break
            log("发包")
            # todo 发包超时，修改MTU
            if ftp_info is not None:
                entity.uploads_ftp(ftp_info, ftp_list)
            if entity:
                # entity.uploads(backpack_list)
                entity.uploads_datacenter_relay(backpack_list)
                entity.uploads_datacenter_unity(backpack_list)
            log("发包完成")
        except Exception as e:
            log("解析公众号错误 {}".format(e))
            if 'chrome not reachable' in str(e):
                raise RuntimeError('chrome not reachable')
                # break

    def crack_sougou(self, url):
        log('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            log('------开始处理搜狗验证码------')
            self.driver.get(url)
            time.sleep(2)
            if '搜公众号' in self.driver.page_source:
                log('浏览器页面正常' + '直接返回')
                return
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
                captcha_path = get_captcha_path()
                captcha.save(captcha_path)
                captcha_name = os.path.basename(captcha_path)
                try:
                    captch_input = ''
                    files = {'img': (captcha_name, open(captcha_path, 'rb'), 'image/png', {})}
                    res = requests.post(url=GetCaptcha_url, files=files)
                    res = res.json()
                    if res.get('Success'):
                        captch_input = res.get('Captcha')
                except Exception as e:
                    log('搜狗验证码获取失败'.format(e))
                    with open(captcha_path, "rb") as f:
                        filebytes = f.read()
                    captch_input = captch_upload_image(filebytes)
                    # log('------验证码：{}------'.format(captch_input))
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
                    except Exception as e:
                        log('--22222222----验证码输入错误------ {}'.format(e))
            except Exception as e:
                log('------未跳转到验证码页面，跳转到首页，忽略------ {}'.format(e))

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


if __name__ == '__main__':
    # test = None
    # while True:
    try:
        test = AccountHttp()
        test.run()
    except Exception as error:
        log('获取账号错误，重启程序{}'.format(error))
    finally:
        driver.quit()
