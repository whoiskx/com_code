# -*- coding:utf-8 -*-

import logging
import os
from logging import Logger

from handler import DailyRotatingHandler

LOG_NOSET = logging.NOTSET
LOG_DEBUG = logging.DEBUG
LOG_INFO = logging.INFO
LOG_ERROR = logging.ERROR
LOG_WARNING = logging.WARNING
LOG_CRITICAL = logging.CRITICAL

# HOME_PATH = '/Users/dong'
HOME_PATH = os.path.expanduser("~")

LOG_FILE_NAME = 'pylog'
LOG_MAX_SIZE = 4 * 1024 * 1024 * 1024
LOG_ENCODING = 'utf-8'
LOG_FORMAT = '%(asctime)s,%(process)d,%(name)s,%(levelname)s,%(filename)s:%(lineno)d,%(message)s'
LOG_PATH = os.path.join(HOME_PATH, 'log', 'error')
OSS_LOG_PATH = os.path.join(HOME_PATH, 'log', "oss")
OSS_LOG_FORMAT = '%(asctime)s,%(message)s'

# global
Log_Level = LOG_DEBUG
add_console_handler_flag = False
add_loghub_handler_flag = True


class LogOptions(object):
    def __init__(self):
        self.path = LOG_PATH
        self.file_name = LOG_FILE_NAME
        self.level = LOG_DEBUG
        self.max_size = LOG_MAX_SIZE
        self.encoding = LOG_ENCODING
        self.fmt = LOG_FORMAT


class BaseLogger(Logger):
    def __init__(self, name, options=LogOptions()):
        super(BaseLogger, self).__init__(name, options.level)

        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        if not os.path.exists(OSS_LOG_PATH):
            os.makedirs(OSS_LOG_PATH)
        self.options = options

        # 添加文件handler
        self.addHandler(self._get_handler(options))

        # 控制台handler
        self._console_handler = None

        # loghub handler
        self._loghub_handler = None
        self.add_loghub_handler()

    def _get_handler(self, options):
        handler = DailyRotatingHandler(
            os.path.join(options.path, options.file_name),
            max_bytes=options.max_size,
            encoding=options.encoding)
        handler.setFormatter(logging.Formatter(options.fmt))
        return handler

    def set_name(self, name):
        self.name = name

    def add_console_handler(self):
        if self._console_handler is None:
            self._console_handler = self._create_console_handler(self.options)
            self.addHandler(self._console_handler)

    def add_loghub_handler(self):
        if self._loghub_handler is None:
            self._loghub_handler = self._create_loghub_handler()
            self.addHandler(self._loghub_handler)

    @staticmethod
    def _create_console_handler(options):
        # 控制台
        console = logging.StreamHandler()
        console.setLevel(options.level)
        formatter = logging.Formatter(options.fmt)
        console.setFormatter(formatter)
        return console

    @staticmethod
    def _create_loghub_handler():
        # loghub
        from handler import LogHubHandler
        loghub = LogHubHandler()
        return loghub


ErrorLogger = BaseLogger


class OssLogger(BaseLogger):
    def __init__(self, name):
        options = LogOptions()
        options.path = OSS_LOG_PATH
        options.level = LOG_INFO
        options.fmt = OSS_LOG_FORMAT
        super(OssLogger, self).__init__(name, options)


class LogManager(object):
    loggers = set()
    logger_name = {}


__log = ErrorLogger('comm.log')
LogManager.loggers.add(__log)
LogManager.logger_name['comm.log'] = __log
__oss = OssLogger('comm.oss')


# for compation with the old version
def get_logger(logger_name=None):
    if logger_name is None:
        return __log
    else:
        if logger_name not in LogManager.logger_name:
            logger = ErrorLogger(logger_name)
            logger.setLevel(Log_Level)
            if add_console_handler_flag:
                logger.add_console_handler()
            if add_loghub_handler_flag:
                logger.add_loghub_handler()
            LogManager.loggers.add(logger)
            LogManager.logger_name[logger_name] = logger
        return LogManager.logger_name[logger_name]


# for compation with the old version
def get_handler():
    return __log._get_handler()


def init_logger():
    """初始化全局日志配置"""
    logger_format = LOG_FORMAT
    logger_level = logging.DEBUG

    log_file_name = os.path.join(LOG_PATH, "logger.log")
    logging.basicConfig(filename=log_file_name, level=logger_level, format=logger_format)

    # 控制台
    # console = logging.StreamHandler()
    # console.setLevel(logger_level)
    # formatter = logging.Formatter(logger_format)
    # console.setFormatter(formatter)
    #
    # # 将定义好的console日志handler添加到root logger
    # logging.getLogger('').addHandler(console)


def set_level(level):
    global Log_Level
    Log_Level = level
    for logger in LogManager.loggers:
        logger.setLevel(level)


set_name = __log.set_name


def add_console_handler():
    global add_console_handler_flag
    add_console_handler_flag = True
    for logger in LogManager.loggers:
        logger.add_console_handler()


def add_loghub_handler():
    global add_loghub_handler_flag
    add_loghub_handler_flag = True
    for logger in LogManager.loggers:
        logger.add_loghub_handler()


debug = __log.debug
info = __log.info
warning = __log.warning
error = __log.error
critical = __log.critical
oss = __oss.info
