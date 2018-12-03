from random import randint
import pymongo
from selenium import webdriver
import time


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


email = "live41@163.com"
password = "cs-123456"
# email = '18390553540@163.com'
# password_urun = 'jh123258456'


# 启动driver
def driver_facebook():
    driver = webdriver.Chrome()
    driver.get("https://www.facebook.com/")
    email_text = driver.find_element_by_id("email")
    password_text = driver.find_element_by_id('pass')
    email_text.send_keys(email)
    password_text.send_keys(password)
    button = driver.find_element_by_id('loginbutton')
    button.click()
    return driver


def execute_times(driver, times=1):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(randint(1, 3))
        print('下拉第{}次，总共下拉{}次'.format(i + 1, times))


# pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
# db['uu'].insert({'name':"李白", "age":"30", "skill":"Python"})
