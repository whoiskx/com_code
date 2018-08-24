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
twitter = {'name': 'hd.twitter', 'domain': 'hd.twitter.yunrunyuqing.com', 'main_ip': '60.190.238.166',
             'backup_ip': '120.78.237.190', 'monitor': "http://hd.twitter.yunrunyuqing.com:38010/hadoop_change_hosts.html",
             'changing': False, 'end_time': None,  'close': False}

article = {'name': 'hd.comment', 'domain': 'hd.comment.yunrunyuqing.com', 'main_ip': '60.190.238.166',
             'backup_ip': '120.78.237.190', 'monitor': "http://hd.comment.yunrunyuqing.com:38010/hadoop_change_hosts.html",
             'changing': False, 'end_time': None,  'close': False}

# urun['aliyun_dns'].insert(d)
conn_product['taskDnsSwitch']['aliyun_dns'].insert(article)
