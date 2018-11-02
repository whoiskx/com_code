# -*- coding: utf-8 -*-
import datetime
import time
from threading import Thread

import pymysql
import redis


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


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


def time_strftime():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now


if __name__ == '__main__':
    test = time_strftime()
    print(test)

