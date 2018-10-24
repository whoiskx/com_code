# -*- coding: utf-8 -*-
import logging

class T(object):
    def __init__(self):
        self.name = 123

    def run(self):
        logging.warning('error')

def main():
    # logging.warning('123')
    import logging

    # 通过下面的方式进行简单配置输出方式与日志级别
    logging.basicConfig(level=logging.ERROR)

    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warn message')
    logging.error('error message')
    logging.critical('critical message')

if __name__ == '__main__':
    main()
    t = T()
    t.run()