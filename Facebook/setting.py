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


# email = "live41@163.com"
# password = "cs-123456"


email = '574613576@qq.com'
password = 'jh123258456'


# 启动driver
def driver_facebook():
    # 使用headless无界面浏览器模式
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    # prefs = {
    #     'profile.default_content_setting_values':
    #         {
    #             'notifications': 2
    #         }
    # }
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome(chrome_options=options)
    #
    driver = webdriver.Firefox()
    driver.implicitly_wait(120)

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
        # driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(randint(3, 5))
        print('下拉第{}次，总共下拉{}次'.format(i + 1, times))
        save_number = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
             1945]
        if i in save_number:
            posts_html = driver.page_source
            with open("posts_index_{}.html".format(i), "w", encoding='utf-8') as f:
                f.write(posts_html)
            log('posts_html {}写入文件夹'.format(i))


# pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
# db['uu'].insert({'name':"李白", "age":"30", "skill":"Python"})
