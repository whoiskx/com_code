# -*- coding: utf-8 -*-
import hashlib
import random
import re

import requests
import datetime

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

url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1536113209&ver=1&signature=HsNYMYa2L5cZcVHzJPWjpzwqd1S6Uh0ATodp-fz7bGSuLtCft8DYPb0fJSG-yDKIPgAuJxk6XO2s4uMTX*V8WQ=='

headers = {
    'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; SNUID=22DB3E2F151060E72907EDED151C0C72; sct=147'
}
r = requests.get(url, headers=headers)
print('------开始处理微信验证码------')
print('微信验证码URL:', url)
cert = random.random()
s = requests
image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
respones1 = s.get(image_url)
with open('code1.txt', 'w', encoding='utf-8') as f:
    f.write(respones1.text)
captch_input = captch_upload_image(respones1.content)
print('------验证码：{}------'.format(captch_input))
data = {
    'cert': cert,
    'input': captch_input
}
respones = s.post(image_url, headers=headers, data=data)
print(respones.status_code)
print(respones.cookies)
print('e')
# print('respones.cookies', respones.cookies)
# print('------cookies已更新------')

