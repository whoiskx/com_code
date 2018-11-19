# -*- coding: utf-8 -*-

"""
    logging日志
"""

import logging


LOG_FILE = 'log.log'

# 实例化handler
handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
fmt = '%(asctime)s - %(levelname)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)     # 为handler添加formatter

logger = logging.getLogger('log')   # 获取名为log的logger
logger.addHandler(handler)          # 为logger添加handler
logger.setLevel(logging.DEBUG)      # 从DEBUG级开始输出日志
