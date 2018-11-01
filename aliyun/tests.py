# import socket
#
# url = 'test.yunrunyuqing.com'
# url = 'crawler.newextract.yunrunyuqing.com'
# ip = socket.gethostbyname(url)
# print(ip)
#
# from urllib.parse import urlparse
# url = 'http://test.yunrunyunqing.com:19002/test.html'
# parsed_url = urlparse(url)
#
# print(parsed_url.netloc)
# i= 0
# while True:
#     if i > 3:
#         break
#     i += 1
#     print(i)
#
# import requests
# url = 'http://localhost:5005'
# requests.get(url)
import pymongo

conn = pymongo.MongoClient('mongodb://120.78.237.213:27017')
urun = conn.taskDnsSwitch

#微博博主信息	60.190.238.178:38010	120.78.170.138:38010	http://hd.blogger.yunrunyuqing.com:38010/hadoop_change_hosts.html	38010	王贺伟	可交付	OK

#微信公众号	60.190.238.178:38010	120.78.170.138:38010	http://hd.wxaccount.yunrunyuqing.com:38010/hadoop_change_hosts.html	38010	王贺伟	可交付	OK

# 新闻APP   	60.190.238.178:38010	120.78.170.138:38010	http://hd.rcmd.yunrunyuqing.com:38010/hadoop_change_hosts.html	38010	王贺伟	可交付	OK
# info = '微信公众号	60.190.238.178:38010	120.78.170.138:38010	http://hd.wxaccount.yunrunyuqing.com:38010/hadoop_change_hosts.html	38010	王贺伟	可交付	OK'
# print(' '.join(info.split()))
# info = ' '.join(info.split())
# result = info.split(' ')[:4]
# print(result)
# 新闻APP   	60.190.238.178:38010	120.78.170.138:38010	http://hd.rcmd.yunrunyuqing.com:38010/hadoop_change_hosts.html	38010
# 文章评论	60.190.238.178:38010	120.78.237.190:38010	http://hd.comment.yunrunyuqing.com:38010/hadoop_change_hosts.html
# 全局境外社交	60.190.238.178:38010	120.78.237.190:38010	http://hd.twitter.yunrunyuqing.com:38010/hadoop_change_hosts.html
# 全局文章接口	        58.56.160.41:38015	120.78.237.190:38015	http://hd.article.yunrunyuqing.com:38015/hadoop_change_hosts.html
# 全局文章外语接口	58.56.160.41:38015	120.78.237.190:38015	http://hd.articlewy.yunrunyuqing.com:38015/hadoop_change_hosts.html
# 全局文章折叠话题	58.56.160.41:38015	120.78.237.190:38015	http://hd.foldarticletopic.yunrunyuqing.com:38015/hadoop_change_hosts.html

# 全局微博	58.56.160.41:38015	47.101.129.120:38015	http://hd.weibo.yunrunyuqing.com:38015/hadoop_change_hosts.html
# 全局微信	60.190.238.178:38010	47.101.129.120:38010	http://hd.weixin.yunrunyuqing.com:38015/hadoop_change_hosts.html	38010	王贺伟	可交付	OK
# 舆情垃圾判断	124.239.144.164:7109	120.78.237.190:7109	http://dm.textclassify.yunrunyuqing.com:7109/dm_change_hosts.html

data = {
    "name": '舆情垃圾判断',
    "domain": 'dm.textclassify.yunrunyuqing.com',
    "main_ip": '124.239.144.164',
    "backup_ip": '120.78.237.190',
    "monitor": 'http://dm.textclassify.yunrunyuqing.com:7109/dm_change_hosts.html',
    "changing": False,
    "end_time": None,
    "close": False
}
urun['aliyun_dns'].insert(data)
print('OK')

# import socket
#
# domain = 'hd.blogger.yunrunyuqing.com'
# current_ip = socket.gethostbyname(domain)
# print(current_ip)
