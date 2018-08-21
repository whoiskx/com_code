import pymongo

conn = pymongo.MongoClient()

urun = conn.urun
# item = urun['aliyun_dns'].find()
# for i in item:
#     print(i)

# d = {'name': 'test', 'domain': 'test.yunrunyuqing.com', 'main_ip': '61.164.49.130',
#              'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
#              'changing': False, 'end_time': None, 'current_domain': '61.164.49.130', 'close': False}
# urun['aliyun_dns'].insert(d)