# -*- coding: utf-8 -*-

import os

read_ver_url = 'http://dispatch.yunrunyuqing.com:38082/resources/sourceVersion/weixin/version.txt'
download_url = 'http://dispatch.yunrunyuqing.com:38082/resources/sourceVersion/weixin/public_update.zip'

base_path = os.path.dirname(os.path.abspath(__file__))
core_spider_path = os.path.join(base_path, 'public_update')
core_zip_path = os.path.join(core_spider_path, 'public_update.zip')
version_txt_path = os.path.join(core_spider_path, 'version.txt')

spider_path = os.path.join(core_spider_path, 'daily_collect')
run_path = os.path.join(spider_path, 'daily_collect.py')

kill_path = 'daily_collect.py'
