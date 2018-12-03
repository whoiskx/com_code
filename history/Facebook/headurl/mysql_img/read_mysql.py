import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import requests
from setting import test, log
# MYSQL_HOST = 'localhost'

MYSQL_HOST = '47.52.190.138'
MYSQL_PORT = 8002
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'Yunrun2015!@#'
MYSQL_DATABASE = 'weibotask'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
	'passwd': MYSQL_PASSWORD,
    'db': MYSQL_DATABASE,
}

header_img = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()
cursor_save = db.cursor()

cursor.execute('select * FROM imagefail_header_url')
count = 0
urls = cursor.fetchmany(5776)
urls = cursor.fetchmany(2000)
proxies = {"https": "http://localhost:1080", }

for index, url_tuple in enumerate(urls):
    numb, post_id, site, url = url_tuple
    id = post_id
    try:
        if not url:
            continue
        print(url)
        resp = requests.get(url, proxies=proxies)
        with open('img_header/{}.png'.format(post_id), 'wb') as f:
            f.write(resp.content)
        test['save_img_mysql'].insert({'id':numb, 'header_url': url, 'blogger_id': id})
        # print('save {}'.format(id))
        log('第{}次 save {} {}'.format(index, numb, id))
    except Exception as e:
        log(e)
        log('=============')
        log(index, post_id)
