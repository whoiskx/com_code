#encoding=utf-8
import time


i = 1
with open("log.txt", 'a') as f:
    value = time.strftime("%M:%S", time.localtime())
    print("time:{} count: {} 哈哈".format(value, i), file=f)