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
    from log_test.logger import logger
    logger.info(12313)

if __name__ == '__main__':
    haha()
