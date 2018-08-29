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

from sql_server_to_xx import cursor, Account, db
account_init = Account()

cursor.execute(
    "INSERT INTO WXAccount_copy(Name) VALUES(%s)",
    (100000000))
# cursor.execute(
#     "INSERT INTO WXAccount_copy(ID, Name, Url, Account, Features, Certified, Pause, Logourl, Codeurl, Number, ImageUrl, Origin, NND, Total, Collectiontime, Interval, Maxupdatecount, Articleinterval, Label, Biz) "
#     "VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",
#     (account_init.id, account_init.name, account_init.url, account_init.account, account_init.features,
#      account_init.certified, account_init.pause, account_init.logourl, account_init.codeurl,
#      account_init.number, account_init.imageUrl, account_init.origin, account_init.NND, account_init.total,
#      account_init.collectiontime, account_init.interval, account_init.maxupdatecount,
#      account_init.articleinterval, account_init.label, account_init.biz,))
db.commit()