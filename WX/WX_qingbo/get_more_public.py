import datetime
import re

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
import urllib.parse
import os
import pymysql
from send_backpack import JsonEntity, Acount, Article
from pyquery import PyQuery as pq

conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun

current_dir = os.getcwd()
log_dir = os.path.join(current_dir, 'wx_log.txt')

MYSQL_HOST = '192.168.1.21'
MYSQL_PORT = 8001
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'ABCd1234'
MYSQL_DATABASE = 'mysql'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
    'passwd': MYSQL_PASSWORD
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open(log_dir, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


class PublicDetails(object):
    def __init__(self):
        self.driver = None
        self.name = ''
        self.read_num = ''
        self.praise = ''
        self.name_list = []

    @staticmethod
    def get_driver():
        # 使用headless无界面浏览器模式
        # options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=options)

        driver = webdriver.Chrome()
        # driver = webdriver.PhantomJS()
        return driver

    @staticmethod
    def date_to_timestamp(before_time):
        # 格式化时间 '2017-03-16 18:22:06'
        ts = time.strptime(before_time, "%Y-%m-%d %H:%M:%S")
        return str(int(time.mktime(ts)))

    def public_name(self):
        url = 'http://183.131.241.60:38011/nextaccount?label=0'
        resp = requests.get(url)
        # print(resp.text)
        datas = json.loads(resp.text)
        name_list = []
        for d in datas:
            name = d.get('name')
            name_list.append(name)
        log('name_list', name_list)
        return name_list

    def login_website(self):
        if self.driver is None:
            self.driver = self.get_driver()
        url = "http://www.gsdata.cn"
        self.driver.get(url)
        time.sleep(2)
        register_login = self.driver.find_element_by_class_name('useinfo').find_elements_by_tag_name('a')
        login = register_login[1]
        login.click()
        time.sleep(3)
        input_button = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/a[2]/img')
        input_button.click()
        time.sleep(2)

        login_button = self.driver.find_element_by_xpath('//*[@id="login-form"]/div/div[1]/input')
        password_button = self.driver.find_element_by_xpath('//*[@id="login-form"]/div/div[2]/input')

        login_button.send_keys('18390553540')
        password_button.send_keys('qb123258456')
        button = self.driver.find_element_by_xpath('//*[@id="login-form"]/div/div[4]/button')
        time.sleep(1)
        button.click()
        time.sleep(2)

    def get_numb(self, name, count):
        # 50次重新定位到搜索主页
        if count % 500 == 0 and count != 0:
            print("重置主页")
            if self.driver is not None:
                log(self.driver.current_url)
                self.driver.quit()
            self.driver = self.get_driver()
            self.login_website()
            time.sleep(3)
        # 点击搜索
        search_input = self.driver.find_element_by_xpath('//*[@id="search_input"]')
        name = '射阳论坛'
        search_input.clear()
        search_input.send_keys(name)
        search_button = self.driver.find_element_by_class_name('search_wx')
        search_button.click()
        time.sleep(2.5)

        # 发包列表

        backpack_list = [
            {
                "headers": {
                    "topic": "datacenter",
                    "key": None,
                    "timestamp": int(time.time())
                },
                "body": "{}"
            }
        ]
        body = []
        public_divs = self.driver.find_elements_by_css_selector('.clearfix.list_query')
        for public_div in public_divs:
            if '提交入库' not in public_div.text:
                # 点击进入公众号
                gxh = public_div.find_element_by_id('nickname')
                gxh.click()
                time.sleep(2)

                all_handles = self.driver.window_handles  # 获取到当前所有的句柄,所有的句柄存放在列表当中
                '''获取非最初打开页面的句柄'''
                if len(all_handles) > 1:
                    # for index, handles in enumerate(all_handles):
                    #     if index == 1:
                    self.driver.switch_to.window(all_handles[1])
                    time.sleep(0.5)
                    try:
                        # 获取公众号 ID, 名称, 微信号
                        account = Acount()
                        account.name = self.driver.find_element_by_class_name('fs22').text
                        wx_num = self.driver.find_element_by_class_name('info-li').text.split('\n')[0]
                        account.account = wx_num.split("：")[-1]
                        get_account_id_url = 'http://60.190.238.178:38010/search/common/wxaccount/select?token=9ef358ed-b766-4eb3-8fde-a0ccf84659db&account={}'.format(
                            account.account)
                        url_resp = requests.get(get_account_id_url)
                        json_obj = json.loads(url_resp.text)
                        results = json_obj.get('results')
                        account.account_id = ''
                        for i in results:
                            account.account_id = i.get('AccountID')
                            break

                        for i in range(2):
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(0.5)

                        # 得到所有文章并解析
                        data_all = self.driver.find_elements_by_css_selector('.wxDetail.bgff')
                        datas = data_all[-1]
                        items = datas.find_elements_by_class_name('clearfix')
                        for count, item in enumerate(items):
                            if count == 0:
                                continue
                            url = item.find_element_by_tag_name('a').get_attribute('href')
                            title = item.find_element_by_class_name('cr30').text
                            read_num = item.find_element_by_css_selector('.wxAti-info').find_element_by_tag_name(
                                'span').text
                            praise_num = \
                                (item.find_element_by_css_selector('.wxAti-info').find_elements_by_tag_name('span'))[
                                    -1].text
                            article_time = item.find_element_by_class_name('fr').text
                            log(name, read_num, praise_num)
                            # save_all = {
                            #     'url': url,
                            #     'read_num': read_num,
                            #     'praise_num': praise_num,
                            #     'title': title,
                            #     'public_url': self.driver.current_url,
                            #     'insert_time': datetime.datetime.now()
                            # }
                            # 发送到队列
                            # parsed_url = urllib.parse.quote(url)
                            # upload_url = 'http://183.131.241.60:38011/InsetUrl?url={}&views={}&praises={}'.format(
                            #     parsed_url, read_num, praise_num)
                            # requests.get(upload_url)

                            cursor.execute(
                                "INSERT INTO wechat_qingbo_copy(current_url, article_url, read_num, praise_num, insert_time) VALUES (%s, %s, %s, %s, %s)",
                                (self.driver.current_url, url, read_num, praise_num, datetime.datetime.now()))
                            db.commit()

                            # 文章解析
                            article = Article()
                            resp = requests.get(url)
                            article_html = resp.text
                            article_timestramp_before = re.search('var ct=".*?"', article_html).group()
                            article_timestramp = re.search('\d+', article_timestramp_before).group()
                            e = pq(article_html)
                            # account = e("#js_name")
                            article_content = e("#js_content").text()
                            # article_author = e("")

                            article.url = url
                            article.title = title
                            article.content = article_content.replace('\n', '')
                            article.author = account.name
                            article.From = account.name
                            article.time = article_timestramp + '000'

                            wx_entity = JsonEntity(article, account)
                            wx_dict = {
                                'ID': wx_entity.id,
                                'Account': wx_entity.account,
                                'TaskID': wx_entity.task_id,
                                'TaskName': wx_entity.task_name,
                                'AccountID': wx_entity.account_id,
                                # GroupName
                                'SiteID': wx_entity.site_id,
                                'TopicID': 0,
                                'Url': wx_entity.url,
                                'Title': wx_entity.title,
                                'Content': wx_entity.content,
                                'Author': wx_entity.author,
                                'Praises': praise_num,
                                'Views': read_num,

                                # "From": None,
                                'Time': wx_entity.time,

                                # \"Views\\\":0,\\\"Praises\\\":0,
                                #  "Hash\\\":\\\"

                                'AddOn': wx_entity.addon + '000'
                            }
                            body.append(wx_dict)

                            urun['wx_http'].insert(wx_dict)
                    except Exception as e:
                        log(e)
                        self.driver.close()
                        # for index, handles in enumerate(all_handles):
                        #     if index == 0:
                        self.driver.switch_to.window(all_handles[0])
                        return 'error windows'

                    self.driver.close()
                    # for index, handles in enumerate(all_handles):
                    #     if index == 0:
                    self.driver.switch_to.window(all_handles[0])

            else:
                log('not found available public')
                return 'not found'

        # 构造并发包
        backpack_list[0].get(body).format(body)
        print(backpack_list)

    def run(self):
        self.login_website()
        count = 0
        while True:
            try:
                log('request count {}'.format(count))
                self.name_list = self.public_name()
                for name in self.name_list:
                    try:
                        log('start name {}'.format(name))
                        self.get_numb(name, count)
                    except Exception as e:
                        log(e)
                        if 'timeout' in str(e):
                            self.driver.get('http://www.gsdata.cn/query/wx?q=%E5%BC%80%E8%AF%9A%E5%BF%AB%E5%8D%B0')
                            time.sleep(1)
                    count += 1
                time.sleep(3)
                count += 1
            except Exception as e:
                log('error afsdfadfsd')
                log(e)
                if self.driver is not None:
                    log(self.driver.current_url)
                    self.driver.quit()
                self.driver = self.get_driver()
                self.login_website()
                count += 1
                continue
        print('haha')


if __name__ == '__main__':
    test = PublicDetails()
    test.run()
