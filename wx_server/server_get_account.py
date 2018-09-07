# -*- coding: utf-8 -*-
import pymongo
import time
import redis
from flask import Flask, request
from setting import hash_md5
import json
from handle_artiles import handle
from utils import db


app = Flask(__name__)
error_results = {
    'Success': False,
    'Account': "NF_Dail",
    'Message': "account not found",
    'count': 0,
    'ArtPubInfo': None,
    'ActiveDegree': None,
    'ArtPosNeg': None,
    'KeyWord': None
}


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(host='192.168.1.162', db=8)
        self.queue = 'analyse'

    def listen_task(self):
        while True:
            account_char = self.rcon.blpop(self.queue, 0)[1]
            from analyse_new_media import AccountHttp
            account = AccountHttp()
            account.name = account_char.decode(encoding="utf-8")
            account.run()
            print("Task get", account_char)

    def prodcons(self, account):
        self.rcon.lpush(self.queue, account)
        print("lpush {} -- {}".format(self.queue, account))
        return "ok"


@app.route('/WeiXinArt/AddAccount')
def add_account():
    account = request.args.get('account')
    task = Task()
    task.prodcons(account)
    _id = hash_md5(account + str(int(time.time())))
    db['newMedia'].insert({'id': _id, 'account': account})
    return _id


@app.route('/WeiXinArt/PublishTimes')
def find_account():
    accountid = request.args.get('accountid')
    print('find', accountid)
    item = list(db['newMedia'].find_one({'id': accountid, }))
    # print(list(result))
    if item:
        articles = item[0].get('data')
        r = handle(articles)
        return json.dumps(r)
    else:
        return json.dumps(error_results)


if __name__ == '__main__':
    app.run(port=38015)
