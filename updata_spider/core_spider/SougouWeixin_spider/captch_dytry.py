# -*- coding: utf-8 -*-
import hashlib
import requests
import datetime
from config import *


# 识别验证码
def captch_upload_image(filebytes):
    """
    :param filebytes: 待识别图像的二进制数据
    :return: 验证码识别后的字符串
    """

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

