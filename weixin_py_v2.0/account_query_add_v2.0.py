import pymssql
from flask import (
    Flask,
    request,
    jsonify,
)
from config import get_mysql_old


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
config_mysql = get_mysql_old()


@app.route(path, methods=['GET', 'POST'])
def index():
    db = pymssql.connect(**config_mysql)
    cursor = db.cursor()
    if request.method == 'GET':
        query_name = request.args.get("account")
        cursor.execute("select * from WXAccount_copy where Account='{}'".format(query_name))
        # for item in items:
        item = cursor.fetchone()
        cursor.close()
        db.close()
        if item:
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
            return jsonify(account.to_dict())
        else:
            return '{}'

    if request.method == 'POST':
        # 插入数据  ?? 需要判重么
        get_account = request.form.to_dict()
        account_insert = Account()
        account_insert.name = get_account.get('name')
        account_insert.url = get_account.get('url')
        account_insert.account = get_account.get('account')       
        account_insert.biz = get_account.get('biz')
        account_insert.collectiontime = get_account.get('collectiontime')

        # "id": 50000000,
        # "name": "音乐 ",
        # "url": "http://weixin.sogou.com/gzh?openid=oIWsFt9mKf6FxwPku87xU-saEi14",
        # "account": "chaoliunvren88",
        #  "imageUrl": "Images/50000/50000000.jpg",  暂时不管
        # "collectiontime": "2018/8/2 12:30:00",
        #  "biz": "MzA5NTExOTIzNQ=="
        print(get_account)
        name = account_insert.name
        account = account_insert.account
        url = account_insert.url
        # collectiontime = account_insert.collectiontime
        biz = account_insert.biz

        # collectiontime 用SQL server 自带的GETDATE补充
        insert_sql = """INSERT INTO WXAccount_copy(Name, Account, Url, CollectionTime, Biz)
                        VALUES ('{}', '{}', '{}', GETDATE(), '{}')""".format(name, account, url, biz)
        print(insert_sql)
        cursor.execute(insert_sql)
        db.commit()
        cursor.close()
        db.close()
        return 'insert successful'


if __name__ == '__main__':
    app.run()
