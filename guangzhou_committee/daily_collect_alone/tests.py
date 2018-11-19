# -*- coding: utf-8 -*-
# import logger
# from logger import logger as ll
# # logger.info(__name__)
# # print(__name__)
# ll.critical(__name__, 1211323)
import logging
import os
import time
import requests
import json


def main():
    # logger = logging.getLogger(main.__name__)
    # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # file_handle = logging.FileHandler('testtttt')
    # file_handle.setFormatter(formatter)
    # logger.addHandler(file_handle)
    # logger.critical('123')
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, 'xml')):
        os.mkdir('xml')


if __name__ == '__main__':
    try:
        url = 'http://10.194.12.106:8002/GetWeixinTask?name=&name_array=&Name_word=&channel=&pageno=1&pagesize=12&local=False&token=082c5e82-a168-4c2e-a8e6-00760225c93a_wechat&page=1&rows=12&sort='
        resp = requests.get(url, timeout=30)
        data = json.loads(resp.text).get('weixin')
        account_list = []
        for account_info in data:
            account_list.append(account_info.get('account'))
        print(account_list)
    except Exception as e:
        print(e)
