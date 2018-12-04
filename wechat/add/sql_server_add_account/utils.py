# -*- coding: utf-8 -*-
import datetime
import hashlib
import logging
import os
import sys
import time
from threading import Thread

import pymysql
import requests


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a+', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

    # logger = logging.getLogger(name)
    # # formatter = logging.Formatter("%(asctime)s %(filename)s
    # # %(levelname)s line:%(lineno)d %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    # log_formatter = '%(asctime)s,%(name)s,%(levelname)s,%(lineno)d,%(message)s'
    # formatter = logging.Formatter(log_formatter)
    # file_handle = logging.FileHandler('log.txt', encoding='utf-8')
    # file_handle.setFormatter(formatter)
    # logger.addHandler(file_handle)
    # # 输出到console
    # console_handle = logging.StreamHandler(sys.stdout)
    # console_handle.formatter = formatter
    # logger.addHandler(console_handle)
    # # 日志输出等级
    # logger.level = logging.DEBUG
    # return logger


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


# 识别验证码
def captch_upload_image(filebytes):
    """
    :param filebytes: 待识别图像的二进制数据
    :return: 验证码识别后的字符串
    """

    # 打码平台参数配置
    # 接口URL
    DYTRY_APIURL = 'http://api.dytry.com/ocr.json'
    # 用户名
    DYTRY_USERNAME = 'uruntest'
    # 用户密码
    DYTRY_PASSWORD = '0763!@#'
    # 题目类型
    DYTRY_TYPEID = 9999
    # 软件ID
    DYTRY_SOFTID = 1107
    # 软件KEY
    DYTRY_SOFTKEY = '34af19d2ee35e938dbbdc0336eb730cb'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, 'images')
    CAPTCHA_NAME = 'captcha.png'

    paramKeys = ['username', 'password', 'typeid', 'softid', 'softkey']
    paramDict = {
        "username": DYTRY_USERNAME,
        "password": DYTRY_PASSWORD,
        "typeid": DYTRY_TYPEID,
        "softid": DYTRY_SOFTID,
        "softkey": DYTRY_SOFTKEY,
    }

    timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')
    boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
    boundarystr = '\r\n--%s\r\n' % (boundary)

    bs = b''
    for key in paramKeys:
        bs = bs + boundarystr.encode('ascii')
        param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
        # print param
        bs = bs + param.encode('utf8')
    bs = bs + boundarystr.encode('ascii')

    header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/jpeg\r\n\r\n' % (
        'sample')
    bs = bs + header.encode('utf8')

    bs = bs + filebytes
    tailer = '\r\n--%s--\r\n' % (boundary)
    bs = bs + tailer.encode('ascii')

    headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
               'Connection': 'Keep-Alive',
               'Expect': '100-continue',
               }
    response = requests.post(url=DYTRY_APIURL, params='', data=bs, headers=headers)
    requests.utils.dict_from_cookiejar(response.cookies)
    captch_input = response.json().get('Result')
    return captch_input

if __name__ == '__main__':
    log().info(123)