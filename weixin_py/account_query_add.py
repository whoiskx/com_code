import pymssql
from flask import (
    Flask,
    request,
    jsonify,
)

# 微信旧库
MYSQL_HOST = '183.131.241.60'
MYSQL_PORT = 38019
MYSQL_USER = 'oofraBnimdA_gz'
MYSQL_PASSWORD = 'fo(25R@A!@8a823#@%'
MYSQL_DATABASE = 'Winxin'

config_mysql = {
    'server': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'database': MYSQL_DATABASE,
    'password': MYSQL_PASSWORD,
    'charset': 'utf8',
}

# 问题：每次请求连接还是一直连接
db = pymssql.connect(**config_mysql)
cursor = db.cursor()
# cursor.execute("select * from WXAccount")
# details = cursor.fetchmany(10)


class Account(object):
    def __init__(self):
        self.id = ''
        self.name = ''
        self.url = ''
        self.account = ''
        self.features = ''
        self.certified = ''
        self.pause = ''
        self.logourl = ''
        self.codeurl = ''
        self.number = ''
        self.imageUrl = ''
        self.origin = ''
        self.NND = ''
        self.total = ''
        self.collectiontime = ''
        self.interval = ''
        self.maxupdatecount = ''
        self.articleinterval = ''
        self.label = ''
        self.biz = ''

    def to_dict(self):
        return self.__dict__


app = Flask(__name__)
path = '/search/common/wxaccount/select'


@app.route(path, methods=['GET', 'POST'])
def index():
    details = []
    items = details
    all_accounts = []
    if request.method == 'GET':
        query_name = request.args.get("account")
        for item in items:
            account = Account()
            # 自增字段
            account.id = item[0]
            account.name = item[1]
            #
            account.url = item[4]
            account.account = item[2]
            account.features = item[5]
            account.certified = item[6]
            account.pause = item[12]
            account.logourl = item[7]
            account.codeurl = item[8]
            # ??
            account.number = 0
            account.imageUrl = item[14]
            account.origin = item[13]
            account.NND = item[17]
            account.total = item[16]
            account.collectiontime = item[22]
            account.interval = item[9]
            account.maxupdatecount = item[21]
            account.articleinterval = item[20]
            account.label = item[10]
            account.biz = item[23]

            print(account.to_dict())
            all_accounts.append(account.to_dict())

        print(all_accounts)
        for account_info in all_accounts:
            if query_name == account_info.get('account'):
                return jsonify(account_info)

    if request.method == 'POST':
        # 插入数据  ?? 需要判重么
        account_insert = request.form.to_dict()
        account_add = Account()
        account_add.id = account_insert.get('id')
        account_add.name = account_insert.get('name')
        account_add.url = account_insert.get('url')
        account_add.account = account_insert.get('account')
        account_add.features = account_insert.get('features')
        account_add.certified = account_insert.get('certified')
        account_add.pause = account_insert.get('pause')
        account_add.logourl = account_insert.get('logourl')
        account_add.codeurl = account_insert.get('codeurl')
        account_add.number = account_insert.get('number')
        account_add.imageUrl = account_insert.get('imageUrl')
        account_add.origin = account_insert.get('origin')
        account_add.NND = account_insert.get('NND')
        account_add.total = account_insert.get('total')
        account_add.collectiontime = account_insert.get('collectiontime')
        account_add.interval = account_insert.get('interval')
        account_add.maxupdatecount = account_insert.get('maxupdatecount')
        account_add.articleinterval = account_insert.get('articleinterval')
        account_add.label = account_insert.get('label')
        account_add.biz = account_insert.get('biz')

        # "id": 50000000,
        # "name": "音乐 ",
        # "url": "http://weixin.sogou.com/gzh?openid=oIWsFt9mKf6FxwPku87xU-saEi14",
        # "account": "chaoliunvren88",
        #  "imageUrl": "Images/50000/50000000.jpg",  暂时不管
        # "collectiontime": "2018/8/2 12:30:00",
        #  "biz": "MzA5NTExOTIzNQ=="
        print(account_insert)
        # cursor.execute(
        #     "INSERT INTO WXAccount_copy(id, name, url, account, features, certified, pause, logourl, codeurl, number, imageUrl, Origin, NND, total, collectiontime, interval, maxupdatecount, articleinterval, label, biz "
        #     "VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",
        #     (account_add.id, account_add.name, account_add.url, account_add.account, account_add.features,
        #      account_add.certified, account_add.pause, account_add.logourl, account_add.codeurl,
        #      account_add.number, account_add.imageUrl, account_add.origin, account_add.NND, account_add.total,
        #      account_add.collectiontime, account_add.interval, account_add.maxupdatecount,
        #      account_add.articleinterval, account_add.label, account_add.biz,))

        # cursor.execute("INSERT INTO WXAccount_copy(name) VALUES({})".format(123))
        cursor.execute("insert into WXAccount_copy(name, url) VALUES({}, {})".format('afdaasfasdfadf', 'dafadfdafadfasf'))

        # cursor.execute("select * from WXAccount")
        # print(cursor.fetchmany(2))
        # cursor.fetchmany(10)
        return 'ok'


if __name__ == '__main__':
    app.run()
