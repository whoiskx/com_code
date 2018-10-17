# -*- coding: utf-8 -*-
import time


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    # if '12:49:4' or '12:49:5' in dt:
    #     with open('log.txt', 'w', encoding='utf-8') as f:
    #         f.truncate()
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
def main():
    for i in range(10):
        log(1)
        time.sleep(1)


if __name__ == '__main__':
    main()
