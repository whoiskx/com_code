import time

import pymongo
from selenium import webdriver

"""live41@163.com
cs-123456
"""
def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('gua.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

email = "live41@163.com"
password = "cs-123456"

email_urun = '18390553540@163.com'
password_urun = 'jh123258456'
# 启动driver
def driver_facebook():
    driver = webdriver.Chrome()
    driver.get("https://www.facebook.com/")

    email = driver.find_element_by_id("email")
    email.send_keys("live41@163.com")
    # email.send_keys("18390553540@163.com")
    # email.send_keys("574613576@qq.com")
    password = driver.find_element_by_id('pass')
    password.send_keys("cs-123456")
    # password.send_keys("jh123258456")
    button = driver.find_element_by_id('loginbutton')
    button.click()
    return driver


# pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
# db['uu'].insert({'name':"李白", "age":"30", "skill":"Python"})