# # -*- coding: utf-8 -*-
# 
# import logging
# import sys
# 
# # 获取logger实例，如果参数为空则返回root logger
# from time import time, asctime
# 
# logger = logging.getLogger()
# 
# # 指定logger输出格式
# formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
# 
# # 文件日志
# file_handler = logging.FileHandler("test.log",)
# file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
# 
# # 控制台日志
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.formatter = formatter  # 也可以直接给formatter赋值
# 
# # 为logger添加的日志处理器
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
# 
# # 指定日志的最低输出级别，默认为WARN级别
# logger.setLevel(logging.INFO)
# 
# # 输出不同级别的log
# logger.debug('this is debug info')
# logger.info('this is information')
# logger.warn('this is warning message')
# logger.error('this is error message')
# logger.fatal('this is fatal message, it is same as logger.critical')
# logger.critical('this is critical message')
# 
# # 2016-10-08 21:59:19,493 INFO    : this is information
# # 2016-10-08 21:59:19,493 WARNING : this is warning message
# # 2016-10-08 21:59:19,493 ERROR   : this is error message
# # 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
# # 2016-10-08 21:59:19,493 CRITICAL: this is critical message
# 
# # 移除一些日志处理器
# logger.removeHandler(file_handler)
# 
# # 记录异常信息
# print((asctime()))
# try:
#     1 / 0
# except Exception as e:
#     # 等同于error级别，但是会额外记录当前抛出的异常堆栈信息
#     logger.exception('this is an exception message')
# # 1 / 0
# print((asctime))
# 
# print(123)
# print(123)
# print(123)
# print(123)
# print(__name__)
import logging
import sys

LOG_FORMAT = '%(asctime)s,%(name)s,%(levelname)s,%(filename)s:%(lineno)d,%(message)s'


def get_log(name=''):
    # 日志配置
    # logging.basicConfig(filename=log_file_name, level=logger_level, format=logger_format)
    logger = logging.getLogger(name)
    # formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s line:%(lineno)d %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    formatter = logging.Formatter(LOG_FORMAT)
    file_handle = logging.FileHandler('log.txt', encoding='utf-8')
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    # 输出到console
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.formatter = formatter
    logger.addHandler(console_handle)
    # 日志输出等级
    logger.level = logging.DEBUG
    return logger


def test():
    log = get_log('abc')
    log.info('this is debug %s', 123)
    log.info('中文')


if __name__ == '__main__':
    test()
# log = get_log()
