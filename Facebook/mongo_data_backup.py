import pymongo

# 备份集合
conn = pymongo.MongoClient('127.0.0.1', 27017)
initial_name = 'spacedata_6666'
backup_name = 'facebook_spacedata'

initial = conn.urun[initial_name]
backup = conn.backup[backup_name]

for i in initial.find():
    backup.insert(i)
