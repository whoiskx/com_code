import datetime
import re

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pymysql
from send_backpack import JsonEntity, Acount, Article
from pyquery import PyQuery as pq

current_dir = os.getcwd()
log_dir = os.path.join(current_dir, 'wx_log.txt')

MYSQL_HOST = '121.28.84.254'
MYSQL_PORT = 7101
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'YunRun2018!@#'
MYSQL_DATABASE = 'test'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'passwd': MYSQL_PASSWORD,
    'db': MYSQL_DATABASE,
    'charset': 'utf8'
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    # print(dt, *args, **kwargs)
    with open(log_dir, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


class PublicDetails(object):
    def __init__(self):
        self.driver = None
        self.name = ''
        self.read_num = ''
        self.praise = ''
        self.name_list = []

    def get_driver(self):
        # 使用headless无界面浏览器模式
        # options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=options)
        if self.driver:
            self.driver.quit()
        self.driver = webdriver.Chrome()
        # driver = webdriver.PhantomJS()
        return self.driver

    def restart_driver(self):
        if self.driver:
            self.driver.quit()
        self.driver = self.get_driver()
        self.login_website()
        time.sleep(2)

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

    def parse_articles(self):
        backpack_list = []
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
            if results == []:
                log('account_id is None')
                return None
            account.account_id = ''
            # todo 没有accountID 怎么做
            for i in results:
                account.account_id = i.get('AccountID')
                break

            for i in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)

            # 得到所有文章并解析存储
            data_all = self.driver.find_elements_by_css_selector('.wxDetail.bgff')
            datas = data_all[-1]
            if '该公众号暂无数据' in datas.text:
                log('该公众号暂无数据')
                return None
            items = datas.find_elements_by_class_name('clearfix')
            for count, item in enumerate(items):
                if count == 0:
                    continue
                # if count == 6:
                #     break
                url = item.find_element_by_tag_name('a').get_attribute('href')
                title = item.find_element_by_class_name('cr30').text
                read_num = item.find_element_by_css_selector('.wxAti-info').find_element_by_tag_name(
                    'span').text
                praise_num = \
                    (item.find_element_by_css_selector('.wxAti-info').find_elements_by_tag_name('span'))[
                        -1].text
                log(account.name, read_num, praise_num)

                # 文章解析
                article = Article()
                resp = requests.get(url)
                article_html = resp.text
                # 文章可能被删除
                if '该内容已被发布者删除 ' in article_html:
                    log('该内容已被发布者删除')
                    continue
                article_timestramp_before = re.search('var ct=".*?"', article_html).group()
                article_timestramp = re.search('\d+', article_timestramp_before).group()
                e = pq(article_html)
                article_content = e("#js_content").text()

                article.url = url
                article.title = title.replace(' ', '')
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
                    'SiteID': int(wx_entity.site_id),
                    'TopicID': 0,
                    'Url': wx_entity.url,
                    'Title': wx_entity.title,
                    'Content': wx_entity.content,
                    'Author': wx_entity.author,
                    'Praises': praise_num,
                    'Views': read_num,
                    'Time': int(wx_entity.time),
                    'AddOn': int(wx_entity.addon + '000'),
                }

                # 构造并发包
                send_http_body = {
                    "headers": {
                        "topic": "weixin",
                        "key": wx_entity.id,
                        "timestamp": int(time.time()),
                    }
                }
                send_http_body.update({'body': json.dumps(wx_dict)})
                backpack_list.append(send_http_body)

                # 上传数据库
                cursor.execute(
                    "INSERT INTO wechat_qingbo(current_url, article_url, read_num, praise_num, addon, account, account_id, author, id, title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                    (self.driver.current_url, url, read_num, praise_num, datetime.datetime.now(),
                     wx_entity.account, wx_entity.account_id, wx_entity.author, wx_entity.id, wx_entity.title))
                db.commit()
                # urun['wx_http2'].insert(wx_dict)
        except Exception as e:
            log('error send', e)

            return None

        return backpack_list

    def get_numb(self, name, count):
        # 50次重新定位到搜索主页
        if count % 400 == 0 and count != 0:
            log("重启浏览器")
            self.restart_driver()
        # 点击搜索
        search_input = self.driver.find_element_by_xpath('//*[@id="search_input"]')
        # name = '杭州解百ALT专卖店'
        search_input.clear()
        search_input.send_keys(name)
        search_button = self.driver.find_element_by_class_name('search_wx')
        search_button.click()
        time.sleep(2.5)

        # 公众号列表
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
                    if len(all_handles) > 2:
                        self.restart_driver()
                        return None
                    # for index, handles in enumerate(all_handles):
                    #     if index == 1:
                    self.driver.switch_to.window(all_handles[-1])
                    time.sleep(0.5)
                    backpack_list = self.parse_articles()
                    # log('backpack_list', backpack_list)
                    # 发包
                    if backpack_list is not None:
                        url1 = 'http://115.231.251.252:26016/'
                        url2 = 'http://60.190.238.168:38015/'
                        body = json.dumps(backpack_list)
                        count = 0

                        while True:
                            if count > 2:
                                break
                            try:
                                log('start uploads')
                                r = requests.post(url1, data=body)
                                if r.status_code == 200:
                                    log('ok1')
                            except Exception as e:
                                log('send http error', e)
                            try:
                                r2 = requests.post(url2, data=body)
                                if r2.status_code == 200:
                                    log('ok2')
                                    break
                            except Exception as e:
                                log(e, 'send http error')
                            count += 1

                        self.driver.close()
                        # for index, handles in enumerate(all_handles):
                        #     if index == 0:
                        time.sleep(0.5)
                        self.driver.switch_to.window(all_handles[0])

                    else:
                        log('backpack_list is None')
                        self.driver.close()
                        # for index, handles in enumerate(all_handles):
                        #     if index == 0:
                        time.sleep(0.5)
                        self.driver.switch_to.window(all_handles[0])
            else:
                log('not found available public')

    def run(self):
        try:
            self.login_website()
        except Exception as e:
            log('login error')
            self.driver.quit()
            return None

        count = 0
        while True:
            try:
                log('request count {}'.format(count))
                self.name_list = self.public_name()
                for name in self.name_list:
                    try:
                        count += 1
                        log('start name {}'.format(name))
                        self.get_numb(name, count)
                    except Exception as e:
                        log('get_numb error', e)
                        # if 'timeout' in str(e):
                        #     url = 'http://www.gsdata.cn/query/wx?q=%E5%BC%80%E8%AF%9A%E5%BF%AB%E5%8D%B0'
                        #     self.driver.get(url)
                        #     time.sleep(1)
                        # else:
                        self.restart_driver()
            except Exception as e:
                log('run error', e)
                self.restart_driver()
                continue
        # log('haha')


if __name__ == '__main__':
    while True:
            test = PublicDetails()
            test.run()
            log('dafasdf')
            if test.driver:
                test.driver.quit()
