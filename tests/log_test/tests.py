# -*- coding: utf-8 -*-
# import logger
# from logger import logger as ll
# # logger.info(__name__)
# # print(__name__)
# ll.critical(__name__, 1211323)
import logging
import sys


def haha():
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    # formatter = logging.Formatter("%(asctime)s_%(name)s_%(levelname)s_%(message)s")
    # file_handle = logging.FileHandler('testtttt.txt')
    # file_handle.setFormatter(formatter)
    # logger.addHandler(file_handle)
    #
    # console_handle = logging.StreamHandler(sys.stdout)
    # console_handle.formatter = formatter
    # logger.addHandler(console_handle)
    # logger.critical('123')
    from log_test.logger import get_log
    log = get_log('afasf')
    log.debug('this is debug')
    log.info(12313)
    log.error(123)
    log.info('张伟使得公司高管搜狗广东分公司法国岁的法国')


if __name__ == '__main__':
    haha()
