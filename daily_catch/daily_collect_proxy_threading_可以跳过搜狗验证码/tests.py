# -*- coding: utf-8 -*-
# import logger
# from logger import logger as ll
# # logger.info(__name__)
# # print(__name__)
# ll.critical(__name__, 1211323)
import datetime
import json
import logging
import os
import time
import requests


def main():
    # logger = logging.getLogger(main.__name__)
    # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # file_handle = logging.FileHandler('testtttt')
    # file_handle.setFormatter(formatter)
    # logger.addHandler(file_handle)
    # logger.critical('123')
    # current_dir = os.getcwd()
    # if not os.path.exists(os.path.join(current_dir, 'xml')):
    #     os.mkdir('xml')
    global s
    s += 1
    print(s)

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
if __name__ == '__main__':
    # from selenium import webdriver
    #
    # chrome_options = webdriver.ChromeOptions()
    # # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    #
    # driver2 = webdriver.Chrome(chrome_options=chrome_options)
    # s = 1
    # main()
    # print(s)
    # from utils import driver
    # driver1 = driver
    # driver2 = driver
    # print( driver1 is driver2)
    # time.sleep(5)
    # 代理
    # account_link = 'http://httpbin.org/ip'
    # proxies = {
    #     'https': "http://localhost:1080",
    #     'http': 'http://127.0.0.1:1080'
    #
    # }
    # homepage = requests.get(account_link, proxies=proxies)
    # print(homepage.status_code)
    # print(homepage.text)
    # from utils import driver, GetDrver
    # driver.get('https://www.baidu.com/')
    # time.sleep(1)
    # driver.quit()
    # time.sleep(1)
    # driver = GetDrver().driver
    # driver.get('https://www.baidu.com/')
    # driver.quit()
    # print('end')
    # driver2 = GetDrver().driver
    # driver2.get('https://www.baidu.com/')
    # print(driver is driver2)
    # coding = utf-8
    # from selenium import webdriver
    # import time
    #
    # browser = webdriver.Firefox()
    #
    # browser.get("http://www.baidu.com")
    # time.sleep(0.3)  # sleep 0.3s
    # browser.find_element_by_id("kw").send_keys("selenium")
    # browser.find_element_by_id("su").click()
    # time.sleep(3)  # sleep 3s
    # browser.quit()

    print(dedup('gh_1c5f79a695d1'))