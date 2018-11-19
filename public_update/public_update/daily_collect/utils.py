# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sys
import uuid
from threading import Thread

import pymongo
import pymysql
import redis
from selenium import webdriver

from config import USE_PROXY


def get_log(name=''):
    # 日志配置
    # logging.basicConfig(filename=log_file_name, level=logger_level, format=logger_format)
    logger = logging.getLogger(name)
    # formatter = logging.Formatter("%(asctime)s %(filename)s
    # %(levelname)s line:%(lineno)d %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    log_formatter = '%(asctime)s,%(name)s,%(levelname)s,%(lineno)d,%(message)s'
    formatter = logging.Formatter(log_formatter)
    file_handle = logging.FileHandler('log_daily_collect.txt', encoding='utf-8')
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    # 输出到console
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.formatter = formatter
    logger.addHandler(console_handle)
    # 日志输出等级
    logger.level = logging.DEBUG
    return logger


# def get_log_info(name=''):
#     # 日志配置
#     # logging.basicConfig(filename=log_file_name, level=logger_level, format=logger_format)
#     logger = logging.getLogger(name)
#     # formatter = logging.Formatter("%(asctime)s %(filename)s
#     # %(levelname)s line:%(lineno)d %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
#     log_formatter = '%(asctime)s,%(name)s,%(levelname)s,%(lineno)d,%(message)s'
#     formatter = logging.Formatter(log_formatter)
#     file_handle = logging.FileHandler('log.txt', encoding='utf-8')
#     file_handle.setFormatter(formatter)
#     logger.addHandler(file_handle)
#     # 输出到console
#     console_handle = logging.StreamHandler(sys.stdout)
#     console_handle.formatter = formatter
#     logger.addHandler(console_handle)
#     # 日志输出等级
#     logger.level = logging.DEBUG
#     return logger.info


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def hash_md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode(encoding='utf-8'))
    return m.hexdigest()


def uploads_mysql(config_mysql, sql, _tuple):
    db = pymysql.connect(**config_mysql)
    cursor = db.cursor()
    cursor.execute(sql, _tuple)
    db.commit()
    cursor.close()
    db.close()


def redis_conn():
    s = redis.StrictRedis(host='192.168.1.162', db=8)
    return s


def mongo_conn():
    conn = pymongo.MongoClient('120.78.237.213', 27017)
    db = conn.WeChat
    return db


def get_captcha_path():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    image_dir = os.path.join(base_dir, 'images')
    captcha_name = 'captcha.png'
    captcha_path = os.path.join(image_dir, captcha_name)
    return captcha_path


def time_strftime():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now


def save_name():
    # 文件不存在就创建
    pwd = os.getcwd()
    file_name = os.path.join(pwd, 'save_name.txt')
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as f:
            pass

    with open('save_name.txt', 'r') as f1:
        name = f1.read()
        if name:
            return name
        elif len(name) == 0:
            name = uuid.uuid1()
    with open('save_name.txt', 'w') as f2:
        if name:
            f2.write(str(name))
            return name


def abuyun_proxy():
    if not USE_PROXY:
        return False
    # proxy_host = "http-dyn.abuyun.com"
    # proxy_port = "9020"
    # # 代理隧道验证信息
    # proxy_user = "H47MY63960OG8D8D"
    # proxy_pass = "DA3B03DDAEE0CDF7"
    proxy_host = "http-dyn.abuyun.com"
    proxy_port = "9020"
    proxy_user = "HW282117435R626D"
    proxy_pass = "73E6ADCC5C073EC4"
    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_user,
        "pass": proxy_pass,
    }
    proxies = {
        "http": proxy_meta,
        "https": proxy_meta,
    }
    return proxies


class GetDrver(object):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        # --no-sandbox 会导致 webdriver无法退出
        # chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)


get_driver = GetDrver()
# driver 每次导入都是同一个？
driver = get_driver.driver

if __name__ == '__main__':
    # log_test = get_log()
    # log_test.info(123)
    # path = get_captcha_path()
    # print(path)
    name = save_name()
    print(name, type(name))
