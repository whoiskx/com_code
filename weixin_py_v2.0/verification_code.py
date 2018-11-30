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

# url = 'https://mp.weixin.qq.com/profile?src=3&timestamp=1536203019&ver=1&signature=NHsz0BdTJaHizbwPPaEODtFV*unABNSLtg*PGevDLZ4dk6dzGAcREd9LbWW3pKjIwCc9Oq8evkihia9XfLP6Xg=='
# headers = {
#     'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; pgv_pvi=7068666880; o_cookie=574613576; pac_uid=1_574613576; tvfe_boss_uuid=19cb1313d3f0ac88; pt2gguin=o0574613576; rewardsn=; wxtokenkey=777; lang=zh_CN; mm_lang=zh_CN; pgv_si=s5298735104; pass_ticket=QukIbv2L+F2U/CZzd3v66/OC4csWnrugWhRMuAyKIGcDjBInCr9SlHiYMfXP9kCL; wap_sid2=CIjwqPwDElxEYmJQYlhjVGVISmxnQWtxUnJWdVBub1d0cFM5NmVRZ1lsUDhLSkpuMnk0OEtmZXNOYjhYUWFwU1FLZWNoZWpvU3dTQzNSZ2RaZVhjanpuMU95UEQyTTBEQUFBfjDposLcBTgMQJRO; wxuin=1156918861; devicetype=android-26; version=26070239; sig=h01e8b30d7bc56542d36f53ce1220c7917d86f0ef07de9675429fe403ef26a9c9c6861d73e3ad587219'
# }
# headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Connection': 'keep-alive',
#             'Host': 'weixin.sogou.com',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
#         }
url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1543301987&ver=1&signature=4H10EL-xVi2yDSeBzcMIJYbo4FzJtNHCYVJqvJoQ9hZJdsDI9CO3*Ef8Fs1q*6E742vtLIEqZtQJVImRUueIaw=='
s = requests.Session()
print('------开始处理微信验证码------')
cert = random.random()
image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
respones = s.get(image_url, )
captch_input = captch_upload_image(respones.content)
print('------验证码：{}------'.format(captch_input))
data = {
    'cert': cert,
    'input': captch_input
}
respones = s.post(image_url, data=data)
cookies = requests.utils.dict_from_cookiejar(respones.cookies)
print('微信cookies:', cookies)
print('------cookies已更新------')
print(respones.status_code)
cc = respones.cookies
d = {}
for c in cc:
    print(c.name, c.value)
    d[c.name] = c.value

print(d)
print('e')
resp = s.get(image_url, )
print(resp.text)
# print('respones.cookies', respones.cookies)
# print('------cookies已更新------')

