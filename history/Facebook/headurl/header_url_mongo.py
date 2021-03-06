import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
from setting import test, log
import random

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'comm'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()
cursor.execute('select * FROM imagefail')
count = 0
urls = cursor.fetchmany(2707)
urls = cursor.fetchmany(1243)
while True:
    # if count < 2:
    #     count += 1
    #     continue
    urls = cursor.fetchmany(988)
    driver = webdriver.Chrome()
    for url_tuple in urls:
        numb, post_id, _ = url_tuple
        header_url_person = ''
        header_url_group = ''
        url = 'https://www.facebook.com/' + post_id
        driver.get(url)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'inputtext')))
            t = random.random() * 2
            time.sleep(t)
            try:
                header_url_person_div = driver.find_element_by_css_selector('.scaledImageFitWidth.img')
                header_url_person = header_url_person_div.get_attribute('src')
            except Exception as e:
                pass

            try:
                header_url_group_div = driver.find_element_by_css_selector('._4jhq.img')
                header_url_group = header_url_group_div.get_attribute('src')
            except Exception as e:
                pass

        except Exception as e:
            log(e)
            log('not find')

        try:
            header_url = header_url_person or header_url_group
            d = {
                'id': numb,
                'url': url,
                'header_url': header_url,
                'post_id': post_id,
            }

            test['img_header_url_10000'].insert(d)
            count += 1
            log('{} 已保存'.format(numb))
        except Exception as e:
            log(e)
            log("insert error")
