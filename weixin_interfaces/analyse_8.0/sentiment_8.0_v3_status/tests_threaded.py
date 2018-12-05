# -*- coding: utf-8 -*-
import json
import random
import time

import requests
from utils import async


# x = 1
#
# @async
# def send(count):
#     url = 'http://localhost:38017/{}/{}'.format(random.randint(0, 9), random.randint(0, 9))
#     print(count, url)
#     r = requests.get(url)
#     print(count, r.text)
#     global x
#     x = count
#     time.sleep(3)
#     print(count, x)
#
#
# def main():
#     count = 0
#     while True:
#         send(count)
#         count += 1
#         time.sleep(0.5)
class Account(object):
    def __init__(self, _account):
        self.name = _account


account_exp = Account('start')


@async
def send(count, account):
    url = 'http://localhost:10004/WeiXinArt/WeiXinAdvanceParse?account={}'.format(account)
    print(count, account, url)
    r = requests.get(url)
    print(count, account, r.status_code)
    # global x
    # x = count
    account = account_exp.name
    time.sleep(3)
    print(count, account, json.loads(r.text).get('Account'))


def main():
    count = 0
    accounts = ['guoanjia-dy', 'znszyhr', 'guoandyc', 'gh_26040b2fdc88', 'gh_7183a2274633', 'guoangz', 'zxyh0451',
                'gh_f4b900d6dc98', 'citicbank_ty', 'gh_598245057b5e', 'Citic_Engineering', 'CITICAMC001', 'guoanyizun',
                'guoango', 'guoansport', 'citic-mmi', 'gyguoanshequ']
    # accounts = ['gh_598245057b5e0', 'guoanyizun', 'gyguoanshequ', 'gh_26040b2fdc88', 'gh_f4b900d6dc98', 'citic-mmi']
    while True:
        send(count, accounts[count])
        count += 1
        time.sleep(0.5)


if __name__ == '__main__':
    main()
