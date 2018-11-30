# -*- coding: utf-8 -*-
import requests


def main():
    body = {
    '__biz': "MjM5MTI2MTI0MA==",
    'mid': '2655142500',
    'sn': '77fbb51f69117d7b573e17928f1a26ce',
    'idx': '1',
    'is_only_read': 1,
        'is_need_ad':0,
    }
    headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'Cookie':'wxuin=2148728940; wap_sid2=COyAzIAIElxrRE9MLXl0eUdEMHNRWE8wWklmd3dFbjM0TExMM3FTa1NidFVEZUU1MXM5MWNDLVhqTjRZa2ttTEVkcW10dGI2NkthelRXZXZqLUQxSmVEN1UtUlp2Tk1EQUFBfjDCmaXeBTgMQAo='
    }
    url = 'http://mp.weixin.qq.com/mp/getappmsgext?uin=MjE0ODcyODk0MA==&key=bebb47fdf2f6904661a36e9c290ce1c501372fa9856394f53eb86fe27380063bd7b4cc65c46126e48f2c08ee231f5b935b664a52aea3f528300e4467587eef1dbee6548f3f33bc2149d55a8b2b7bb068'
    r = requests.get(url, data=body, headers=headers)
    print(r.text)

if __name__ == '__main__':
    main()
