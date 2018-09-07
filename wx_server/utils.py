# -*- coding: utf-8 -*-
import time

import pymongo
import pymysql

conn = pymongo.MongoClient('120.78.237.213', 27017)
db = conn.WeChat


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


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