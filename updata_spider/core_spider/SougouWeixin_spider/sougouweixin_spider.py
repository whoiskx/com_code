# -*- coding: utf-8 -*-
import os
import sys
import re
import json
import uuid
import time
import hashlib
import random
import threading
import requests
import datetime
import urllib.parse
from io import BytesIO
from PIL import Image
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from ftp_util import my_ftp
from sqlserver_util import my_sqlserver
from captch_dytry import captch_upload_image

print = logger.info


class SougouWeixin(object):
    def __init__(self, url, crawl_no=0):
        # 进程序号
        self.crawl_no = crawl_no

        self.url = url
        # 当前关键词查询缓存列表
        self.key_cache_single = []
        # 已查到的微信号字典
        self.account_find_all = {}
        # 该新闻关键词查询下有多少条新闻
        self.news_totals_all = 0
        # 已请求次数
        self.requests_totals_all = 0

        # 代理服务器配置
        self.proxies = {}

        # requests相关配置:搜狗
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(UA_POOL),
        }

        self.s = requests.session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.cookies = {}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(10)
        self.browser.set_script_timeout(10)
        self.wait = WebDriverWait(self.browser, 3)

    # 处理验证码
    def crack_sougou(self, url):
        # 是否处理验证码
        if CAPTCHA_ENABLED:
            print('------开始处理未成功的URL：{}'.format(url))
            if re.search('weixin\.sogou\.com/antispider', url):
                print('出现验证码：session重新初始化...')
                self.s = requests.session()
                print('------开始处理搜狗验证码------')
                try:
                    self.browser.get(url)
                    time.sleep(2)
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
                    captcha_name = re.sub('0', str(self.crawl_no), CAPTCHA_NAME)
                    captcha_path = os.path.join(IMAGE_DIR, captcha_name)
                    captcha.save(captcha_path)
                    captch_input = ''
                    if GETCAPTCHA_TYPE == 1:
                        with open(captcha_path, "rb") as f:
                            filebytes = f.read()
                        captch_input = captch_upload_image(filebytes)
                    elif GETCAPTCHA_TYPE == 2:
                        files = {'img': (captcha_name, open(captcha_path, 'rb'), 'image/png', {})}
                        get_captcha_ok = 0
                        try:
                            res = requests.post(url=GetCaptcha_URL_main, files=files, timeout=5)
                            res = res.json()
                            if res.get('Success'):
                                get_captcha_ok = 1
                                captch_input = res.get('Captcha')
                        except Exception as e:
                            print('验证码接口请求失败：{}...{}'.format(GetCaptcha_URL_main, e))
                            logger.error('验证码接口请求失败：{}...{}'.format(GetCaptcha_URL_main, e))
                        if get_captcha_ok == 0:
                            try:
                                res = requests.post(url=GetCaptcha_URL_backup, files=files, timeout=5)
                                res = res.json()
                                if res.get('Success'):
                                    captch_input = res.get('Captcha')
                            except Exception as e:
                                print('备用：验证码接口请求失败：{}...{}'.format(GetCaptcha_URL_backup, e))
                                logger.error('备用：验证码接口请求失败：{}...{}'.format(GetCaptcha_URL_backup, e))

                    print('------验证码{}：{}------'.format(captcha_name, captch_input))
                    if captch_input:
                        input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                        input_text.clear()
                        input_text.send_keys(captch_input)
                        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                        submit.click()
                        print('------输入验证码------')
                        time.sleep(1)
                        new_cookie = {}
                        if re.search('login-info', self.browser.page_source):
                            print('------验证码正确------')
                            cookies = self.browser.get_cookies()
                            for items in cookies:
                                new_cookie[items.get('name')] = items.get('value')
                            self.cookies = new_cookie
                            print('------cookies已更新------')
                        else:
                            print('------验证码输入错误------')
                        return new_cookie
                except Exception as e:
                    print('------处理搜狗验证码失败------{}'.format(e))
                    logger.error('------处理搜狗验证码失败------{}'.format(e))
            elif re.search('mp\.weixin\.qq\.com/profile', url):
                print('------开始处理微信验证码------')
                cert = random.random()
                image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
                respones = self.s.get(image_url, cookies=self.cookies, timeout=3)
                captch_input = captch_upload_image(respones.content)
                print('------验证码：{}------'.format(captch_input))
                data = {
                    'cert': cert,
                    'input': captch_input
                }
                # requests相关配置:公众号首页
                verifycode_headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'mp.weixin.qq.com',
                    'Origin': 'http://mp.weixin.qq.com',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                }
                respones = self.s.post(image_url, headers=verifycode_headers, cookies=self.cookies, data=data,
                                       timeout=3)
                ret = respones.json().get('ret')
                if ret == 0:
                    print('------验证码正确----ret--{}'.format(ret))
                    self.cookies = requests.utils.dict_from_cookiejar(respones.cookies)
                    print('------cookies已更新------')
                else:
                    print('------验证码错误----ret--{}'.format(respones.json()))
            else:
                print('------该URL不属于验证码链接----')
        else:
            print('不处理验证码，重新请求...')

    # 查找相关新闻，data_type：0:全部时间，1:一天内，2:一周内，3:一月内
    def get_news_other(self, search_key, data_type):
        news_type = ''
        if data_type == 0:
            news_type = '全部时间'
        elif data_type == 1:
            news_type = '一天内'
        elif data_type == 2:
            news_type = '一周内'
        elif data_type == 3:
            news_type = '一月内'
        print('------正在搜索：{}    采集时间范围：{}------'.format(search_key, news_type))

        # 该新闻一共有多少页
        page_total = 1
        # 是否进行后续的请求
        requests_flag = 0

        for i in range(20):
            try:
                params = {
                    'query': search_key,
                    'type': 2,
                    'page': 1,
                    'ie': 'utf8',
                    'tsn': data_type,
                    's_from': 'input'
                }
                query = urllib.parse.urlencode({'query': search_key, 'page': 1, 'tsn': data_type, })
                referer = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=input&_sug_=y&_sug_type_=&' + query
                self.headers['Referer'] = referer
                response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies,
                                      proxies={}, timeout=3)
                news_total_text = response.text
                if re.search('没有找到相关的微信公众号文章', news_total_text):
                    print('------没有找到相关的微信公众号文章------')
                    break
                elif (
                        re.search('id="tool"', news_total_text)
                        and re.search('id="pagebar_container"', news_total_text) == None
                ):
                    print('------当前搜索只有一页------')
                    requests_flag = 1
                    break
                elif self.judge_news(news_total_text):
                    if re.search('约([\d,，]*\d+)条', news_total_text):
                        news_total_str = re.findall('约([\d,，]*\d+)条', news_total_text)[0]
                        self.news_totals_all = int(re.sub('[,，]', '', news_total_str))
                        print('------找到约{}条结果------'.format(self.news_totals_all))
                        page_total = self.news_totals_all // 10
                        if self.news_totals_all % 10 > 0:
                            page_total += 1
                        print('------共有{}页------'.format(page_total))
                        requests_flag = 1
                    break
                else:
                    self.crack_sougou(response.url)
            except Exception as e:
                print('请求查询页失败，重试...{}'.format(e))
                logger.error('请求查询页失败，重试...{}'.format(e))

        # 查找全部
        if page_total >= 10:
            page_total = 10
        params = {
            'query': search_key,
            'type': 2,
            'page': 1,
            'ie': 'utf8',
            'tsn': data_type,
            's_from': 'input',
            'ft': '',
            'et': '',
            'interation': '',
            'wxid': '',
            'usip': '',
        }
        if requests_flag:
            for i in range(0, page_total):
                page = i + 1
                params['page'] = page
                query = urllib.parse.urlencode({'query': search_key, 'page': page, })
                referer = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=input&_sug_=y&_sug_type_=&' + query
                self.headers['Referer'] = referer
                # 对该页发起请求
                print('------正在请求第{}页------'.format(page))
                no_find = self.requests_news(params, page)
                if no_find:
                    break

    # 查找相关新闻，data_type：5: 按时间区间   ft 至 et
    def get_news_between(self, search_key, data_type, ft, et):
        print('------正在搜索：{}    采集时间范围：{} 至 {}------'.format(search_key, ft, et))

        # 该新闻一共有多少页
        page_total = 1
        # 是否进行后续的请求
        requests_flag = 0

        for i in range(20):
            try:
                params = {
                    'query': search_key,
                    'type': 2,
                    'page': 1,
                    'ie': 'utf8',
                    'tsn': data_type,
                    's_from': 'input',
                    'ft': ft,
                    'et': et,
                    'interation': '',
                    'wxid': '',
                    'usip': '',
                }
                query = urllib.parse.urlencode({'query': search_key, 'page': 1, })
                referer = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=input&_sug_=y&_sug_type_=&' + query
                self.headers['Referer'] = referer
                response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies,
                                      proxies={}, timeout=3)
                news_total_text = response.text
                if re.search('没有找到相关的微信公众号文章', news_total_text):
                    print('------没有找到相关的微信公众号文章------')
                    break
                elif (
                        re.search('id="tool"', news_total_text)
                        and re.search('id="pagebar_container"', news_total_text) == None
                ):
                    print('------当前搜索只有一页------')
                    requests_flag = 1
                    break
                elif self.judge_news(news_total_text):
                    if re.search('约([\d,，]*\d+)条', news_total_text):
                        news_total_str = re.findall('约([\d,，]*\d+)条', news_total_text)[0]
                        self.news_totals_all = int(re.sub('[,，]', '', news_total_str))
                        print('------找到约{}条结果------'.format(self.news_totals_all))
                        page_total = self.news_totals_all // 10
                        if self.news_totals_all % 10 > 0:
                            page_total += 1
                        print('------共有{}页------'.format(page_total))
                        requests_flag = 1
                    break
                else:
                    self.crack_sougou(response.url)
            except Exception as e:
                print('请求查询页失败，重试...{}'.format(e))
                logger.error('请求查询页失败，重试...{}'.format(e))

        # 查找全部
        if page_total >= 10:
            page_total = 10
        params = {
            'query': search_key,
            'type': 2,
            'page': 1,
            'ie': 'utf8',
            'tsn': data_type,
            's_from': 'input',
            'ft': ft,
            'et': et,
            'interation': '',
            'wxid': '',
            'usip': '',
        }
        if requests_flag:
            for i in range(0, page_total):
                page = i + 1
                params['page'] = page
                query = urllib.parse.urlencode({'query': search_key, 'page': page, })
                referer = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=input&_sug_=y&_sug_type_=&' + query
                self.headers['Referer'] = referer
                # 对该页发起请求
                print('------正在请求第{}页------'.format(page))
                no_find = self.requests_news(params, page)
                if no_find:
                    break

    # 对每一页发起请求
    def requests_news(self, params, page):
        no_find = 0
        for c in range(20):
            try:
                response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies,
                                      proxies={}, timeout=3)
                page_source = response.text
                if re.search('没有找到相关的微信公众号文章', page_source):
                    print('------没有找到相关的微信公众号文章------')
                    no_find = 1
                    break
                elif (
                        re.search('id="tool"', page_source)
                        and re.search('id="pagebar_container"', page_source) == None
                ):
                    print('------当前搜索只有一页------')
                    no_find = 1
                    if self.judge_news(page_source):
                        self.parse_news(page_source, page)
                    break
                elif self.judge_news(page_source):
                    self.parse_news(page_source, page)
                    time.sleep(1)
                    break
                else:
                    self.crack_sougou(response.url)
            except Exception as e:
                print('该页请求失败，重试...{}'.format(e))
                logger.error('该页请求失败，重试...{}'.format(e))
        return no_find

    # 判断是否正确请求到新闻页面
    def judge_news(self, page_source):
        html = etree.HTML(page_source)
        news_list = html.xpath('//div[@class="news-box"]/ul[@class="news-list"]/li')
        now_title = html.xpath('//title/text()')[0]
        if len(news_list) > 0:
            print('------成功跳转到新闻页面，开始爬取...当前网页标题：{}------'.format(now_title))
            return True
        elif (
                len(news_list) == 0
                and re.search('相关微信公众号文章 – 搜狗微信搜索', now_title)
                and (not re.search('没有找到相关的微信公众号文章', now_title))
        ):
            print('------成功跳转到新闻页面，开始爬取...当前网页标题：{}------'.format(now_title))
            print('------news_list为空！！！page_source：{}------'.format(page_source))
            return True
        else:
            print('------未成功跳转到新闻页面！！！当前网页标题：{}------'.format(now_title))
            return False

    # 开始处理每一页里的新闻URL
    def parse_news(self, html, page=1):
        html = etree.HTML(html)
        news_list = html.xpath('//div[@class="news-box"]/ul[@class="news-list"]/li')
        print('------正在解析第{}页，该页有{}条新闻------'.format(page, len(news_list)))
        for new in news_list:
            print('-' * 90)
            content_url = new.xpath('./div[@class="txt-box"]/h3/a/@data-share')[0]
            article_date_str = new.xpath('./div[@class="txt-box"]/div[@class="s-p"]/span/script/text()')[0]
            article_account = new.xpath('./div[@class="txt-box"]/div[@class="s-p"]/a/text()')[0].strip()
            article_title = ''.join(new.xpath('./div[@class="txt-box"]/h3/a//text()'))
            print('该新闻作者：{}'.format(article_account))
            print('该新闻标题：{}'.format(article_title))
            print('该新闻链接：{}'.format(content_url))

            delta_days = 0
            article_single_md5 = ''
            if re.search('timeConvert\(\'(\d+)\'\)', article_date_str):
                article_timestamp_str = re.findall('timeConvert\(\'(\d+)\'\)', article_date_str)[0]
                article_date = datetime.date.fromtimestamp(int(article_timestamp_str))
                delta_days = (datetime.date.today() - article_date).days
                print('该新闻发文日期：{}，距离当前天数：{}'.format(article_date, delta_days))
                article_md5_str = article_account + article_title + article_timestamp_str
                h1 = hashlib.md5()
                h1.update(article_md5_str.encode(encoding='utf-8'))
                article_single_md5 = h1.hexdigest()

            if delta_days > 15:
                print('该新闻距离当前天数：{}，超过两星期，跳过...'.format(delta_days))
                continue
            if (
                    article_single_md5 != ''
                    and article_single_md5 in self.key_cache_single
            ):
                print('该新闻在当前关键词搜索中已采集...')
                continue

            # 开始解析，增源，判重，发包
            self.source_sentenced_send(content_url)
            self.requests_totals_all += 1
            if article_single_md5 != '':
                self.key_cache_single.append(article_single_md5)
            print('crawl_no:{}, 已请求URL数量：{}'.format(self.crawl_no, self.requests_totals_all))

    # 解析每一条新闻URL，按照格式配置
    def parse_detail(self, content_url):
        print('content_url：{}'.format(content_url))
        if not re.match('https?://(mp\.weixin\.qq\.com|weixin\.sogou\.com/api/share)', content_url):
            print('parse_detail...传入url不符合规则...跳过：{}'.format(content_url))
            return None
        new_result = {
            'headers': {
                'topic': 'weixin',
                'key': '',
                'timestamp': 0,
            },
            'body': {
                'ID': '',
                'Account': '',
                'TaskID': '',
                'TaskName': '',
                'AccountID': '',
                'SiteID': 0,
                'TopicID': 0,
                'Url': '',
                'Title': '',
                'Content': '',
                'Author': '',
                'Time': 0,
                'AddOn': 0,
                'Tags': '',
                'DefinedSite': '',
                'CustomerID': '',
                'CrawlerType': '2',
                'ImageUrl': '',
            }
        }
        page_source = ''
        page_source_ok = 0
        for i in range(30):
            try:
                response = self.s.get(content_url, cookies=self.cookies, proxies=self.proxies, timeout=3)
                page_source = response.text
                if re.search('Too Many Requests', page_source, re.I):
                    print('------Too Many Requests.Oops, tunnel requests exceeded.代理连接数超过规定------')
                    time.sleep(random.uniform(0, 1))
                    continue
                page_source_ok = 1
                break
            except Exception as e:
                print('请求新闻详情页面失败，重试...{}'.format(e))
                logger.error('请求新闻详情页面失败，重试...{}'.format(e))
                time.sleep(random.uniform(0, 1))

        if len(page_source) and page_source_ok == 1:
            if re.search('此帐号被投诉且经审核涉嫌侵权', page_source):
                print('------此帐号被投诉且经审核涉嫌侵权。此帐号已注销，内容无法查看。跳过------')
                return None
            elif (
                    re.search('id="js_share_headimg"', page_source)
                    and re.search('id="js_share_content"', page_source)
                    and re.search('id="js_share_author"', page_source)
            ):
                print('------这是分享文章，非公众号文章。跳过------')
                return None
            elif re.search('该内容已被发布者删除', page_source):
                print('------该内容已被发布者删除。跳过------')
                return None
            elif re.search('链接已过期', page_source):
                print('------链接已过期。跳过------')
                return None
            elif re.search('此帐号处于帐号迁移流程中', page_source):
                print('------此帐号处于帐号迁移流程中。跳过------')
                return None
            elif re.search('访问过于频繁[，,]请用微信扫描二维码进行访问', page_source):
                print('------访问过于频繁，请用微信扫描二维码进行访问。跳过------')
                if not self.proxies:
                    time.sleep(20 * 60)
                return None

            for i in range(10):
                try:
                    nowtime_str = str(time.time()).split('.')[0]
                    new_result['headers']['topic'] = 'weixin'
                    new_result['headers']['timestamp'] = int(nowtime_str)
                    html = etree.HTML(page_source)
                    new_result['body']['Url'] = content_url
                    title_str = html.xpath('//h2[@id="activity-name"]/text()')[0]
                    new_result['body']['Title'] = title_str.strip().replace(' ', '').replace('&nbsp;', '').replace(
                        '&quot;', '')
                    new_result['body']['Content'] = ''.join(html.xpath('//div[@id="js_content"]//text()')).strip()
                    new_result['body']['Author'] = html.xpath('//div[@id="meta_content"]/span/a/text()')[0].strip()
                    new_result['body']['Time'] = int(re.findall('var ct="(\d+)"', page_source)[0] + '000')
                    new_result['body']['AddOn'] = int(nowtime_str + '000')
                    new_result['body']['TaskName'] = '微信_' + new_result['body']['Author']
                    ImageUrl_ls = []
                    if re.search('data-src="(https://mmbiz\.qpic\.cn/mmbiz(_jpg|_png|/).*?)"', page_source):
                        image_urls = re.findall('data-src="(https://mmbiz\.qpic\.cn/mmbiz(_jpg|_png|/).*?)"',
                                                page_source)
                        for item in image_urls:
                            if (
                                    re.search('wx_fmt', item[0])
                                    and (not re.search('wx_fmt=other', item[0]))
                                    and (item[0] not in ImageUrl_ls)
                            ):
                                ImageUrl_ls.append(item[0])
                    if len(ImageUrl_ls) == 1:
                        new_result['body']['ImageUrl'] = ImageUrl_ls[0]
                    elif len(ImageUrl_ls) > 1:
                        new_result['body']['ImageUrl'] = '|'.join(ImageUrl_ls)

                    account_source_collectiontime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    account_source_biz = ''
                    if re.search('var biz = "" *\| *\| *"(.*?)"', page_source):
                        account_source_biz = re.findall('var biz = "" *\| *\| *"(.*?)"', page_source)[0]
                    elif re.search('var biz = "(.*?)" *\| *\| *""', page_source):
                        account_source_biz = re.findall('var biz = "(.*?)" *\| *\| *""', page_source)[0]

                    # ID为Title+Time的MD5加密
                    title_time_str = new_result['body']['Title'] + str(new_result['body']['Time'])
                    hl = hashlib.md5()
                    hl.update(title_time_str.encode(encoding='utf-8'))
                    title_time_md5 = hl.hexdigest()
                    new_result['headers']['key'] = title_time_md5
                    new_result['body']['ID'] = title_time_md5

                    # 公众号的微信号
                    account_no = html.xpath('//div[@id="js_profile_qrcode"]/div/p[1]/span/text()')
                    if len(account_no):
                        new_result['body']['Account'] = account_no[0]
                    else:
                        new_result['body']['Account'] = self.find_account(new_result['body']['Author'])
                        if (
                                new_result['body']['Account'] == ''
                                and re.search('var user_name = "(.*?)"', page_source)
                        ):
                            print('开始在该文章源码里查找系统分配原始微信号')
                            new_result['body']['Account'] = re.findall('var user_name = "(.*?)"', page_source)[0]
                            if new_result['body']['Account']:
                                print('在该文章源码里查找系统分配原始微信号---成功：{}'.format(new_result['body']['Account']))
                                self.account_find_all[new_result['body']['Account']] = new_result['body']['Author']
                            else:
                                print('在该文章源码里查找系统分配原始微信号---失败：{}'.format(new_result['body']['Account']))

                    if new_result['body']['Account']:
                        account_id = ''
                        try:
                            # 查询底层公众号基础信息
                            account_id = self.get_account_id(new_result['body']['Account'])

                            # 增源
                            if (
                                    SOURCE_ADD_ENABLED
                                    and account_id in ['', 0, None, '0']
                            ):
                                print('增源：该微信号是新的：{}'.format(new_result['body']['Account']))
                                my_sqlserver.add_account(name=new_result['body']['Author'],
                                                         account=new_result['body']['Account'],
                                                         url='http://weixin.sogou.com/gzh?openid',
                                                         collectiontime=account_source_collectiontime,
                                                         biz=account_source_biz)
                        except Exception as e:
                            print('查询或增源失败...{}'.format(e))
                            logger.error('查询或增源失败...{}'.format(e))

                        # 获取AccountID
                        try:
                            if not account_id:
                                account_id = self.get_account_id(new_result['body']['Account'])
                            if account_id:
                                new_result['body']['TaskID'] = account_id
                                new_result['body']['AccountID'] = account_id
                                new_result['body']['SiteID'] = int(account_id)
                        except Exception as e:
                            print('获取AccountID失败...{}'.format(e))
                            logger.error('获取AccountID失败...{}'.format(e))

                    if not new_result['body']['AccountID']:
                        print('AccountID为空:{}，跳过...'.format(new_result['body']['AccountID']))
                        return None

                    # 判重的keys，微信号+微信号ID的MD5
                    sentenced_keys = new_result['body']['Account'] + ' ' + new_result['body']['AccountID']
                    h2 = hashlib.md5()
                    h2.update(sentenced_keys.encode(encoding='utf-8'))
                    sentenced_keys_md5 = h2.hexdigest()

                    # 判重的数据格式
                    sentenced_ls = json.dumps([
                        {
                            'key': sentenced_keys_md5,
                            'sourceNodes': SOURCENODES,
                            'sourceType': SOURCETYPE,
                            'urls': [title_time_md5],
                        }
                    ])

                    # 发包的数据格式:数据中心
                    send_result = {
                        'headers': new_result['headers'],
                        'body': json.dumps(new_result['body'])
                    }

                    # 发包的数据格式:三合一
                    send_pro_result = {
                        'headers': {
                            'topic': 'proWeixin',
                            'key': new_result['headers']['key'],
                            'timestamp': new_result['headers']['timestamp'],
                        },
                        'body': json.dumps({
                            'ID': new_result['body']['ID'],
                            'TaskName': new_result['body']['TaskName'],
                            'Domain': '',
                            'SiteType': 0,
                            'Overseas': 0,
                            'Title': new_result['body']['Title'],
                            'Content': new_result['body']['Content'],
                            'Time': new_result['body']['Time'],
                            'Source': '',
                            'Url': new_result['body']['Url'],
                            'Account': new_result['body']['Account'],
                            'AccountID': new_result['body']['AccountID'],
                            'Author': new_result['body']['Author'],
                            'From': '',
                            'Images': 0,
                            'ImageUrl': new_result['body']['ImageUrl'],
                            'PortraitUrl': '',
                            'VideoUrl': '',
                            'Keywords': '',
                            'Language': 0,
                            'TopicName': '',
                            'Views': 0,
                            'Transmits': 0,
                            'Comments': 0,
                            'Praises': 0,
                            'Follows': 0,
                            'Fans': 0,
                            'Blogs': 0,
                            'Sex': 0,
                            'UID': '',
                            'BlogID': '',
                            'Province': '',
                            'City': '',
                            'QuoteBlogID': '',
                            'QuoteUrl': '',
                            'QuoteTime': 0,
                            'QuoteImages': 0,
                            'QuoteVideoUrl': '',
                            'QuoteShortUrl': '',
                            'QuoteUID': '',
                            'QuoteSex': 0,
                            'QuoteProvince': '',
                            'QuoteCity': '',
                            'QuoteFollows': 0,
                            'QuoteFans': 0,
                            'AddOn': new_result['body']['AddOn'],
                            'LongBlogType': 1,
                            'ArticleTitle': '',
                            'ArticleContent': '',
                            'Original': 0,
                            'QuoteContent': '',
                            'QuoteAuthor': '',
                            'QuotePortraitUrl': '',
                            'QuoteImageUrl': '',
                            'QuoteComments': 0,
                            'QuotePraises': 0,
                            'QuoteTransmits': 0,
                            'QuoteSource': '',
                            'Place': '',
                            'DataType': 1003,
                            'EventID': '',
                            'ClassifyID': '',
                            'IsGarbage': 0,
                            'ShortUrl': '',
                            'Tags': '',
                            'DefinedSite': '',
                            'CustomerID': '',
                            'CrawlerType': '2',
                        }, ensure_ascii=False)
                    }

                    # 发包的数据格式:FTP
                    ftp_id = new_result['body']['AccountID']
                    if ftp_id:
                        ftp_id = int(ftp_id)
                    send_ftp_result = {
                        'id': ftp_id,
                        'url': new_result['body']['Url'],
                        'title': new_result['body']['Title'],
                        'content': new_result['body']['Content'],
                        'author': new_result['body']['Author'],
                        'time': time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(int(str(new_result['body']['Time'])[:-3]))),
                        'account': new_result['body']['Account'],
                        'image': new_result['body']['ImageUrl']
                    }

                    return {
                        'sentenced_ls': sentenced_ls,
                        'send_result': send_result,
                        'send_pro_result': send_pro_result,
                        'send_ftp_result': send_ftp_result,
                    }

                except Exception as e:
                    print('解析具体新闻报错，重试...{}'.format(e))
                    logger.error('解析具体新闻报错，重试...{}'.format(e))

        else:
            print('parse_detail...失败,page_source_ok：{}'.format(page_source_ok))
            print('parse_detail...失败,page_source：{}'.format(page_source))
            return None

    # 解析，增源，判重，发包
    def source_sentenced_send(self, content_url):
        # 解析
        detail_result = self.parse_detail(content_url)
        if detail_result:
            sentenced_ls = detail_result['sentenced_ls']
            send_result = detail_result['send_result']
            send_pro_result = detail_result['send_pro_result']
            send_ftp_result = detail_result['send_ftp_result']

            # 判重
            if SENTENCED_ENABLED:
                # 判重：当前公众号的文章url是否已经存在
                existed_ls = self.sentenced_news_get(sentenced_ls)
                url_md5 = json.loads(sentenced_ls)[0].get('urls')[0]
                if url_md5 not in existed_ls:
                    print('判重结果：这是新文章，开始发包...')
                    # 发包
                    if SEND_PACKAGE_ENABLED:
                        # 发包:FTP
                        send_ftp_ok = self.send_ftp_news(send_ftp_result)
                        # 发包:数据中心
                        send_ok = self.send_news(send_result)
                        # 发包:三合一
                        send_pro_ok = self.send_pro_news(send_pro_result)
                        # 发包成功，判重添加
                        if send_ftp_ok == 1 and send_ok == 1 and send_pro_ok == 1:
                            sentenced_res = self.sentenced_news_add(json.dumps([json.loads(sentenced_ls)[0]]))
                            if sentenced_res.get('msg') == '成功' and sentenced_res.get('status') == 0:
                                print('判重URL：添加成功...')
                else:
                    print('判重结果：这是旧文章，跳过')
                    print('send_result_headers：{}'.format(send_result['headers']))
                    print('send_pro_result_headers：{}'.format(send_pro_result['headers']))
            else:
                print('判重结果：不进行判重，开始发包...')
                # 发包
                if SEND_PACKAGE_ENABLED:
                    # 发包:FTP
                    send_ftp_ok = self.send_ftp_news(send_ftp_result)
                    # 发包:数据中心
                    send_ok = self.send_news(send_result)
                    # 发包:三合一
                    send_pro_ok = self.send_pro_news(send_pro_result)
                    # 发包成功，判重添加
                    if send_ftp_ok == 1 and send_ok == 1 and send_pro_ok == 1:
                        sentenced_res = self.sentenced_news_add(json.dumps([json.loads(sentenced_ls)[0]]))
                        if sentenced_res.get('msg') == '成功' and sentenced_res.get('status') == 0:
                            print('全部发包成功，判重URL：添加成功...')

    # 如果新闻页面没有显示微信号，则根据公众号查出来
    def find_account(self, author):
        account = ''

        # 查找记录只保存100条
        if len(self.account_find_all) > 100:
            self.account_find_all.clear()

        if author in self.account_find_all.values():
            print('开始在查找记录中找微信号：{}'.format(author))
            for k, v in self.account_find_all.items():
                if v == author:
                    print('成功查找微信号：{}'.format(author))
                    account = k
        else:
            print('开始在网页查找微信号：{}'.format(author))
            url = 'https://weixin.sogou.com/weixin'
            params = {
                'type': 1,
                'query': author,
                'ie': 'utf8',
                's_from': 'input',
                '_sug_': 'y',
            }
            for c in range(10):
                try:
                    response = self.s.get(url, params=params, cookies=self.cookies, proxies={}, timeout=3)
                    page_source = response.text
                    if re.search('<label name="em_weixinhao">(.*?)</label>', page_source):
                        account = re.findall('<label name="em_weixinhao">(.*?)</label>', page_source)[0]
                        print('成功查找微信号：{}'.format(author))
                        self.account_find_all[account] = author
                        break
                    elif re.search('<p class="p1">呀！</p>', page_source):
                        print('暂无与“{}”相关的官方认证订阅号。。'.format(author))
                        break
                    else:
                        self.crack_sougou(response.url)
                except Exception as e:
                    print('在网页查找微信号报错，重试...{}'.format(e))
                    logger.error('在网页查找微信号报错，重试...{}'.format(e))
        if account == '':
            print('查找"{}"的微信号失败...'.format(author))
        return account

    # 根据微信号从查询接口获取AccountId
    def get_account_id(self, account):
        account_id = ''
        params = {
            'account': account
        }
        for i in range(5):
            try:
                url_resp = requests.get(url=GetAccountId_URL2, params=params, timeout=3)
                account_id = json.loads(url_resp.text).get('id')
                if account_id in ['', 0, None, '0']:
                    account_res = my_sqlserver.get_account(account)
                    if len(account_res):
                        account_id = account_res[0][0]
                if account_id not in ['', 0, None, '0']:
                    account_id = str(account_id)
                break
            except Exception as e:
                print('获取AccountId失败...{}'.format(e))
                logger.error('获取AccountId失败...{}'.format(e))
        return account_id

    # 判重（获取url），返回该公众号所有已存在文章：Schedule/GetCacheWx
    def sentenced_news_get(self, sentenced_ls):
        params = {
            'keys': json.loads(sentenced_ls)[0].get('key'),
            'sourceNodes': SOURCENODES,
            'sourceType': SOURCETYPE,
        }
        for i in range(10):
            try:
                response = requests.get(url=GetCacheWx_URL_main, params=params, timeout=3)
                if response.status_code == 200:
                    res_data = response.json().get('data')
                    if len(res_data) == 0:
                        return []
                    else:
                        existed_ls = res_data[0].get('urls')
                        return existed_ls
            except Exception as e:
                print('{}，请求失败，重试...{}'.format(GetCacheWx_URL_main, e))
                logger.error('{}，请求失败，重试...{}'.format(GetCacheWx_URL_main, e))
        return []

    # 判重（添加url），往公众号添加这个新文章：Schedule/CacheWx
    def sentenced_news_add(self, need_add_all):
        if need_add_all:
            # 发包成功了，就把这些数据添加到判重缓存中
            for i in range(10):
                try:
                    response = requests.post(url=CacheWx_URL_main, data=need_add_all, timeout=3)
                    if response.status_code == 200:
                        return response.json()
                except Exception as e:
                    print('{}，请求失败，重试...{}'.format(CacheWx_URL_main, e))
                    logger.error('{}，请求失败，重试...{}'.format(CacheWx_URL_main, e))
            return {'msg': '', 'status': ''}
        else:
            print('判重（添加url）参数为空，不添加...')
            return {'msg': '', 'status': ''}

    # 解析后列表序列化并发送:数据中心
    def send_news(self, send_result):
        print('send_result_headers：{}'.format(send_result['headers']))
        send_ok = 0
        if send_result:
            if sys.getsizeof(json.dumps(send_result)) >= 2 * 1024 * 1024:
                print('这条数据大于2M，丢弃...')
                return
            # 将该条数据添加到待发包中
            datacenter_Yweixin = [
                {
                    "headers": {
                        "topic": "Yweixin",
                    },
                    "body": json.dumps([send_result])
                },
            ]
            json_result_Yweixin = json.dumps(datacenter_Yweixin)
            for i in range(10):
                try:
                    send_response = requests.post(url=SEND_URL_datacenter_main, data=json_result_Yweixin, timeout=3)
                    if send_response.status_code == 200:
                        print('数据中心：发包成功...')
                        send_ok = 1
                        return send_ok
                except Exception as e:
                    print('{}，数据中心：发包失败，重试...{}'.format(SEND_URL_datacenter_main, e))
                    logger.error('{}，数据中心：发包失败，重试...{}'.format(SEND_URL_datacenter_main, e))

            if send_ok == 0:
                for i in range(10):
                    try:
                        send_response = requests.post(url=SEND_URL_datacenter_backup, data=json_result_Yweixin,
                                                      timeout=3)
                        if send_response.status_code == 200:
                            print('备用：数据中心：发包成功...')
                            send_ok = 1
                            return send_ok
                    except Exception as e:
                        print('备用：{}，数据中心：发包失败，重试...{}'.format(SEND_URL_datacenter_backup, e))
                        logger.error('备用：{}，数据中心：发包失败，重试...{}'.format(SEND_URL_datacenter_backup, e))

            return send_ok
        else:
            print('解析后返回结果为空，不添加到待发包中!')
            return send_ok

    # 解析后列表序列化并发送:三合一
    def send_pro_news(self, send_pro_result):
        print('send_pro_result_headers：{}'.format(send_pro_result['headers']))
        send_pro_ok = 0
        if send_pro_result:
            if sys.getsizeof(json.dumps(send_pro_result)) >= 2 * 1024 * 1024:
                print('这条数据大于2M，丢弃...')
                return
            # 将该条数据添加到待发包中
            datacenter_YproWeixin = [
                {
                    "headers": {
                        "topic": "YproWeixin",
                    },
                    "body": json.dumps([send_pro_result])
                },
            ]
            json_result_YproWeixin = json.dumps(datacenter_YproWeixin)
            for i in range(10):
                try:
                    send_response = requests.post(url=SEND_URL_datacenter_main, data=json_result_YproWeixin, timeout=3)
                    if send_response.status_code == 200:
                        print('三合一：发包成功...')
                        send_pro_ok = 1
                        return send_pro_ok
                except Exception as e:
                    print('{}，三合一：发包失败，重试...{}'.format(SEND_URL_datacenter_main, e))
                    logger.error('{}，三合一：发包失败，重试...{}'.format(SEND_URL_datacenter_main, e))

            if send_pro_ok == 0:
                for i in range(10):
                    try:
                        send_response = requests.post(url=SEND_URL_datacenter_backup, data=json_result_YproWeixin,
                                                      timeout=3)
                        if send_response.status_code == 200:
                            print('备用：三合一：发包成功...')
                            send_pro_ok = 1
                            return send_pro_ok
                    except Exception as e:
                        print('备用：{}，三合一：发包失败，重试...{}'.format(SEND_URL_datacenter_backup, e))
                        logger.error('备用：{}，三合一：发包失败，重试...{}'.format(SEND_URL_datacenter_backup, e))

        else:
            print('解析后返回结果为空，不添加到待发包中!')
            return send_pro_ok

    # 解析后并发送:FTP
    def send_ftp_news(self, send_ftp_result):
        send_ftp_ok = 0
        try:
            xml_name = my_ftp.create_xml(send_ftp_result)
            zip_name = str(uuid.uuid1())
            my_ftp.create_zip(xml_name, zip_name, send_ftp_result)
            send_ok = my_ftp.send(zip_name)
            if send_ok:
                send_ftp_ok = 1
                xml_num = len(os.listdir(XMLS_DIR))
                print('本地已存在XML和ZIP数量为：{}'.format(xml_num))
                if xml_num >= MAX_XML_NUM:
                    my_ftp.del_xml_zip()
                    print('本地已存在XML和ZIP文件已清空')
        except Exception as e:
            print('FTP操作异常：{}'.format(e))
            logger.error('FTP操作异常：{}'.format(e))
        return send_ftp_ok

    # 退出selenium
    def quit(self):
        self.browser.quit()
        print('关闭selenium')

    # 开始运行
    def run(self, search_key, DEMO_TYPE, ft_et_list):
        if DEMO_TYPE == 1 and ft_et_list != []:
            print('任务采集：一天')
            self.get_news_other(search_key, data_type=1)

            print('任务采集：{} 至 {}'.format(ft_et_list[-1], ft_et_list[0]))
            for ft in ft_et_list:
                et = ft
                data_type = 5
                self.get_news_between(search_key, data_type, ft, et)

            print('任务采集：一周')
            self.get_news_other(search_key, data_type=2)

        if DEMO_TYPE == 2:
            print('日常采集：默认 一天 一周')
            for data_type in [0, 1, 2]:
                self.get_news_other(search_key, data_type)


# 通过接口获取新闻关键字
def get_api_keys():
    key_list = []
    for i in range(10):
        try:
            response = requests.get(url=ScheduleDispatch_URL, timeout=3)
            result = json.loads(response.text)
            data = result.get('data')
            if data != '':
                key_word = json.loads(data).get('keyword')
                key_list.append(key_word)
            break
        except Exception as e:
            print('微信元搜索任务调度失败...{}'.format(e))
            logger.error('微信元搜索任务调度失败...{}'.format(e))
    return key_list


# 通过txt文件获取新闻关键字
def get_txt_keys():
    # 关键字txt文件路径
    keys_file_path = os.path.join(FILES_DIR, KEYS_FILE_NAME)
    print('KEYS_FILE_PATH：{}'.format(keys_file_path))

    key_list = []
    if os.path.exists(keys_file_path):
        if os.path.isfile(keys_file_path):
            with open(keys_file_path, mode='r', encoding='utf-8') as f:
                for i in f.readlines():
                    if i.strip():
                        key_list.append(i.strip())
        else:
            print('该文件名不存在！请检查是否为正确文件名：{}'.format(keys_file_path))
    else:
        print('该路径不存在！请检查该路径是否正确：{}'.format(keys_file_path))
    return key_list


# 返回最近三天的日期列表,如：['2018-10-24', '2018-10-23', '2018-10-22']
def get_date_list():
    base_date_str = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    date_need_list = [base_date_str]
    base_date = datetime.datetime.strptime(base_date_str, '%Y-%m-%d')
    for i in range(-1, -3, -1):
        delta = datetime.timedelta(days=i)
        n_days = base_date + delta
        n_days = n_days.strftime('%Y-%m-%d')
        date_need_list.append(n_days)
    print('date_need_list：{}'.format(date_need_list))
    return date_need_list


# 检测abuyun代理IP接口是否到期
def get_abuyun_proxy():
    if ABUYUN_ENABLED:
        try:
            target_url = "http://test.abuyun.com"
            proxy = 'http://{}:{}@{}:{}'.format(ABUYUN_USER, ABUYUN_PASS, ABUYUN_HOST, ABUYUN_PORT)
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            resp = requests.get(url=target_url, proxies=proxies)
            status_code = resp.status_code
            if status_code == 200:
                print('status_code：{}，阿布云代理获取正常...开始使用...'.format(status_code))
                return proxies
            elif status_code == 429:
                print('status_code：{}，阿布云代理连接数超过上限...开始使用...'.format(status_code))
                return proxies
            elif status_code == 402:
                print('status_code：{}，阿布云代理已欠费...不再使用...'.format(status_code))
                return {}
        except Exception as e:
            print('阿布云代理获取失败...不再使用...{}'.format(e))
            logger.error('阿布云代理获取失败...不再使用...{}'.format(e))
            return {}
    else:
        return {}


# 获取代理池中的代理
def get_proxy():
    proxies = {}
    GETPROXY_URL = 'http://183.238.76.204:38016/GetProxy'
    try:
        res = requests.get(url=GETPROXY_URL)
        proxies = res.json().get('proxies')
        if proxies:
            print('获取代理成功...{}'.format(proxies))
    except Exception as e:
        print('获取代理失败...{}'.format(e))
    return proxies


# 采集主程序
def crawl(crawl_no=0):
    url = 'https://weixin.sogou.com/weixin'
    sougou_weixin = SougouWeixin(url, crawl_no)
    restart_num = 0

    while 1:
        try:
            key_list = []
            if TXT_ENABLED == 1:
                print('读取TXT文件内关键词...')
                key_list = get_txt_keys()
            else:
                print('请求关键词接口...')
                key_list = get_api_keys()

            if key_list:
                ft_et_list = []
                if DEMO_TYPE == 1:
                    ft_et_list = get_date_list()
                print('key_list：{}'.format(key_list))
                for search_key in key_list:
                    if (
                            search_key
                            and search_key not in ['*', '-', '+', ' ', '    ', ]
                            and len(search_key) <= 35
                    ):
                        search_key = re.sub('[\+＋]', ' ', search_key)
                        for i in range(3):
                            try:
                                print('开始采集...新闻关键词：{}'.format(search_key))
                                sougou_weixin.proxies = get_abuyun_proxy()
                                sougou_weixin.key_cache_single = []
                                sougou_weixin.run(search_key, DEMO_TYPE, ft_et_list)
                                print('采集完毕...新闻关键词：{}'.format(search_key))
                                time.sleep(1)
                                restart_num += 1
                                break
                            except Exception as e:
                                print('采集程序报错中止：{}'.format(e))
                                logger.error('采集程序报错中止：{}'.format(e))
                if restart_num >= 50:
                    sougou_weixin.quit()
                    print('已采集50个关键词，10秒后重启selenium，继续采集...')
                    sougou_weixin = SougouWeixin(url, crawl_no)
                    restart_num = 0
            else:
                time.sleep(10)
        except Exception as e:
            print('运行程序报错中止：{}'.format(e))
            logger.error('运行程序报错中止：{}'.format(e))
            continue


if __name__ == '__main__':
    thread_ls = []
    for i in range(THREAD_NUM):
        t = threading.Thread(target=crawl, args=(i,))
        thread_ls.append(t)
        t.start()

    for t in thread_ls:
        t.join()
