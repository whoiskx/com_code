# # l =[('ID',), ('Name',), ('Account',), ('Category',), ('Url',), ('Feature',), ('Certification',), ('LogoUrl',), ('CodeUrl',), ('Interval',), ('Label',), ('Addon',), ('Pause',), ('Origin',), ('ImageUrl',), ('IsRL',), ('total',), ('NND',), ('Hot',), ('UpdateTime',), ('ArticleInterval',), ('MaxUpdateCount',), ('CollectionTime',), ('Biz',), ('MonPub',), ('MonView',), ('AutoFM',)]
# # for index, name in enumerate(l):
# #     x
# # import requests
# #
# # url = 'https://wenku.baidu.com/view/ae675f50d1f34693dbef3e81.html?re=view'
# # r = requests.get(url)
# # print(r.text)
#
# d ={
#     "id": 50000000,
#     "name": "音乐 ",
#     "url": "http://weixin.sogou.com/gzh?openid=oIWsFt9mKf6FxwPku87xU-saEi14",
#     "account": "chaoliunvren88",
#     "features": "",
#     "certified": "",
#     "pause": 0,
#     "logourl": None,
#     "codeurl": None,
#     "number": 0,
#     "imageUrl": "Images/50000/50000000.jpg",
#     "Origin": "0",
#     "NND": 0,
#     "total": 170,
#     "collectiontime": "2018/8/2 12:30:00",
#     "interval": 11520,
#     "maxupdatecount": 0,
#     "articleinterval": 0,
#     "label": 1,
#     "biz": "MzA5NTExOTIzNQ=="
# }
# print(len(d.keys()))
# for i in d.keys():
#     print(i,end=', ')

s = """ account_init.id = account_insert.get('id')
        account_init.name = account_insert.get('name')
        account_init.url = account_insert.get('url')
        account_init.account = account_insert.get('account')
        account_init.features = account_insert.get('features')
        account_init.certified = account_insert.get('certified')
        account_init.pause = account_insert.get('pause')
        account_init.logourl = account_insert.get('logourl')
        account_init.codeurl = account_insert.get('codeurl')
        account_init.number = account_insert.get('number')
        account_init.imageUrl = account_insert.get('imageUrl')
        account_init.origin = account_insert.get('origin')
        account_init.NND = account_insert.get('NND')
        account_init.total = account_insert.gettotal('total')
        account_init.collectiontime = account_insert.get('collectiontime')
        account_init.interval = account_insert.get('interval')
        account_init.maxupdatecount = account_insert.get('maxupdatecount')
        account_init.articleinterval = account_insert.get('articleinterval')
        account_init.label = account_insert.get('label')
        account_init.biz = account_insert.get('biz')"""

# aa = s.split("\n")
# print(aa)
# ss = ''
# for a in aa:
#     ss = a.split('=')[0]
#     print(ss, end=',')
#
# from sql_server_to_xx import cursor, Account, db
# account_init = Account()
#
# cursor.execute(
#     "INSERT INTO WXAccount_copy(Name) VALUES(%s)",
#     (100000000))
# # cursor.execute(
# #     "INSERT INTO WXAccount_copy(ID, Name, Url, Account, Features, Certified, Pause, Logourl, Codeurl, Number, ImageUrl, Origin, NND, Total, Collectiontime, Interval, Maxupdatecount, Articleinterval, Label, Biz) "
# #     "VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",
# #     (account_init.id, account_init.name, account_init.url, account_init.account, account_init.features,
# #      account_init.certified, account_init.pause, account_init.logourl, account_init.codeurl,
# #      account_init.number, account_init.imageUrl, account_init.origin, account_init.NND, account_init.total,
# #      account_init.collectiontime, account_init.interval, account_init.maxupdatecount,
# #      account_init.articleinterval, account_init.label, account_init.biz,))
# db.commit()
#
# s = "{\"ID\": \"662b56cfdf17b40eea98dec01a49d8c1\", \"Account\": \"dadingyuju\", \"TaskID\": \"50446290\", \"TaskName\": \"\\u5fae\\u4fe1_\\u5927\\u9f0e\\u8c6b\\u5267\", \"AccountID\": \"50446290\", \"SiteID\": 50446290, \"TopicID\": 0, \"Url\": \"https://mp.weixin.qq.com/s?timestamp=1535708054&src=3&ver=1&signature=uulJZSS6rD01od4FwW9jJVf-6zHwwnEKrKpjPzyfHSvzN5DHz6Mt5sttdFtt5mJ-0WYUM7ghoLrquD78QNMCtli8C-dR9H9xiZk8Nf2n7HnLO3z0RAk1ldHOWo-KEVUa*rtNs6FG6OWYCz7K5lfbXM-xbO6lFN*leS1RrlKnfSg=\", \"Title\": \"\\u3010\\u7ecf\\u5178\\u5c0f\\u54c1\\u3011\\u300a\\u7b11\\u8c08\\u4eba\\u751f\\u300b\\u7b11\\u5f97\\u6211\\u809a\\u5b50\\u75db\\uff01\", \"Content\": \"\\u7eb5\\u770b\\u53e4\\u4eca\\uff0c\\u4eba\\u751f\\u7686\\u620f\\uff0c\\u620f\\u6620\\u4eba\\u751f\\u3002\\u70b9\\u51fb\\u6807\\u9898\\u4e0b\\u7684\\u84dd\\u5b57\\u201c\\u5927\\u9f0e\\u8c6b\\u5267\\u201d\\uff0c\\u6211\\u4eec\\u5c06\\u514d\\u8d39\\u4e3a\\u60a8\\u63d0\\u4f9b\\u7ecf\\u5178\\u620f\\u5267\\u3001\\u66f2\\u827a\\u3001\\u65b0\\u95fb\\u8f76\\u4e8b\\u53ca\\u6df1\\u5ea6\\u54f2\\u6587\\uff0c\\u4e3a\\u60a8\\u7684\\u751f\\u6d3b\\u589e\\u5149\\u6dfb\\u5f69\\u3002\\n\\u3010\\u7ecf\\u5178\\u5c0f\\u54c1\\u3011\\u300a\\u7535\\u68af\\u5185\\u5916\\u300b\\u300a\\u7b11\\u8c08\\u4eba\\u751f\\u300b\\u7b11\\u5f97\\u6211\\u809a\\u5b50\\u75db\\uff01\\u90ed\\u51ac\\u4e34 \\u6731\\u519b \\u51af\\u5de9\\u7b49\\u8868\\u6f14\\n\\n\\n\\n\\n\\u7b11\\u4e00\\u7b11\\uff0c\\u5341\\u5e74\\u5c11\\n1\\u3001\\u8bb0\\u8005\\uff1a\\u201c\\u4f60\\u597d\\uff0c\\u80fd\\u4e0d\\u80fd\\u8c08\\u4e0b\\u4f60\\u7684\\u521b\\u4e1a\\u7ecf\\u5386\\u5462?\\u201d\\n\\u6211\\u8bf4\\uff1a\\u201c\\u6211\\u4ee5\\u524d\\u5f00\\u8fc7\\u4e00\\u5bb6\\u65e9\\u9910\\u5e97\\uff0c\\u624d\\u5f00\\u4e86\\u4e0d\\u5230\\u4e00\\u4e2a\\u661f\\u671f\\u5c31\\u5012\\u95ed\\u4e86\\u201d\\n\\u8bb0\\u8005\\uff1a\\u201c\\u4e3a\\u4ec0\\u4e48\\u5462\\uff1f\\u201d\\n\\u6211\\uff1a\\u201c\\u56e0\\u4e3a\\u6211\\u65e9\\u4e0a\\u8d77\\u4e0d\\u6765\\uff0c\\u73b0\\u5728\\u6539\\u6210\\u591c\\u5e02\\u4e86\\u201d\\n\\u8bb0\\u8005\\uff1a\\u201c\\u73b0\\u5728\\u751f\\u610f\\u4e00\\u5b9a\\u5f88\\u597d\\u5427\\u201d\\n\\u6211\\uff1a\\u201c\\u54ce\\uff0c\\u65f6\\u95f4\\u4e0d\\u65e9\\u4e86\\uff0c\\u5df2\\u7ecf\\u516b\\u70b9\\u534a\\u4e86\\uff0c\\u6211\\u8981\\u6536\\u644a\\u4e86\\uff0c\\u56f0\\u4e86\\u201d\\n\\u8bb0\\u8005\\uff1a\\u201c.....................................\\u201d\\n\\n\\n2\\u3001\\u5f00\\u5b66\\u7b2c\\u4e00\\u5929\\uff0c\\u5168\\u73ed\\u81ea\\u6211\\u4ecb\\u7ecd\\uff0c\\u4e00\\u4e2a\\u7537\\u751f\\u8d70\\u4e0a\\u8bb2\\u53f0\\uff0c\\u8bf4\\u201c\\u5927\\u5bb6\\u597d\\uff0c\\u6211\\u53eb\\u5c24\\u6c38\\uff0c\\u6211\\u7231\\u4e0b\\u68cb\\u3002\\u201d\\u63a5\\u4e0b\\u6765\\u662f\\u4e00\\u4e2a\\u5973\\u751f\\uff0c\\u5979\\u5a07\\u7f9e\\u7f9e\\u5730\\u8d70\\u4e0a\\u8bb2\\u53f0\\uff0c\\u5fd0\\u5fd1\\u4e0d\\u5b89\\u5730\\u81ea\\u6211\\u4ecb\\u7ecd\\uff1a\\u201c\\u6211\\u53eb\\u590f\\u742a\\uff0c\\u6211\\u559c\\u6b22\\u6e38\\u6cf3\\u3002\\u201d\\u5168\\u73ed\\u7206\\u53d1\\u51fa\\u4e86\\u70ed\\u70c8\\u7684\\u638c\\u58f0\\uff01\\uff01\\uff01\\n\\n\\n3\\u3001\\u4e0a\\u8bfe\\u65f6\\u5019\\uff0c\\u6211\\u7761\\u7740\\u4e86\\uff0c\\u8001\\u5e08\\u7a81\\u7136\\u53eb\\u6211\\u56de\\u7b54\\u95ee\\u9898\\uff0c\\u6211\\u4e00\\u8138\\u61f5\\u903c\\u7684\\u7ad9\\u8d77\\u6765\\u3002\\n\\u540c\\u684c\\u6084\\u6084\\u8bf4\\u9053\\uff1a\\u201c\\u9009A\\u201d\\n\\u8fd9\\u65f6\\uff0c\\u6211\\u524d\\u9762\\u4e00\\u4e2a\\u54e5\\u4eec\\u8bf4\\u9053\\uff1a\\u201c\\u542c\\u6211\\u7684\\uff0c\\u9009B\\u201d\\n\\u65c1\\u8fb9\\u7684\\u540c\\u5b66\\u53c8\\u8bf4\\u9053\\uff1a\\u201c\\u8fd9\\u7edd\\u5bf9\\u9009D\\u554a\\u201d\\n\\u6211\\u81ea\\u4fe1\\u4e00\\u7b11\\uff0c\\u7b54\\u9053\\uff1a\\u201c\\u8001\\u5e08\\uff0c\\u8fd9\\u9053\\u9898\\u9009C\\u201d\\n\\u53ea\\u89c1\\u8001\\u5e08\\u9752\\u7b4b\\u66b4\\u8d77\\uff0c\\u51b2\\u6211\\u543c\\u9053\\uff1a\\u201c\\u8fd9\\u662f\\u4e00\\u9053\\u5224\\u65ad\\u9898\\uff01\\u201d\\n4\\u3001\\u4e00\\u54e5\\u4eec\\u4e0a\\u73ed\\u8fdf\\u5230\\u4e86\\u3002\\n\\u9886\\u5bfc\\u6124\\u6012\\u5730\\u95ee\\uff1a\\u201c\\u4f60\\u4e3a\\u4ec0\\u4e48\\u8fd9\\u4e48\\u665a\\u624d\\u6765\\uff1f\\u201d\\n\\u8fd9\\u54e5\\u4eec\\u56de\\u7b54\\uff1a\\u201c\\u4e0d\\u597d\\u610f\\u601d\\uff0c\\u7761\\u8fc7\\u5934\\u4e86\\u201d\\n\\u9886\\u5bfc\\uff1a\\u201c\\u4e3a\\u4ec0\\u4e48\\u7761\\u8fc7\\u5934\\uff0c\\u600e\\u4e48\\u56de\\u4e8b\\u554a\\uff1f\\u201d\\n\\u54e5\\u4eec\\u56de\\u7b54\\uff1a\\u201c\\u505a\\u68a6\\uff0c\\u68a6\\u89c1\\u5f00\\u4f1a\\uff0c\\u60a8\\u5728\\u4f5c\\u91cd\\u8981\\u8bb2\\u8bdd\\uff0c\\u89c9\\u5f97\\u7279\\u522b\\u7cbe\\u5f69\\uff0c\\u5c31\\u60f3\\u591a\\u542c\\u4e00\\u4f1a\\u3002\\u201d\\n\\u5168\\u529e\\u516c\\u5ba4\\u987f\\u65f6\\u54cd\\u8d77\\u96f7\\u9e23\\u822c\\u7684\\u638c\\u58f0\\uff0c\\u673a\\u667a\\u8fd1\\u5996\\u554a\\uff01\\n\\n\\n5\\u3001\\u4fee\\u624b\\u673a\\u3002\\u4e00\\u4e2a\\u4eba\\u8dd1\\u8fc7\\u6765\\u95ee\\uff0c\\n\\u82f9\\u679c\\u516d\\u6389\\u6c34\\u91cc\\u4e86\\u80fd\\u4fee\\u597d\\u5417\\uff1f\\n\\u6211\\u8bf4\\uff1a\\u201c\\u8fd9\\u4e2a\\u4e0d\\u6562\\u786e\\u5b9a\\uff0c\\u8981\\u5177\\u4f53\\u770b\\u4e00\\u4e0b\\u4e25\\u4e0d\\u4e25\\u91cd\\u201d\\n\\u90a3\\u4eba\\u8bf4\\uff1a\\u201c\\u4f60\\u8981\\u662f\\u786e\\u5b9a\\u80fd\\u4fee\\u597d\\uff0c\\u6211\\u5c31\\u53bb\\u6cb3\\u91cc\\u635e\\uff0c\\u4e0d\\u786e\\u5b9a\\u6211\\u5c31\\u4e0d\\u53bb\\u635e\\u4e86\\u201d\\n\\n\\n6\\u3001\\u6709\\u4e00\\u6b21\\uff0c\\u6211\\u4eec\\u73ed\\u7ea7\\u6765\\u4e86\\u4e00\\u4f4d\\u65b0\\u8001\\u5e08\\uff0c\\u6559\\u6570\\u5b66\\u7684\\uff0c\\u4e0a\\u7b2c\\u4e00\\u5802\\u8bfe\\uff0c\\u8001\\u5e08\\u60f3\\u8ddf\\u540c\\u5b66\\u4eec\\u8ba4\\u8bc6\\u4e0b\\uff0c\\u4e8e\\u662f\\u5f00\\u59cb\\u70b9\\u540d\\uff0c\\u5f53\\u70b9\\u5230\\u67d0\\u4e2a\\u540c\\u5b66\\u7684\\u540d\\u5b57\\u65f6\\u5019\\uff0c\\n\\u8001\\u5e08\\uff1a\\u201c\\u8d75\\u534e\\u660e\\u201d\\n\\u540c\\u5b66\\uff1a\\u201c\\u591c!\\u201d\\n\\u8001\\u5e08\\uff1a\\u201c\\u8d75\\u534e\\u660e\\uff01\\u201d\\n\\u540c\\u5b66\\uff1a\\u201c\\u591c\\uff01\\u201d\\n\\u8001\\u5e08\\uff1a\\u201c\\u8036\\u4ec0\\u4e48\\u8036\\uff01\\u4f60\\u4eec\\u4ee5\\u524d\\u8001\\u5e08\\u6ca1\\u6709\\u6559\\u8fc7\\u4f60\\u70b9\\u540d\\u8981\\u7b54\\u201c\\u5230\\u201d\\u5417\\u201d\\n\\u540c\\u5b66\\uff1a\\u201c\\u90a3\\u4e2a......\\u8001\\u5e08\\u6211\\u53eb\\u8d75\\u70e8\\u660e\\u3002\\u201d\\n\\u795d\\u300a\\u5927\\u9f0e\\u8c6b\\u5267\\u300b\\u65b0\\u8001\\u670b\\u53cb\\u4eec\\u5e78\\u798f\\u5b89\\u5eb7\\uff0c\\u4e8b\\u4e1a\\u5174\\u65fa\\u3002\\u559c\\u6b22\\u672c\\u8282\\u76ee\\u8bb0\\u5f97\\u8f6c\\u53d1\\u5206\\u4eab\\u81f3\\u670b\\u53cb\\u5708\\uff0c\\u60a8\\u7684\\u652f\\u6301\\u5c31\\u662f\\u6211\\u4eec\\u7684\\u6700\\u5927\\u52a8\\u529b\\uff01\\u66f4\\u591a\\u7cbe\\u5f69\\u8282\\u76ee\\u548c\\u6587\\u7ae0\\u8bf7\\u5728\\u4e0b\\u9762\\u201d\\u9605\\u8bfb\\u539f\\u6587\\u201c\\u67e5\\u770b\\u5386\\u53f2\\u4fe1\\u606f\\u4e3b\\u9875\\u9762\\u4e0a\\u65b9\\u641c\\u7d22\\u680f\\u4e2d\\uff0c\\u518d\\u641c\\u7d22\\u60a8\\u559c\\u6b22\\u7684\\u8282\\u76ee\\u3002\\n\\u3010\\u7248\\u6743\\u58f0\\u660e\\u3011\\u89c6\\u9891\\u56fe\\u6587\\u6765\\u6e90\\u4e8e\\u7f51\\u7edc\\uff0c\\u7248\\u6743\\u5f52\\u539f\\u4f5c\\u8005\\u6240\\u6709\\uff0c\\u82e5\\u4fb5\\u6743\\uff0c\\u8bf7\\u8054\\u7cfb\\u6211\\u4eec\\uff0c\\u8c22\\u8c22\\uff01\", \"Author\": \"\\u5927\\u9f0e\\u8c6b\\u5267\", \"Time\": 1534887000000, \"AddOn\": 1535708155000}"
#
#
# s = '{"ID": "f9b15d04aa8ffe2f74992e2e5d7b6a0a", "Account": "dadingyuju", "TaskID": "50446290", "TaskName": "\\u5fae\\u4fe1_\\u5927\\u9f0e\\u8c6b\\u5267", "AccountID": "50446290", "SiteID": 50446290, "TopicID": 0, "Url": "https://mp.weixin.qq.com/s?timestamp=1535708575&src=3&ver=1&signature=uulJZSS6rD01od4FwW9jJURXm5UJgD8RCkUS9JDmcHXofgwkNVEaQ7pq2XnuMAGxYwDcDZ*lO9AoxCEAEIq*0YlyIJeN4lW5kNtY4xReq1izBM0Rr5S6C7yaitlzHRoHucehry6XHqiEXbA1qS57nXCx9bZ-01JWx0uUE13q4og=", "Title": "\\u3010\\u7ecf\\u5178\\u5c0f\\u54c1\\u3011\\u300a\\u7b11\\u8c08\\u4eba\\u751f\\u300b\\u7b11\\u5f97\\u6211\\u809a\\u5b50\\u75db\\uff01", "Content": "\\u7eb5\\u770b\\u53e4\\u4eca\\uff0c\\u4eba\\u751f\\u7686\\u620f\\uff0c\\u620f\\u6620\\u4eba\\u751f\\u3002\\u70b9\\u51fb\\u6807\\u9898\\u4e0b\\u7684\\u84dd\\u5b57\\u201c\\u5927\\u9f0e\\u8c6b\\u5267\\u201d\\uff0c\\u6211\\u4eec\\u5c06\\u514d\\u8d39\\u4e3a\\u60a8\\u63d0\\u4f9b\\u7ecf\\u5178\\u620f\\u5267\\u3001\\u66f2\\u827a\\u3001\\u65b0\\u95fb\\u8f76\\u4e8b\\u53ca\\u6df1\\u5ea6\\u54f2\\u6587\\uff0c\\u4e3a\\u60a8\\u7684\\u751f\\u6d3b\\u589e\\u5149\\u6dfb\\u5f69\\u3002\\n\\u3010\\u7ecf\\u5178\\u5c0f\\u54c1\\u3011\\u300a\\u7535\\u68af\\u5185\\u5916\\u300b\\u300a\\u7b11\\u8c08\\u4eba\\u751f\\u300b\\u7b11\\u5f97\\u6211\\u809a\\u5b50\\u75db\\uff01\\u90ed\\u51ac\\u4e34 \\u6731\\u519b \\u51af\\u5de9\\u7b49\\u8868\\u6f14\\n\\n\\n\\n\\n\\u7b11\\u4e00\\u7b11\\uff0c\\u5341\\u5e74\\u5c11\\n1\\u3001\\u8bb0\\u8005\\uff1a\\u201c\\u4f60\\u597d\\uff0c\\u80fd\\u4e0d\\u80fd\\u8c08\\u4e0b\\u4f60\\u7684\\u521b\\u4e1a\\u7ecf\\u5386\\u5462?\\u201d\\n\\u6211\\u8bf4\\uff1a\\u201c\\u6211\\u4ee5\\u524d\\u5f00\\u8fc7\\u4e00\\u5bb6\\u65e9\\u9910\\u5e97\\uff0c\\u624d\\u5f00\\u4e86\\u4e0d\\u5230\\u4e00\\u4e2a\\u661f\\u671f\\u5c31\\u5012\\u95ed\\u4e86\\u201d\\n\\u8bb0\\u8005\\uff1a\\u201c\\u4e3a\\u4ec0\\u4e48\\u5462\\uff1f\\u201d\\n\\u6211\\uff1a\\u201c\\u56e0\\u4e3a\\u6211\\u65e9\\u4e0a\\u8d77\\u4e0d\\u6765\\uff0c\\u73b0\\u5728\\u6539\\u6210\\u591c\\u5e02\\u4e86\\u201d\\n\\u8bb0\\u8005\\uff1a\\u201c\\u73b0\\u5728\\u751f\\u610f\\u4e00\\u5b9a\\u5f88\\u597d\\u5427\\u201d\\n\\u6211\\uff1a\\u201c\\u54ce\\uff0c\\u65f6\\u95f4\\u4e0d\\u65e9\\u4e86\\uff0c\\u5df2\\u7ecf\\u516b\\u70b9\\u534a\\u4e86\\uff0c\\u6211\\u8981\\u6536\\u644a\\u4e86\\uff0c\\u56f0\\u4e86\\u201d\\n\\u8bb0\\u8005\\uff1a\\u201c.....................................\\u201d\\n\\n\\n2\\u3001\\u5f00\\u5b66\\u7b2c\\u4e00\\u5929\\uff0c\\u5168\\u73ed\\u81ea\\u6211\\u4ecb\\u7ecd\\uff0c\\u4e00\\u4e2a\\u7537\\u751f\\u8d70\\u4e0a\\u8bb2\\u53f0\\uff0c\\u8bf4\\u201c\\u5927\\u5bb6\\u597d\\uff0c\\u6211\\u53eb\\u5c24\\u6c38\\uff0c\\u6211\\u7231\\u4e0b\\u68cb\\u3002\\u201d\\u63a5\\u4e0b\\u6765\\u662f\\u4e00\\u4e2a\\u5973\\u751f\\uff0c\\u5979\\u5a07\\u7f9e\\u7f9e\\u5730\\u8d70\\u4e0a\\u8bb2\\u53f0\\uff0c\\u5fd0\\u5fd1\\u4e0d\\u5b89\\u5730\\u81ea\\u6211\\u4ecb\\u7ecd\\uff1a\\u201c\\u6211\\u53eb\\u590f\\u742a\\uff0c\\u6211\\u559c\\u6b22\\u6e38\\u6cf3\\u3002\\u201d\\u5168\\u73ed\\u7206\\u53d1\\u51fa\\u4e86\\u70ed\\u70c8\\u7684\\u638c\\u58f0\\uff01\\uff01\\uff01\\n\\n\\n3\\u3001\\u4e0a\\u8bfe\\u65f6\\u5019\\uff0c\\u6211\\u7761\\u7740\\u4e86\\uff0c\\u8001\\u5e08\\u7a81\\u7136\\u53eb\\u6211\\u56de\\u7b54\\u95ee\\u9898\\uff0c\\u6211\\u4e00\\u8138\\u61f5\\u903c\\u7684\\u7ad9\\u8d77\\u6765\\u3002\\n\\u540c\\u684c\\u6084\\u6084\\u8bf4\\u9053\\uff1a\\u201c\\u9009A\\u201d\\n\\u8fd9\\u65f6\\uff0c\\u6211\\u524d\\u9762\\u4e00\\u4e2a\\u54e5\\u4eec\\u8bf4\\u9053\\uff1a\\u201c\\u542c\\u6211\\u7684\\uff0c\\u9009B\\u201d\\n\\u65c1\\u8fb9\\u7684\\u540c\\u5b66\\u53c8\\u8bf4\\u9053\\uff1a\\u201c\\u8fd9\\u7edd\\u5bf9\\u9009D\\u554a\\u201d\\n\\u6211\\u81ea\\u4fe1\\u4e00\\u7b11\\uff0c\\u7b54\\u9053\\uff1a\\u201c\\u8001\\u5e08\\uff0c\\u8fd9\\u9053\\u9898\\u9009C\\u201d\\n\\u53ea\\u89c1\\u8001\\u5e08\\u9752\\u7b4b\\u66b4\\u8d77\\uff0c\\u51b2\\u6211\\u543c\\u9053\\uff1a\\u201c\\u8fd9\\u662f\\u4e00\\u9053\\u5224\\u65ad\\u9898\\uff01\\u201d\\n4\\u3001\\u4e00\\u54e5\\u4eec\\u4e0a\\u73ed\\u8fdf\\u5230\\u4e86\\u3002\\n\\u9886\\u5bfc\\u6124\\u6012\\u5730\\u95ee\\uff1a\\u201c\\u4f60\\u4e3a\\u4ec0\\u4e48\\u8fd9\\u4e48\\u665a\\u624d\\u6765\\uff1f\\u201d\\n\\u8fd9\\u54e5\\u4eec\\u56de\\u7b54\\uff1a\\u201c\\u4e0d\\u597d\\u610f\\u601d\\uff0c\\u7761\\u8fc7\\u5934\\u4e86\\u201d\\n\\u9886\\u5bfc\\uff1a\\u201c\\u4e3a\\u4ec0\\u4e48\\u7761\\u8fc7\\u5934\\uff0c\\u600e\\u4e48\\u56de\\u4e8b\\u554a\\uff1f\\u201d\\n\\u54e5\\u4eec\\u56de\\u7b54\\uff1a\\u201c\\u505a\\u68a6\\uff0c\\u68a6\\u89c1\\u5f00\\u4f1a\\uff0c\\u60a8\\u5728\\u4f5c\\u91cd\\u8981\\u8bb2\\u8bdd\\uff0c\\u89c9\\u5f97\\u7279\\u522b\\u7cbe\\u5f69\\uff0c\\u5c31\\u60f3\\u591a\\u542c\\u4e00\\u4f1a\\u3002\\u201d\\n\\u5168\\u529e\\u516c\\u5ba4\\u987f\\u65f6\\u54cd\\u8d77\\u96f7\\u9e23\\u822c\\u7684\\u638c\\u58f0\\uff0c\\u673a\\u667a\\u8fd1\\u5996\\u554a\\uff01\\n\\n\\n5\\u3001\\u4fee\\u624b\\u673a\\u3002\\u4e00\\u4e2a\\u4eba\\u8dd1\\u8fc7\\u6765\\u95ee\\uff0c\\n\\u82f9\\u679c\\u516d\\u6389\\u6c34\\u91cc\\u4e86\\u80fd\\u4fee\\u597d\\u5417\\uff1f\\n\\u6211\\u8bf4\\uff1a\\u201c\\u8fd9\\u4e2a\\u4e0d\\u6562\\u786e\\u5b9a\\uff0c\\u8981\\u5177\\u4f53\\u770b\\u4e00\\u4e0b\\u4e25\\u4e0d\\u4e25\\u91cd\\u201d\\n\\u90a3\\u4eba\\u8bf4\\uff1a\\u201c\\u4f60\\u8981\\u662f\\u786e\\u5b9a\\u80fd\\u4fee\\u597d\\uff0c\\u6211\\u5c31\\u53bb\\u6cb3\\u91cc\\u635e\\uff0c\\u4e0d\\u786e\\u5b9a\\u6211\\u5c31\\u4e0d\\u53bb\\u635e\\u4e86\\u201d\\n\\n\\n6\\u3001\\u6709\\u4e00\\u6b21\\uff0c\\u6211\\u4eec\\u73ed\\u7ea7\\u6765\\u4e86\\u4e00\\u4f4d\\u65b0\\u8001\\u5e08\\uff0c\\u6559\\u6570\\u5b66\\u7684\\uff0c\\u4e0a\\u7b2c\\u4e00\\u5802\\u8bfe\\uff0c\\u8001\\u5e08\\u60f3\\u8ddf\\u540c\\u5b66\\u4eec\\u8ba4\\u8bc6\\u4e0b\\uff0c\\u4e8e\\u662f\\u5f00\\u59cb\\u70b9\\u540d\\uff0c\\u5f53\\u70b9\\u5230\\u67d0\\u4e2a\\u540c\\u5b66\\u7684\\u540d\\u5b57\\u65f6\\u5019\\uff0c\\n\\u8001\\u5e08\\uff1a\\u201c\\u8d75\\u534e\\u660e\\u201d\\n\\u540c\\u5b66\\uff1a\\u201c\\u591c!\\u201d\\n\\u8001\\u5e08\\uff1a\\u201c\\u8d75\\u534e\\u660e\\uff01\\u201d\\n\\u540c\\u5b66\\uff1a\\u201c\\u591c\\uff01\\u201d\\n\\u8001\\u5e08\\uff1a\\u201c\\u8036\\u4ec0\\u4e48\\u8036\\uff01\\u4f60\\u4eec\\u4ee5\\u524d\\u8001\\u5e08\\u6ca1\\u6709\\u6559\\u8fc7\\u4f60\\u70b9\\u540d\\u8981\\u7b54\\u201c\\u5230\\u201d\\u5417\\u201d\\n\\u540c\\u5b66\\uff1a\\u201c\\u90a3\\u4e2a......\\u8001\\u5e08\\u6211\\u53eb\\u8d75\\u70e8\\u660e\\u3002\\u201d\\n\\u795d\\u300a\\u5927\\u9f0e\\u8c6b\\u5267\\u300b\\u65b0\\u8001\\u670b\\u53cb\\u4eec\\u5e78\\u798f\\u5b89\\u5eb7\\uff0c\\u4e8b\\u4e1a\\u5174\\u65fa\\u3002\\u559c\\u6b22\\u672c\\u8282\\u76ee\\u8bb0\\u5f97\\u8f6c\\u53d1\\u5206\\u4eab\\u81f3\\u670b\\u53cb\\u5708\\uff0c\\u60a8\\u7684\\u652f\\u6301\\u5c31\\u662f\\u6211\\u4eec\\u7684\\u6700\\u5927\\u52a8\\u529b\\uff01\\u66f4\\u591a\\u7cbe\\u5f69\\u8282\\u76ee\\u548c\\u6587\\u7ae0\\u8bf7\\u5728\\u4e0b\\u9762\\u201d\\u9605\\u8bfb\\u539f\\u6587\\u201c\\u67e5\\u770b\\u5386\\u53f2\\u4fe1\\u606f\\u4e3b\\u9875\\u9762\\u4e0a\\u65b9\\u641c\\u7d22\\u680f\\u4e2d\\uff0c\\u518d\\u641c\\u7d22\\u60a8\\u559c\\u6b22\\u7684\\u8282\\u76ee\\u3002\\n\\u3010\\u7248\\u6743\\u58f0\\u660e\\u3011\\u89c6\\u9891\\u56fe\\u6587\\u6765\\u6e90\\u4e8e\\u7f51\\u7edc\\uff0c\\u7248\\u6743\\u5f52\\u539f\\u4f5c\\u8005\\u6240\\u6709\\uff0c\\u82e5\\u4fb5\\u6743\\uff0c\\u8bf7\\u8054\\u7cfb\\u6211\\u4eec\\uff0c\\u8c22\\u8c22\\uff01", "Author": "\\u5927\\u9f0e\\u8c6b\\u5267", "Time": 1534887000000, "AddOn": 1535708674000}'
# import json
#
# ss = json.loads(s)
# print(ss)

# def hash_md5(s):
#     import hashlib
#     m = hashlib.md5()
#     m.update(s.encode(encoding='utf-8'))
#     return m.hexdigest()
# s = '【经典小品】《笑谈人生》笑得我肚子痛！' + '1534887000000'
#
# print(hash_md5(s))

# 解析
# s = {
# "status": 0,
# "msg": "成功",
# "data": "{\"id\":50519673,\"name\":\"襄阳市科技馆\",\"account\":\"xykjgdyh\",\"biz\":\"MzA4MTU2OTYwMw\\u003d\\u003d\",\"url\":\"http://weixin.sogou.com/gzh?openid\\u003doIWsFt6j5gSIDk5QfPMHPtdLg8hw\",\"scheduleID\":1,\"interval\":50,\"labelID\":1,\"destinationID\":1,\"authentication\":\"“绿色消费,你行动了吗?”vrT\",\"introduction\":\"想知道科技馆最新活动吗?想知道最潮流的科普小贴士吗?想对科技馆说悄悄话吗?快来关注我们吧!\",\"logoPath\":\"Images/50519/50519673.jpg\",\"weight\":0,\"pause\":0,\"collectiontime\":\"2018-08-24 00:08:58.0\",\"outtime\":1535133336920,\"ipid\":\"\"}"
# }
# data_json = s.get('data')
# import json
# data = json.loads(data_json)
# print(data)
#
# name = data.get('name')
# print(name)
# ss = json.loads('1')
# print(ss)

s = 'mp.weixin.qq.com\\\\/s?__biz=MjEwNjI0NzM4MQ==&amp;mid=2670247197&amp;idx=4&amp;sn=2486c64c051c62270bbf44b550415315&amp;chksm=4f6922a7781eabb19203b3809b816a26b42bb1330f3e4b69414bbcc5e2b18014cbd04e88825b&amp;scene=27#wechat_redirect'
s = 'mp.weixin.qq.com\\\\/s?__biz=MzA5ODUzOTA0OQ==&amp;mid=2651689502&amp;idx=1&amp;sn=03b19580985efae3703bd302e5945c47&amp;chksm=8b693158bc1eb84e73f780d00ff41a1dd727cd99330b19c072702c13649a2349b0db7202a61a&amp;scene=27#wechat_redirect'
s = '__biz=MzA5ODUzOTA0OQ==&amp;mid=2651689518&amp;idx=1&amp;sn=e94911c2b408a742367abfb36ea1552a&amp;chksm=8b693168bc1eb87e86d2ccd90b89db8bda87aec7e1135822605c68bda96324e9e793d1de1224&amp;scene=27#wechat_redirect'
ss = s.replace('amp;', '')
print(ss)