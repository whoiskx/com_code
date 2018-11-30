# -*- coding: utf-8 -*-

"""
更新程序
"""
import time
import logging
import zipfile
import requests
from config import *


class UpdateVersion(object):
    def __init__(self):
        """logging日志"""
        LOG_FILE = 'log.log'
        handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')  # 实例化handler
        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)  # 实例化formatter
        handler.setFormatter(formatter)  # 为handler添加formatter
        self.logger = logging.getLogger('log')  # 获取名为log的logger
        self.logger.addHandler(handler)  # 为logger添加handler
        self.logger.setLevel(logging.DEBUG)  # 从DEBUG级开始输出日志

    # 主程序入口
    def judge_update(self):
        # 判断版本
        server_v = requests.get(read_ver_url)
        server_v = server_v.text
        server_v = float(server_v)
        with open(version_txt_path, 'r') as f:
            locate_v = f.read()
        locate_v = float(locate_v)

        # 如果服务器版本号 > 本地版本号：
        if server_v > locate_v:
            self.logger.info("---发现服务器有新版本---")

            # 杀死旧程序
            self.kill_old_ver()

            # 下载新程序
            self.download_zip()

            # 解压zip文件
            self.decompression()

            # 开启采集器
            self.run_collector()

        else:
            self.logger.info('---没有新版本---')

    # 杀死旧程序
    def kill_old_ver(self):
        kill_chromium = ('pkill -f chromium-browse')
        kill_chromium = os.system(kill_chromium)
        if kill_chromium == 15:
            self.logger.info('----chromium-browse进程已杀死----')

        kill_chromedriver = ('pkill -f chromedriver')
        kill_chromedriver = os.system(kill_chromedriver)
        if kill_chromedriver == 15:
            self.logger.info('----chromedriver进程已杀死----')

        kill_py = ('pkill -f {}'.format(kill_path))
        kill_py = os.system(kill_py)
        if kill_py == 15:
            self.logger.info('---程序已成功停止：{}---'.format(kill_py))

    # 下载新程序
    def download_zip(self):
        self.logger.info("----正在开始下载新版本----")
        response = requests.get(download_url)
        with open(core_zip_path, "wb") as code:
            code.write(response.content)
        self.logger.info('----下载新版本完毕----')

    # 解压压缩包
    def decompression(self):
        zip_file = zipfile.ZipFile(core_zip_path, 'r')
        zip_file.extractall(path='{}'.format(core_spider_path))  # 解压到路径(path=r"")
        zip_file.close()
        self.logger.info('---解压文件完毕---')

    # 开启采集器
    def run_collector(self):
        self.logger.info('---正在开启采集器---')
        run_py = ('nohup python3 {} &'.format(run_path))
        run_result = os.system(run_py)
        if run_result != 0:
            self.logger.info('---程序执行失败：{}---'.format(run_result))


if __name__ == '__main__':
    upver = UpdateVersion()
    while True:
        try:
            upver.judge_update()
            time.sleep(300)  # 休眠5分钟
        except Exception as e:
            print(e)
            print('自动更新程序失败...重试')
            time.sleep(1)
