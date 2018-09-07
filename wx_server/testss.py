import pymongo
conn = pymongo.MongoClient('120.78.237.213', 27017)
db = conn.WeChat
db['account'].insert({})