import logging

from .logger import get_handler, get_logger, \
    LOG_NOSET, LOG_DEBUG, LOG_INFO, \
    LOG_ERROR, LOG_WARNING, LOG_CRITICAL, \
    set_name, set_level, add_console_handler, \
    add_loghub_handler, debug, info, warning, \
    error, critical, oss, init_logger

logging.getLogger = get_logger
