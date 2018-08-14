from random import randint
import pymongo
import pymysql
from selenium import webdriver
import time


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


email = "live41@163.com"
password = "cs-123456"

# email = '574613576@qq.com'
# password = 'jh123258456'



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
                'images': 2,  # 禁止图片
            }
    }
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)

    # driver = webdriver.Firefox()
    driver.implicitly_wait(120)

    driver.get("https://www.facebook.com/")
    email_text = driver.find_element_by_id("email")
    password_text = driver.find_element_by_id('pass')
    email_text.send_keys(email)
    password_text.send_keys(password)
    button = driver.find_element_by_id('loginbutton')
    button.click()
    return driver


def driver_chrome():
    driver = webdriver.Chrome()
    return driver


def execute_times(driver, times=1):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(randint(2, 4))

        print('下拉第{}次，总共下拉{}次'.format(i + 1, times))
        save_number = [10, 200, 250, 280, 300, 350, 400, 440, 480, 550, 600, 700, 800, 900, 1100, 1200, 1500]
        if i in save_number:
            time.sleep(10)
            print('begin')
            x = input(">....")
            if x == 'skip':
                continue
            posts_html = driver.page_source
            print('end')
            time.sleep(20)
            with open("posts_index22_{}.html".format(i), "w", encoding='utf-8') as f:
                f.write(posts_html)
            log('posts_html_22_{}写入文件夹'.format(i))
            time.sleep(15)

def hash_md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode(encoding='utf-8'))
    return m.hexdigest()

# pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
test = conn.test
# db['uu'].insert({'name':"李白", "age":"30", "skill":"Python"})

MYSQL_HOST = 'localhost'

MYSQL_PORT = 3306
MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'Yunrun2015!@#'
MYSQL_DATABASE = 'comm'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
    # 'passwd': MYSQL_PASSWORD
    'charset': 'utf8',
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()

print(1)
