import datetime

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
import urllib.parse
import os
import pymysql
# conn = pymongo.MongoClient('127.0.0.1', 27017)
# urun = conn.urun

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

    def get_public_name(self):
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
            # 使用headless无界面浏览器模式
            # options = Options()
            # options.add_argument('--headless')
            # # options.add_argument('--disable-gpu')
            # self.driver = webdriver.Chrome(chrome_options=options)
            # self.driver = webdriver.PhantomJS()
            self.driver = webdriver.Chrome()
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
        # current_time = time.strftime(':%M:%S', time.localtime(int(time.time())))
        if count % 100 == 0:
            print("重置主页")
            if self.driver is not None:
                log(self.driver.current_url)
                # log(self.driver.page_source)
                self.driver.quit()
            # 使用headless无界面浏览器模式
            # options = Options()
            # options.add_argument('--headless')
            # # options.add_argument('--disable-gpu')
            # self.driver = webdriver.Chrome(chrome_options=options)
            # self.driver = webdriver.PhantomJS()
            self.driver = webdriver.Chrome()
            self.login_website()
            time.sleep(3)
        # 点击搜索
        search_input = self.driver.find_element_by_xpath('//*[@id="search_input"]')
        # search_input.send_keys('富翁俱乐部 ')
        # name = 'cube'
        search_input.clear()
        search_input.send_keys(name)
        search_button = self.driver.find_element_by_class_name('search_wx')
        search_button.click()
        time.sleep(2.5)

        public_divs = self.driver.find_elements_by_css_selector('.clearfix.list_query')
        for public_div in public_divs:
            if '提交入库' not in public_div.text:
                gxh = public_div.find_element_by_id('nickname')
                gxh.click()
                time.sleep(2)

                all_handles = self.driver.window_handles  # 获取到当前所有的句柄,所有的句柄存放在列表当中
                # print(all_handles)
                '''获取非最初打开页面的句柄'''
                if len(all_handles) > 1:
                    for index, handles in enumerate(all_handles):
                        if index == 1:
                            self.driver.switch_to_window(handles)
                    time.sleep(2)
                    for i in range(2):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.5)
                    # html = self.driver.page_source
                    # print(html)
                    # 得到所有文章并解析
                    data_all = self.driver.find_elements_by_css_selector('.wxDetail.bgff')
                    datas = data_all[-1]
                    items = datas.find_elements_by_class_name('clearfix')
                    for count, item in enumerate(items):
                        if count == 0:
                            continue
                        url = item.find_element_by_tag_name('a').get_attribute('href')
                        title = item.find_element_by_class_name('cr30').text
                        read_num = item.find_element_by_css_selector('.wxAti-info').find_element_by_tag_name('span').text
                        praise_num = (item.find_element_by_css_selector('.wxAti-info').find_elements_by_tag_name('span'))[-1].text
                        log(name, read_num, praise_num)
                        save_all = {
                            'url': url,
                            'read_num': read_num,
                            'praise_num': praise_num,
                            'title': title,
                            'public_url': self.driver.current_url,
                            'insert_time': datetime.datetime.now()
                        }
                        parsed_url = urllib.parse.quote(url)
                        # print(parsed_url)
                        upload_url = 'http://183.131.241.60:38011/InsetUrl?url={}&views={}&praises={}'.format(parsed_url, read_num, praise_num)
                        requests.get(upload_url)
                        cursor.execute(
                            "INSERT INTO wechat_qingbo(current_url, article_url, read_num, praise_num,  insert_time) VALUES (%s, %s,%s, %s,  %s)",
                            (self.driver.current_url, url, read_num, praise_num,  datetime.datetime.now()))
                        db.commit()
                        # cursor.execute("INSERT INTO wechat_qingbo VALUES (?, ?, ?)")
                        # urun['read_praise_num_details_temp'].insert(save_all)

                    self.driver.close()
                    for index, handles in enumerate(all_handles):
                        if index == 0:
                            self.driver.switch_to_window(handles)
            else:
                log('not found available public')
                return 'not found'

    def run(self):
        self.login_website()
        count = 0
        while True:
            try:
                log('request count {}'.format(count))
                self.name_list = self.get_public_name()
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
                        continue
                time.sleep(3)
                count += 1
            except Exception as e:
                log('error afsdfadfsd')
                if self.driver is not None:
                    log(self.driver.current_url)
                    # log(self.driver.page_source)
                    self.driver.quit()
                # 使用headless无界面浏览器模式
                # options = Options()
                # options.add_argument('--headless')
                # # options.add_argument('--disable-gpu')
                # self.driver = webdriver.Chrome(chrome_options=options)
                # self.driver = webdriver.PhantomJS()
                self.driver = webdriver.Chrome()
                self.login_website()
                count += 1
                continue
        print('haha')


if __name__ == '__main__':
    test = PublicDetails()
    test.run()
