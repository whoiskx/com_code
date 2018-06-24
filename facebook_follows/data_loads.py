import json
import pymongo
from setting import urun

# 备份集合
facebook = urun.facebook
conn = pymongo.MongoClient('127.0.0.1', 27017)
backup = conn.backup
for i in facebook.find():
    backup.facebook.insert(i)
