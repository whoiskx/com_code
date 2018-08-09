import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo

conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    # print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
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
            # print(name)
            name_list.append(name)
        # print(name_list)
        return name_list

    def login_website(self):
        if self.driver is None:
            # 使用headless无界面浏览器模式
            # options = Options()
            # options.add_argument('--headless')
            # # options.add_argument('--disable-gpu')
            # self.driver = webdriver.Chrome(chrome_options=options)
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

    def get_numb(self, name):
        search_input = self.driver.find_element_by_xpath('//*[@id="search_input"]')
        # search_input.send_keys('富翁俱乐部 ')
        search_input.clear()
        search_input.send_keys(name)
        search_button = self.driver.find_element_by_class_name('search_wx')
        search_button.click()
        time.sleep(2.5)

        gxh = self.driver.find_element_by_xpath('//*[@id="nickname"]')
        gxh.click()
        time.sleep(2)
        all_handles = self.driver.window_handles  # 获取到当前所有的句柄,所有的句柄存放在列表当中
        # print(all_handles)
        '''获取非最初打开页面的句柄'''
        for index, handles in enumerate(all_handles):
            if index == 1:
                self.driver.switch_to_window(handles)
        time.sleep(2)
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)

        # html = self.driver.page_source
        # print(html)

        data_all = self.driver.find_elements_by_css_selector('.wxDetail.bgff')
        datas = data_all[-1]
        items = datas.find_elements_by_class_name('clearfix')
        for count, item in enumerate(items):
            if count == 0:
                continue
            url = item.find_element_by_tag_name('a').get_attribute('href')
            read_num = item.find_element_by_css_selector('.wxAti-info').find_element_by_tag_name('span').text
            praise_num = (item.find_element_by_css_selector('.wxAti-info').find_elements_by_tag_name('span'))[-1].text
            # print(url, read_num, praise_num)


            save_all = {
                'url': url,
                'read_num': read_num,
                'praise_num': praise_num,
                'name': name,
                'public_url': self.driver.current_url,
                'insert_time': time.strftime('%m-%d %H:%M', time.localtime(int(time.time())))
            }
            urun['read_praise_num_details'].insert(save_all)

        self.driver.close()
        for index, handles in enumerate(all_handles):
            if index == 0:
                self.driver.switch_to_window(handles)

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
                        self.get_numb(name)
                    except Exception as e:
                        log(e)
                        continue
                time.sleep(5)
                count += 1
            except Exception as e:
                log('error afsdfadfsd')
                if self.driver is not None:
                    log(self.driver.current_url)
                    log(self.driver.page_source)
                    self.driver.quit()
                # 使用headless无界面浏览器模式
                # options = Options()
                # options.add_argument('--headless')
                # # options.add_argument('--disable-gpu')
                # self.driver = webdriver.Chrome(chrome_options=options)
                self.driver = webdriver.Chrome()
                self.login_website()
                continue
        print('haha')


if __name__ == '__main__':
    test = PublicDetails()
    test.run()
