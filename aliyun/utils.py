import pymongo
# 本地
# conn = pymongo.MongoClient()
# urun = conn.urun

# 生产
conn_product = pymongo.MongoClient('mongodb://120.78.237.213:27017')
print(conn_product.database_names)
# item = urun['aliyun_dns'].find()
# for i in item:
#     print(i)

# 'current_domain': '61.164.49.130',
d = {'name': 'test', 'domain': 'test.yunrunyuqing.com', 'main_ip': '61.164.49.130',
             'backup_ip': '124.239.144.163', 'monitor': "http://test.yunrunyuqing.com:19002/test.html",
             'changing': False, 'end_time': None,  'close': False}

# urun['aliyun_dns'].insert(d)
conn_product['taskDnsSwitch']['aliyun'].insert(d)
