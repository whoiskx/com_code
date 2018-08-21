# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.get('https://www.baidu.com/')
# driver.quit()
# driver.quit()
# driver.quit()
#
# print(driver)
# print(0)


# try:
#     raise RuntimeError
# except Exception as e:
#     print(e)
import os
import time

file_name = 'tlog.txt'
print(os.path.getsize(file_name))

while True:
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    # if '11:55:01' in dt:
    with open('tlog.txt', 'w', encoding='utf-8') as f:
        f.truncate()
            # print('start')
            # time.sleep(10)
            # print('end')
# with open('tlog.txt', 'a+', encoding='utf-8') as f:
#     print(len(f.read()))