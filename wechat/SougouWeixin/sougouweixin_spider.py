# -*- coding: utf-8 -*-
import re
import sys
import time
import json
import random
import hashlib
import datetime

import requests
import urllib.parse
from PIL import Image
from io import BytesIO
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from log import *
from config import *
from sqlserver_util import my_sqlserver
from captch_dytry import captch_upload_image


class SougouWeixin(object):
    def __init__(self, url):
        self.url = url
        # 待发包的数据
        self.need_send_all = []
        # 待添加判重中的数据
        self.need_add_all = []
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

    # 查找相关新闻，data_type：1:一天内，2:一周内，3:一月内
    # 不要
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
        logger.info('------正在搜索：{}    采集时间范围：{}------'.format(search_key, news_type))

        # 该新闻一共有多少页
        page_total = 1
        # 是否进行后续的请求
        requests_flag = 0

        while 1:
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
            response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            news_total_text = response.text
            if self.judge_news(news_total_text):
                if re.search('约([\d,，]*\d+)条', news_total_text):
                    news_total_str = re.findall('约([\d,，]*\d+)条', news_total_text)[0]
                    self.news_totals_all = int(re.sub('[,，]', '', news_total_str))
                    logger.info('------找到约{}条结果------'.format(self.news_totals_all))
                    page_total = self.news_totals_all // 10
                    if self.news_totals_all % 10 > 0:
                        page_total += 1
                    logger.info('------共有{}页------'.format(page_total))
                    requests_flag = 1
                break
            elif re.search('没有找到相关的微信公众号文章', news_total_text):
                logger.info('------没有找到相关的微信公众号文章------')
                break
            elif (
                    re.search('id="tool"', news_total_text)
                    and re.search('id="pagebar_container"', news_total_text) == None
            ):
                logger.info('------当前搜索只有一页------')
                requests_flag = 1
                break
            else:
                self.crack_sougou(response.url)

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
    # 不要
    def get_news_between(self, search_key, data_type, ft, et):
        logger.info('------正在搜索：{}    采集时间范围：{} 至 {}------'.format(search_key, ft, et))

        # 该新闻一共有多少页
        page_total = 1
        # 是否进行后续的请求
        requests_flag = 0

        while 1:
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
            response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            news_total_text = response.text
            if self.judge_news(news_total_text):
                if re.search('约([\d,，]*\d+)条', news_total_text):
                    news_total_str = re.findall('约([\d,，]*\d+)条', news_total_text)[0]
                    self.news_totals_all = int(re.sub('[,，]', '', news_total_str))
                    logger.info('------找到约{}条结果------'.format(self.news_totals_all))
                    page_total = self.news_totals_all // 10
                    if self.news_totals_all % 10 > 0:
                        page_total += 1
                    logger.info('------共有{}页------'.format(page_total))
                    requests_flag = 1
                break
            elif re.search('没有找到相关的微信公众号文章', news_total_text):
                logger.info('------没有找到相关的微信公众号文章------')
                break
            elif (
                    re.search('id="tool"', news_total_text)
                    and re.search('id="pagebar_container"', news_total_text) == None
            ):
                logger.info('------当前搜索只有一页------')
                requests_flag = 1
                break
            else:
                self.crack_sougou(response.url)

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
                logger.info('------正在请求第{}页------'.format(page))
                no_find = self.requests_news(params, page)
                if no_find:
                    break

    # 对每一页发起请求
    # 不要
    def requests_news(self, params, page):
        no_find = 0
        for c in range(20):
            response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            page_source = response.text
            if self.judge_news(page_source):
                self.parse_news(page_source, page)
                time.sleep(1)
                break
            elif re.search('没有找到相关的微信公众号文章', page_source):
                logger.info('------没有找到相关的微信公众号文章------')
                no_find = 1
                break
            elif (
                        re.search('id="hint_container"', page_source)
                    and re.search('id="pagebar_container"', page_source) == None
            ):
                logger.info('------当前搜索只有一页------')
                no_find = 1
                break
            else:
                self.crack_sougou(response.url)
        return no_find

    # 判断是否正确请求到新闻页面
    def judge_news(self, page_source):
        html = etree.HTML(page_source)
        news_list = html.xpath('//div[@class="news-box"]/ul[@class="news-list"]/li')
        now_title = html.xpath('//title/text()')[0]
        if len(news_list) > 0:
            logger.info('------成功跳转到新闻页面，开始爬取...当前网页标题：{}------'.format(now_title))
            return True
        elif (
                len(news_list) == 0
                and re.search('相关微信公众号文章 – 搜狗微信搜索', now_title)
                and (not re.search('没有找到相关的微信公众号文章', now_title))
        ):
            logger.info('------成功跳转到新闻页面，开始爬取...当前网页标题：{}------'.format(now_title))
            #logger.info('------news_list为空！！！page_source：{}------'.format(page_source))
            return True
        else:
            logger.info('------未成功跳转到新闻页面！！！当前网页标题：{}------'.format(now_title))
            return False

    # 处理验证码
    def crack_sougou(self, url):
        logger.info('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            logger.info('出现验证码：session重新初始化...')
            self.s = requests.session()
            logger.info('------开始处理搜狗验证码------')
            self.browser.get(url)
            time.sleep(2)
            if 'login-info' in self.browser.page_source:
                for i in range(30):
                    self.browser.get(url)
                    logger.info('浏览器正常...异常调用验证码函数')
                    logger.info('当前浏览器url:'.format(self.browser.current_url))
                    if 'login-info' not in self.browser.page_source:
                        break
            try:
                img = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
                logger.info('------出现验证码页面------')
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
                captch_input = ''
                if GETCAPTCHA_TYPE == 1:
                    with open(captcha_path, "rb") as f:
                        filebytes = f.read()
                    captch_input = captch_upload_image(filebytes)
                elif GETCAPTCHA_TYPE == 2:
                    files = {'img': (CAPTCHA_NAME, open(captcha_path, 'rb'), 'image/png', {})}
                    res = requests.post(url=GetCaptcha_url, files=files)
                    res = res.json()
                    if res.get('Success'):
                        captch_input = res.get('Captcha')
                logger.info('------验证码：{}------'.format(captch_input))
                if captch_input:
                    input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                    input_text.clear()
                    input_text.send_keys(captch_input)
                    submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                    submit.click()
                    try:
                        logger.info('------输入验证码------')
                        time.sleep(1)
                        new_cookie = {}
                        if re.search('login-info', self.browser.page_source):
                            logger.info('------验证码正确------')
                            cookies = self.browser.get_cookies()
                            for items in cookies:
                                new_cookie[items.get('name')] = items.get('value')
                            self.cookies = new_cookie
                            logger.info('------cookies已更新------')
                        else:
                            logger.info('------验证码输入错误------')
                        return new_cookie
                    except:
                        logger.info('------验证码输入错误------')
            except:
                logger.info('------未跳转到验证码页面，跳转到首页，忽略------')
        elif re.search('mp\.weixin\.qq\.com', url):
            logger.info('------开始处理微信验证码------')
            cert = random.random()
            image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
            respones = self.s.get(image_url, cookies=self.cookies)
            captch_input = captch_upload_image(respones.content)
            logger.info('------验证码：{}------'.format(captch_input))
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
            respones = self.s.post(image_url, headers=verifycode_headers, cookies=self.cookies, data=data)
            ret = respones.json().get('ret')
            if ret == 0:
                logger.info('------验证码正确----ret--{}'.format(ret))
                self.cookies = requests.utils.dict_from_cookiejar(respones.cookies)
                logger.info('------cookies已更新------')
            else:
                logger.info('------验证码错误----ret--{}'.format(respones.json()))

    # 开始处理每一页里的新闻URL
    # 不要
    def parse_news(self, html, page=1):
        html = etree.HTML(html)
        news_list = html.xpath('//div[@class="news-box"]/ul[@class="news-list"]/li')
        #logger.info('------正在解析第{}页，该页有{}条新闻------'.format(page, len(news_list)))
        for new in news_list:
            # logger.info('-' * 90)
            content_url = new.xpath('./div[@class="txt-box"]/h3/a/@href')[0]
            # 开始解析，增源，判重，发包
            self.source_sentenced_send(content_url)
            self.requests_totals_all += 1
            logger.info('已请求URL数量：{}'.format(self.requests_totals_all))

            if ACCOUNT_HOME_PAGE_ENABLED:
                # 进入该公众号页面，采集该页所有新闻
                s_p_url = new.xpath('./div[@class="txt-box"]/div[@class="s-p"]/a/@href')[0]
                for c in range(10):
                    s_p_response = self.s.get(s_p_url, cookies=self.cookies)
                    s_p_source = s_p_response.text
                    if re.search('var msgList = (.+?]});', s_p_source):
                        s_p_msgList = re.findall('var msgList = (.+?]});', s_p_source)[0]
                        s_p_list = json.loads(s_p_msgList).get('list')
                        for s_p in s_p_list:
                            # print('-' * 45)
                            content_url_new = re.sub(';', '&', s_p.get('app_msg_ext_info').get('content_url'))
                            if re.match('/s\?', content_url_new):
                                content_url_new = 'https://mp.weixin.qq.com' + content_url_new
                            # 开始解析，增源，判重，发包
                            self.source_sentenced_send(content_url_new)
                            self.requests_totals_all += 1
                            logger.info('已请求URL数量：', self.requests_totals_all)
                            time.sleep(0.3)
                            item_list = s_p.get('app_msg_ext_info').get('multi_app_msg_item_list')
                            if len(item_list):
                                for item in item_list:
                                    # print('-' * 25)
                                    content_url_new = re.sub(';', '&', item.get('content_url'))
                                    if re.match('/s\?', content_url_new):
                                        content_url_new = 'https://mp.weixin.qq.com' + content_url_new
                                    # 开始解析，增源，判重，发包
                                    self.source_sentenced_send(content_url_new)
                                    self.requests_totals_all += 1
                                    logger.info('已请求URL数量：', self.requests_totals_all)
                                    time.sleep(0.3)
                        break
                    else:
                        logger.info('进入该公众号页面---失败')
                        self.crack_sougou(s_p_response.url)

    # 解析，增源，判重，发包
    def source_sentenced_send(self, content_url):
        # 解析
        detail_result = self.parse_detail(content_url)
        if detail_result:
            # 增源
            if SOURCE_ADD_ENABLED:
                account_source_dic = detail_result['account_source_dic']
                self.account_to_source(name=account_source_dic['name'], account=account_source_dic['account'],
                                       collectiontime=account_source_dic['collectiontime'],
                                       biz=account_source_dic['biz'])

            sentenced_ls = detail_result['sentenced_ls']
            send_result = detail_result['send_result']

            # 判重
            if SENTENCED_ENABLED:
                # 判重：当前公众号的文章url是否已经存在
                existed_ls = self.sentenced_news_get(sentenced_ls)
                url_md5 = json.loads(sentenced_ls)[0].get('urls')[0]
                if url_md5 not in existed_ls:
                    logger.info('判重结果：这是新文章，添加到待发包中')
                    # 发包
                    if SEND_PACKAGE_ENABLED:
                        # 将该条数据添加到待发包中:数据中心
                        send_ok = self.send_news(send_result)
                        # 将该条数据添加到待添加判重缓存中
                        self.need_add_all.append(json.loads(sentenced_ls)[0])
                        # 发包成功，判重添加
                        if send_ok == 1:
                            sentenced_res = self.sentenced_news_add(json.dumps(self.need_add_all))
                            if sentenced_res['msg'] == '成功' and sentenced_res['status'] == 0:
                                logger.info('判重URL：添加成功，并清空待添加判重缓存列表')
                                self.need_add_all.clear()
                else:
                    logger.info('判重结果：这是旧文章，跳过')
                    logger.info('send_result_headers', send_result['headers'])

    # 解析每一条新闻URL，按照格式配置
    def parse_detail(self, content_url):
        print('content_url：', content_url)
        if not re.match('https?://mp\.weixin\.qq\.com', content_url):
            logger.info('parse_detail...传入url不符合规则...跳过：{}'.format(content_url))
            return None
        new_result = {
            'headers': {
                'topic': 'weixin',
                'key': '',
                'timestamp': '',
            },
            'body': {
                'ID': '',
                'Account': '',
                'TaskID': '',
                'TaskName': '',
                'AccountID': '',
                'SiteID': '',
                'TopicID': 1,
                'Url': '',
                'Title': '',
                'Content': '',
                'Author': '',
                'Time': '',
                'AddOn': '',
                'Tags': '',
                'DefinedSite': '',
                'CustomerID': '',
            }
        }
        page_source = ''
        page_source_ok = 0
        for i in range(10):
            try:
                response = self.s.get(content_url, cookies=self.cookies)
                page_source = response.text
                page_source_ok = 1
                break
            except Exception as e:
                logger.error('请求新闻详情页面失败，重试{}'.format(e))
                time.sleep(1)

        if len(page_source) and page_source_ok == 1:
            if re.search('此帐号被投诉且经审核涉嫌侵权', page_source):
                logger.info('------此帐号被投诉且经审核涉嫌侵权。此帐号已注销，内容无法查看。跳过------')
                return None
            elif re.search('该内容已被发布者删除', page_source):
                logger.info('------该内容已被发布者删除。跳过------')
                return None
            elif re.search('链接已过期', page_source):
                logger.info('------链接已过期。跳过------')
                return None
            elif re.search('访问过于频繁[，,]请用微信扫描二维码进行访问', page_source):
                logger.info('------访问过于频繁，请用微信扫描二维码进行访问。跳过------')
                time.sleep(10 * 60)
                return None
            try:
                nowtime_str = str(time.time()).split('.')[0]
                new_result['headers']['topic'] = 'weixin'
                new_result['headers']['timestamp'] = int(nowtime_str)
                html = etree.HTML(page_source)
                new_result['body']['Url'] = content_url
                new_result['body']['Title'] = html.xpath('//h2[@id="activity-name"]/text()')[0].strip()
                new_result['body']['Content'] = ''.join(html.xpath('//div[@id="js_content"]//text()')).strip()
                new_result['body']['Author'] = html.xpath('//div[@id="meta_content"]/span/a/text()')[0].strip()
                new_result['body']['Time'] = int(re.findall('var ct="(\d+)"', page_source)[0] + '000')
                new_result['body']['AddOn'] = int(nowtime_str + '000')
                new_result['body']['TaskName'] = '微信_' + new_result['body']['Author']

                account_source_collectiontime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                account_source_biz = ''
                if re.search('var biz = "" *\| *\| *"(.*?)"', page_source):
                    account_source_biz = re.findall('var biz = "" *\| *\| *"(.*?)"', page_source)[0]
                elif re.search('var biz = "(.*?)" *\| *\| *""', page_source):
                    account_source_biz = re.findall('var biz = "(.*?)" *\| *\| *""', page_source)[0]

                logger.info('该新闻标题：{}'.format(new_result['body']['Title']))
                logger.info('该新闻链接：{}'.format(content_url))

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
                        logger.info('------开始在该文章源码里查找系统分配原始微信号------')
                        new_result['body']['Account'] = re.findall('var user_name = "(.*?)"', page_source)[0]
                        if new_result['body']['Account']:
                            logger.info('------在该文章源码里查找系统分配原始微信号---成功：{}'.format(new_result['body']['Account']))
                            self.account_find_all[new_result['body']['Account']] = new_result['body']['Author']
                        else:
                            logger.info('------在该文章源码里查找系统分配原始微信号---失败：{}'.format(new_result['body']['Account']))

                # 获取AccountID
                if new_result['body']['Account']:
                    account_id = self.get_account_id(new_result['body']['Account'])
                    if account_id:
                        new_result['body']['TaskID'] = account_id
                        new_result['body']['AccountID'] = account_id
                        new_result['body']['SiteID'] = int(account_id)

                # 判重的keys，微信号+微信号ID的MD5
                sentenced_keys = new_result['body']['Account'] + new_result['body']['AccountID']
                h2 = hashlib.md5()
                h2.update(sentenced_keys.encode(encoding='utf-8'))
                sentenced_keys_md5 = h2.hexdigest()

                # 增源的数据格式
                account_source_dic = {
                    'name': new_result['body']['Author'],
                    'account': new_result['body']['Account'],
                    'collectiontime': account_source_collectiontime,
                    'biz': account_source_biz,
                }
                # print('account_source_dic', json.dumps(account_source_dic, indent=4, ensure_ascii=False))

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

                return {
                    'account_source_dic': account_source_dic,
                    'sentenced_ls': sentenced_ls,
                    'send_result': send_result,
                }

            except Exception as e:
                logger.error(e)
                logger.info('------该新闻不属于公众号文章，跳过------')
                return None
        else:
            logger.info('parse_detail...失败,page_source_ok：{}'.format(page_source_ok))
            logger.info('parse_detail...失败,page_source：{}'.format(page_source))
            return None

    # 根据微信号从数据库获取AccountId
    def get_account_id(self, account):
        account_id = ''
        params = {
            'token': GetAccountId_TOKEN,
            'account': account
        }
        url_resp = requests.get(url=GetAccountId_URL, params=params)
        account_res = json.loads(url_resp.text).get('results')
        if len(account_res):
            account_id = account_res[0].get('AccountID')
        else:
            res = my_sqlserver.get_account(account)
            if len(res):
                account_id = res[0][0]
        account_id = str(account_id)
        return account_id

    # 判断是否为新公众号，以微信号为判断依据，如是则增源
    def account_to_source(self, name, account, collectiontime, biz):
        res = my_sqlserver.get_account(account)
        if not len(res):
            logger.info('增源：该微信号是新的：{}'.format(account))
            url = 'http://weixin.sogou.com/gzh?openid'
            my_sqlserver.add_account(name=name, account=account, url=url, collectiontime=collectiontime, biz=biz)

    # 判重（获取url），返回该公众号所有已存在文章：Schedule/GetCacheWx
    def sentenced_news_get(self, sentenced_ls):
        params = {
            'keys': json.loads(sentenced_ls)[0].get('key'),
            'sourceNodes': SOURCENODES,
            'sourceType': SOURCETYPE,
        }
        url = GetCacheWx_URL_main
        # logger.info(params)
        while 1:
            try:
                response = requests.get(url=url, params=params, timeout=3)
                if response.status_code == 200:
                    res_data = response.json().get('data')
                    if len(res_data) == 0:
                        return []
                    else:
                        existed_ls = res_data[0].get('urls')
                        return existed_ls
            except Exception as e:
                logger.error('{}请求失败，重试...{}'.format(url, e))
                time.sleep(1)

    # 判重（添加url），往公众号添加这个新文章：Schedule/CacheWx
    def sentenced_news_add(self, need_add_all):
        url = CacheWx_URL_main
        if need_add_all:
            # 发包成功了，就把这些数据添加到判重缓存中
            while 1:
                try:
                    response = requests.post(url=url, data=need_add_all, timeout=3)
                    if response.status_code == 200:
                        return response.json()
                except Exception as e:
                    logger.error(e)
                    logger.info('{}请求失败，重试...'.format(url))
                    time.sleep(1)

    # 解析后列表序列化并发送:数据中心
    def send_news(self, send_result):
        # logger.info('send_result_headers', send_result['headers'])
        send_ok = 0
        url_1 = SEND_URL_1
        if send_result:
            if sys.getsizeof(json.dumps(send_result)) >= 1 * 1024 * 1024:
                logger.info('这条数据大于1M，添加到待发包中失败，跳过...')
                return
            # 将该条数据添加到待发包中
            self.need_send_all.append(send_result)
            datacenter_Yweixin = [
                {
                    "headers": {
                        "topic": "Yweixin",
                    },
                    "body": json.dumps(self.need_send_all)
                },
            ]
            json_result_Yweixin = json.dumps(datacenter_Yweixin)
            json_result = json.dumps(self.need_send_all)
            if sys.getsizeof(json_result) >= MAX_SEND_SIZE:
                logger.info('数据中心:待发包数据已达到{}k，数量为{}，开始发包'.format(MAX_SEND_SIZE // 1024, len(self.need_send_all)))
                while 1:
                    try:
                        send_response1 = requests.post(url=url_1, data=json_result)
                        if send_response1.status_code == 200:
                            self.need_send_all.clear()
                            logger.info('数据中心:发包成功，并清空待发包数据列表')
                            send_ok = 1
                            return send_ok
                    except Exception as e:
                        logger.error(e)
                        logger.info('数据中心:发包失败，重试...')
                        time.sleep(1)
        else:
            logger.info('解析后返回结果为空，不添加到待发包中!')
            return send_ok

    # 如果新闻页面没有显示微信号，则根据公众号查出来
    def find_account(self, author):
        account = ''

        # 查找记录只保存100条
        if len(self.account_find_all) > 100:
            self.account_find_all.clear()

        if author in self.account_find_all.values():
            logger.info('--开始在查找记录中找微信号：{}--'.format(author))
            for k, v in self.account_find_all.items():
                if v == author:
                    logger.info('--成功查找微信号：{}--'.format(author))
                    account = k
        else:
            logger.info('--开始在网页查找微信号：{}--'.format(author))
            url = 'https://weixin.sogou.com/weixin'
            params = {
                'type': 1,
                'query': author,
                'ie': 'utf8',
                's_from': 'input',
                '_sug_': 'y',
            }
            for c in range(10):
                response = requests.get(url, params=params, cookies=self.cookies)
                page_source = response.text
                if re.search('<label name="em_weixinhao">(.*?)</label>', page_source):
                    account = re.findall('<label name="em_weixinhao">(.*?)</label>', page_source)[0]
                    logger.info('--成功查找微信号：{}--'.format(author))
                    self.account_find_all[account] = author
                    break
                elif re.search('<p class="p1">呀！</p>', page_source):
                    logger.info('暂无与“{}”相关的官方认证订阅号。。'.format(author))
                    break
                else:
                    self.crack_sougou(response.url)
        if account == '':
            logger.info('--查找{}的微信号失败--'.format(author))
        return account

    # 退出selenium
    def quit(self):
        self.browser.quit()
        logger.info('关闭selenium')

    # 开始运行
    def run(self, search_key, DEMO_TYPE, ft_et_list):
        if DEMO_TYPE == 1 and ft_et_list != []:
            logger.info('任务采集：一天')
            self.get_news_other(search_key, data_type=1)

            logger.info('任务采集：{} 至 {}'.format(ft_et_list[-1], ft_et_list[0]))
            for ft in ft_et_list:
                et = ft
                data_type = 5
                self.get_news_between(search_key, data_type, ft, et)

            logger.info('任务采集：一周')
            self.get_news_other(search_key, data_type=2)

        if DEMO_TYPE == 2:
            logger.info('日常采集：默认 一天 一周')
            for data_type in [0, 1, 2]:
                self.get_news_other(search_key, data_type)
                
# 通过接口获取新闻关键字
def get_api_keys():
    key_list = []
    key_api_0 = 'http://10.194.12.106:8002/nextaccount?label=0'
    key_api_1 = 'http://10.194.12.106:8002/nextaccount?label=1'

    result = json.loads(requests.get(key_api_0).text)
    logger.info('get_api_keys:{}'.format(result))
    logger.info(result)
    for k in result:
        key_list.append(k.get('name'))
    logger.info(key_list)

    if key_list != []:
        logger.info('调用关键字接口：key_api_0')
        return key_list

    else:
        result = json.loads(requests.get(key_api_1).text)
        for k in result:
            key_list.append(k.get('name'))
        logger.info('调用关键字接口：key_api_1')
        return key_list

# 通过txt文件获取新闻关键字
def get_txt_keys():
    # 关键字txt文件路径
    keys_file_path = os.path.join(FILES_DIR, KEYS_FILE_NAME)
    logger.info('KEYS_FILE_PATH', keys_file_path)

    key_list = []
    if os.path.exists(keys_file_path):
        if os.path.isfile(keys_file_path):
            with open(keys_file_path, mode='r', encoding='utf-8') as f:
                for i in f.readlines():
                    key_list.append(i.strip())
        else:
            logger.info('该文件名不存在！请检查是否为正确文件名：{}'.format(keys_file_path))
    else:
        logger.info('该路径不存在！请检查该路径是否正确：{}'.format(keys_file_path))

    return key_list


# 返回最近三天的日期列表,如：['2018-09-25', '2018-09-24', '2018-09-23']
def get_date_list():
    base_date_str = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    date_need_list = [base_date_str]
    base_date = datetime.datetime.strptime(base_date_str, '%Y-%m-%d')
    for i in range(-1, -3, -1):
        delta = datetime.timedelta(days=i)
        n_days = base_date + delta
        n_days = n_days.strftime('%Y-%m-%d')
        date_need_list.append(n_days)

    date_need_list = date_need_list[::-1]
    logger.info('date_need_list：{}'.format(date_need_list))
    return date_need_list


if __name__ == '__main__':
    url = 'https://weixin.sogou.com/weixin'
    sougou_weixin = SougouWeixin(url)
    while 1:
        try:
            logger.info('请求关键词接口...')
            key_list = get_api_keys()
            # key_list = ['读书']    # 本地调试
            if TXT_ENABLED:
                logger.info('读取TXT文件内关键词...')
                key_list = get_txt_keys()
            if key_list:
                ft_et_list = []
                if DEMO_TYPE == 3:
                    ft_et_list = get_date_list()
                for search_key in key_list:
                    if search_key:
                        for i in range(10):
                            try:
                                logger.info('开始采集...新闻关键词：{}'.format(search_key))
                                sougou_weixin.run(search_key, DEMO_TYPE, ft_et_list)
                                logger.info('采集完毕...新闻关键词：{}'.format(search_key))
                                time.sleep(1)
                                break
                            except Exception as e:
                                logger.error('程序报错中止：{}'.format(e))
                                continue
                sougou_weixin.quit()
                logger.info('10秒后重启selenium')
                sougou_weixin = SougouWeixin(url)
            time.sleep(10)
        except Exception as e:
            logger.error('程序报错中止：{}'.format(e))
            continue
