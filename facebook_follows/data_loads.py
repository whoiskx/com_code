import json
import pymongo
from setting import urun

# 备份集合
facebook = urun.facebook_group_members
conn = pymongo.MongoClient('127.0.0.1', 27017)
backup = conn.backup
for i in facebook.find():
    backup.facebook_group_members.insert(i)
