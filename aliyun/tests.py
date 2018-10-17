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
# import pymongo
#
# conn = pymongo.MongoClient('mongodb://120.78.237.213:27017')
# urun = conn.taskDnsSwitch
#
#
#
# data = {
#     "name" : '热门微博',
#     "domain" :'hd.hotweibo.yunrunyuqing.com',
#     "main_ip" : '58.56.160.41:38015',
#     "backup_ip" : '120.78.237.138:38015',
#     "monitor" : 'http://hd.hotweibo.yunrunyuqing.com:38015/hadoop_change_hosts.html',
#     "changing" : False,
#     "end_time" : None,
#     "close" : False
# }
# urun['aliyun_dns'].insert(data)
# print(data)
import socket

domain = 'hd.hotweibo.yunrunyuqing.com'
current_ip = socket.gethostbyname(domain)
print(current_ip)