# -*- coding: utf-8 -*-
# import logger
# from logger import logger as ll
# # logger.info(__name__)
# # print(__name__)
# ll.critical(__name__, 1211323)
import logging


def main():
    logger = logging.getLogger(main.__name__)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handle = logging.FileHandler('testtttt')
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    logger.critical('123')


if __name__ == '__main__':
    main()
