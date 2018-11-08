# -*- coding: utf-8 -*-
import os
import time

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def log2(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log_record.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def log3(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log_error_file.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def main():
    home_path = 'D:\WXSchedule\Images'
    all_img_dir = os.listdir(home_path)

    big_size_count = 0
    open_error = 0
    for index, img_dir in enumerate(all_img_dir):
        log('index:{}'.format(index))
        log(len(img_dir))
        log('Path:{}'.format(img_dir))
        file_path = os.path.join(home_path, img_dir)
        # print(file_path)
        all_img_file = os.listdir(file_path)
        # print(all_img_file)
        if all_img_file:
            for path in all_img_file:
                really_path = os.path.join(file_path, path)

                # path = os.path.join(os.getcwd(), "115339132.jpg")
                try:
                    img = Image.open(really_path)
                except OSError as e:
                    log('path, error {}'.format(e))
                    open_error += 1
                    # todo 删除再添加
                    os.remove(really_path)
                    log3('错误文件|{}'.format(path))
                    continue
                if img.size > (91, 91):
                    big_size_count += 1
                    log(img.size, path)
                    size = 90
                    img.resize((size, size), Image.ANTIALIAS).save(really_path)
                    log2('替换完成|{}'.format(path))
                # print(img.format, )
                # print(img.size)
                # size = 90
                # img.resize((size, size), Image.ANTIALIAS).save("icom_%d.png" % (size))
    log('big_size_count:{}'.format(big_size_count))
    log('open_error:{}'.format(open_error))


if __name__ == '__main__':
    main()
