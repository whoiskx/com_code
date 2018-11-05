# -*- coding: utf-8 -*-
import logging
import sys
from threading import Thread

import pymongo
import pymysql
import redis


def get_log(name=''):
    # 日志配置
    # logging.basicConfig(filename=log_file_name, level=logger_level, format=logger_format)
    logger = logging.getLogger(name)
    # formatter = logging.Formatter("%(asctime)s %(filename)s
    # %(levelname)s line:%(lineno)d %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    log_formatter = '%(asctime)s,%(name)s,%(levelname)s,%(lineno)d,%(message)s'
    formatter = logging.Formatter(log_formatter)
    file_handle = logging.FileHandler('log.txt', encoding='utf-8')
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    # 输出到console
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.formatter = formatter
    logger.addHandler(console_handle)
    # 日志输出等级
    logger.level = logging.DEBUG
    return logger


def get_log_info(name=''):
    # 日志配置
    # logging.basicConfig(filename=log_file_name, level=logger_level, format=logger_format)
    logger = logging.getLogger(name)
    # formatter = logging.Formatter("%(asctime)s %(filename)s
    # %(levelname)s line:%(lineno)d %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    log_formatter = '%(asctime)s,%(name)s,%(levelname)s,%(lineno)d,%(message)s'
    formatter = logging.Formatter(log_formatter)
    file_handle = logging.FileHandler('log.txt', encoding='utf-8')
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    # 输出到console
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.formatter = formatter
    logger.addHandler(console_handle)
    # 日志输出等级
    logger.level = logging.DEBUG
    return logger


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


if __name__ == '__main__':
    log_test = get_log()
    log_test.info('test')