# -*- coding: utf-8 -*-
# import logger
# from logger import logger as ll
# # logger.info(__name__)
# # print(__name__)
# ll.critical(__name__, 1211323)
import logging
import os


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
    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.close()
