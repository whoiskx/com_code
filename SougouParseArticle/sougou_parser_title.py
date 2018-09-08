# -*- coding: utf-8 -*-
import os
import sys
import re
import json
import time
import jieba
import random
import hashlib
import requests
import datetime
import urllib.parse
from io import BytesIO
from PIL import Image
from lxml import etree
from collections import Counter
from SougouParseArticle.config import *
from fake_useragent import UserAgent
from SougouParseArticle.captch_dytry import captch_upload_image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SougouWexin(object):
    def __init__(self, data):
        self.url = 'https://weixin.sogou.com/weixin'
        # 查询的关键词
        self.search_key = data.get('title')
        # 相同标题的文章内容列表
        self.useful_datalist = [data]
        # 该新闻关键词查询下有多少条新闻
        self.news_totals_all = 0

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
        self.wait = WebDriverWait(self.browser, 10)

    # 获取随机User-Agent
    def get_ua(self):
        user_agent = UserAgent().random
        print('Get User-Agent:', user_agent)
        return user_agent

    # 查找相关新闻，全部
    def get_news_all(self, search_key):
        print('------正在搜索：{}    采集时间范围：全部------'.format(search_key))
        # 该新闻一共有多少页
        page_total = 1
        # 是否进行后续的请求
        requests_flag = 0

        while 1:
            params = {
                'query': search_key,
                'type': 2,
                'ie': 'utf8',
            }
            referer_param = urllib.parse.urlencode({'query': search_key})
            referer = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=input&_sug_=y&_sug_type_=&page=1&' + referer_param
            self.headers['Referer'] = referer
            response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            news_total_text = response.text
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
            elif re.search('没有找到相关的微信公众号文章', news_total_text):
                print('------没有找到相关的微信公众号文章------')
                break
            elif (
                    re.search('id="hint_container"', news_total_text)
                    and re.search('id="pagebar_container"', news_total_text) == None
            ):
                print('------当前搜索只有一页------')
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
        }
        if requests_flag:
            for i in range(0, page_total):
                page = i + 1
                params['page'] = page
                self.headers['User-Agent'] = self.get_ua()
                # 对该页发起请求
                print('------正在请求第{}页------'.format(page))
                res = self.requests_news(params, page)
                if res['stop_to_next'] == 1 or res['find_same_title_flag'] == 0:
                    break
                time.sleep(1)

    # 对每一页发起请求
    def requests_news(self, params, page):
        # 该页没有文章或只有一页为1则退出，正常为0则继续
        stop_to_next = 0
        # 是否有相同标题的，有是1则继续，没有是0则退出
        find_same_title_flag = 0
        for c in range(20):
            response = self.s.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            page_source = response.text
            if self.judge_news(page_source):
                find_same_title_flag = self.parse_news(page_source, page)
                time.sleep(1)
                break
            elif re.search('没有找到相关的微信公众号文章', page_source):
                print('------没有找到相关的微信公众号文章------')
                stop_to_next = 1
                break
            elif (
                    re.search('id="hint_container"', page_source)
                    and re.search('id="pagebar_container"', page_source) == None
            ):
                print('------当前搜索只有一页------')
                stop_to_next = 1
                break
            else:
                self.crack_sougou(response.url)
        return {
            'stop_to_next': stop_to_next,
            'find_same_title_flag': find_same_title_flag
        }

    # 判断是否正确请求到新闻页面
    def judge_news(self, page_source):
        html = etree.HTML(page_source)
        news_list = html.xpath('//div[@class="news-box"]/ul[@class="news-list"]/li')
        if len(news_list) > 0:
            print('------成功跳转到新闻页面，开始爬取------')
            return True
        else:
            print('------未成功跳转到新闻页面！！------')
            return False

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
                            print('---1111111---验证码输入错误------')
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
                        print('--22222222----验证码输入错误------')
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

    # 开始处理每一页里的新闻URL
    def parse_news(self, html, page=1):
        # 在该页是否找到相同标题内容
        find_same_title_flag = 0
        html = etree.HTML(html)
        news_list = html.xpath('//div[@class="news-box"]/ul[@class="news-list"]/li')
        print('------正在解析第{}页，该页有{}条新闻------'.format(page, len(news_list)))
        for new in news_list:
            print('-' * 45)
            content_url = new.xpath('./div[@class="txt-box"]/h3/a/@href')[0]
            # 开始解析
            res = self.parse_detail(content_url)
            if res == 1:
                find_same_title_flag = 1
        return find_same_title_flag

    # 解析每一条新闻URL，按照格式配置
    def parse_detail(self, content_url):
        find_same_flag = 0
        print('content_url：', content_url)
        if not re.match('https?://mp\.weixin\.qq\.com', content_url):
            print('parse_detail...传入url不符合规则...跳过：{}'.format(content_url))
            return None
        response = self.s.get(content_url, cookies=self.cookies)
        page_source = response.text
        if re.search('此帐号被投诉且经审核涉嫌侵权', page_source):
            print('------此帐号被投诉且经审核涉嫌侵权。此帐号已注销，内容无法查看。跳过------')
            return None
        elif re.search('该内容已被发布者删除', page_source):
            print('------该内容已被发布者删除。跳过------')
            return None
        try:
            result = {
                'title': '',
                'content': '',
                'timestamp': None,
            }
            html = etree.HTML(page_source)
            result['title'] = html.xpath('//h2[@id="activity-name"]/text()')[0].strip()
            print('title：', result['title'])
            result['content'] = ''.join(html.xpath('//div[@id="js_content"]//text()')).strip()
            print('content：', result['content'])
            result['timestamp'] = int(re.findall('var ct="(\d+)"', page_source)[0])
            print('timestamp：', result['timestamp'])
            if result['title'] and result['content'] and result['timestamp']:
                print('search_key：', self.search_key)
                if result['title'] == self.search_key:
                    print('----找到相同标题文章----')
                    find_same_flag = 1
                    self.useful_datalist.append(result)
                return find_same_flag
            else:
                print('解析标题或内容为空')
                return None
        except Exception as e:
            print(e)
            print('------该新闻不属于公众号文章，跳过------')
            return None

    # 对useful_datalist进行数据统计分析
    def data_to_analysis(self, useful_datalist):
        print('进行数据统计分析', len(useful_datalist), useful_datalist)
        result = {
            "Success": False,
            "Message": "没有相关文章",
            "Title": None,
            "TransQuan": None,
            "KeyWords": None,
        }
        # 传播量信息
        trans_quan = {
            "FirstArt": {
                "Time": "",
                "Title": ""
            },
            "TransTime": {
                "TranSpan": "",
                "TranDate": ""
            },
            "Peak": {
                "peakArtDate": "",
                "peakArtCount": None
            },
            "ArtPubTimeArea": [
                {"00:00-04:00": 0},
                {"04:00-08:00": 0},
                {"08:00-12:00": 0},
                {"12:00-16:00": 0},
                {"16:00-20:00": 0}
            ]
        }
        # 文章的舆论关键词  {"times": None,"keyword": ""}
        key_words = {
            "list": []
        }
        if len(self.useful_datalist):
            # 按照发文时间戳从小到大（从早到晚）排序
            useful_datalist = sorted(useful_datalist, key=lambda x: x['timestamp'])
            print(json.dumps(useful_datalist, indent=4, ensure_ascii=False))
            result['Success'] = True
            result['Message'] = ''
            result['Title'] = self.search_key

            # 所有文章内容列表
            content_all_list = []
            # 所有时间戳进行格式处理 2018/07/08 1:15:39
            time_all_list = []
            # 所有时间戳进行格式处理日期 2018/07/08
            time_date_list = []
            # 所有时间戳进行格式处理时间 1:15:39
            time_time_list = []
            for i in useful_datalist:
                content_all_list.append(i['content'])
                time_str = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(i['timestamp']))
                res = re.split(' ', time_str)
                time_all_list.append(time_str)
                time_date_list.append(res[0])
                time_time_list.append(res[1])

            # 首发文章信息
            trans_quan['FirstArt']['Time'] = time_all_list[0]
            trans_quan['FirstArt']['Title'] = self.search_key

            # 传播时长信息
            d1 = datetime.datetime.strptime(time_all_list[0], "%Y/%m/%d %H:%M:%S")
            d2 = datetime.datetime.strptime(time_all_list[-1], "%Y/%m/%d %H:%M:%S")
            tran_span = d2 - d1
            second_total = tran_span.seconds
            d = tran_span.days
            h = second_total // (60 * 60)
            m = (second_total - 60 * 60 * h) // 60
            trans_quan['TransTime']['TranSpan'] = '{}天{}小时{}分'.format(d, h, m)
            trans_quan['TransTime']['TranDate'] = '{} 至 {}'.format(time_all_list[0], time_all_list[-1])

            # 相似文章最多的文章标题，当天发文数量
            peak_res = Counter(time_date_list).most_common(1)
            trans_quan['Peak']['peakArtDate'] = peak_res[0][0]
            trans_quan['Peak']['peakArtCount'] = peak_res[0][1]

            # 各个时间段文章的传播量
            for i in time_time_list:
                t = int(i[:2])
                if 0 <= t < 4:
                    trans_quan['ArtPubTimeArea'][0]['00:00-04:00'] += 1
                elif 4 <= t < 8:
                    trans_quan['ArtPubTimeArea'][1]['04:00-08:00'] += 1
                elif 8 <= t < 12:
                    trans_quan['ArtPubTimeArea'][2]['08:00-12:00'] += 1
                elif 12 <= t < 16:
                    trans_quan['ArtPubTimeArea'][3]['12:00-16:00'] += 1
                elif 16 <= t <= 20:
                    trans_quan['ArtPubTimeArea'][4]['16:00-20:00'] += 1

            # 分词处理
            key_words_list = []
            seg_list = jieba.cut(''.join(content_all_list), cut_all=False)
            for i in seg_list:
                if len(i) >= 2 and re.match('[\u4e00-\u9fff]+', i):
                    key_words_list.append(i)

            # 返回前10个出现频率最高的词
            key_words_counter = Counter(key_words_list).most_common(10)
            for k in key_words_counter:
                key_words['list'].append(
                    {
                        "times": k[1],
                        "keyword": k[0]
                    }
                )

            result['TransQuan'] = trans_quan
            result['KeyWords'] = key_words
        return result

    # 从底层数据库获取所有相同标题的内容，并添加到useful_datalist
    def get_from_db(self):
        params = {
            'sort': 'Time desc',
            'word': self.search_key,
            'fl': 'title,content,time',
            'categories': 2,
        }
        response = requests.get(SELECT_API_URL, params=params)
        response = response.json()
        for res in response['results']:
            if res['Title'] == self.search_key:
                new_res = {
                    'title': res['Title'],
                    'content': res['Title'],
                    'timestamp': int(res['Time'][:-3]),
                }
                self.useful_datalist.append(new_res)

    # 开始运行
    def run(self):
        # 在搜狗微信上找所有标题相同内容
        self.get_news_all(self.search_key)
        # 在底层数据上找所有标题相同内容
        self.get_from_db()
        # 所有都查询完毕，对useful_datalist进行数据统计分析
        result = self.data_to_analysis(self.useful_datalist)
        # 关闭selenium
        self.browser.quit()
        return result


if __name__ == '__main__':
    dic = {"title": "2倍速追剧背后的焦虑", "content": "aaaa", "timestamp": 1234567}
    parse_title = SougouWexin(dic)
    result = parse_title.run()
    print('程序运行结果：')
    print(json.dumps(result, indent=4, ensure_ascii=False))
