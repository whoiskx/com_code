# i = 0
#
# def generater():
#     global i
#     i += 1
#     yield i
#
# def foo():
#     global i
#     i += 1
#     return i
#
#
# # x = generater()
# # print(next(x))
# # print(next(x))
# # print(next(x))
#
# print(foo())

import json
import pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun

# 备份集合
facebook = urun.post_year
conn = pymongo.MongoClient('127.0.0.1', 27017)
backup = conn.backup
for i in facebook.find():
    backup.post_year.insert(i)
