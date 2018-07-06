from random import randint
import pymongo
from selenium import webdriver
import time
from setting import email, password


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def time_sleep():
    time.sleep(3)


# 启动driver
def driver_facebook():
    # 使用headless无界面浏览器模式
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2,
                # 'images': 2,
            }
    }
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)

    # driver = webdriver.Firefox()
    driver.implicitly_wait(60)

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
        time.sleep(randint(2, 4))

        print('下拉第{}次，总共下拉{}次'.format(i + 1, times))
        save_number = [10, 200, 250, 280, 300, 350]
        if i in save_number:
            print('begin')
            x = input(">....")
            if x == 'skip':
                continue
            posts_html = driver.page_source
            print('end')
            time.sleep(10)
            name = driver.title
            with open("{}_index_{}.html".format(name, i), "w", encoding='utf-8') as f:
                f.write(posts_html)
            log('{}_html__{}写入文件夹'.format(name, i))
            time.sleep(10)


# pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
test = conn.test
