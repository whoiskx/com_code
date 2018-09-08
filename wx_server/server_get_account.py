# -*- coding: utf-8 -*-
import datetime

import pymongo
import time
import redis
from flask import Flask, request
from utils import hash_md5
import json
from handle_artiles import handle
from utils import db, async, hash_md5
from analyse_new_media import AccountHttp

app = Flask(__name__)
error_result = {
    'Success': False,
    'Account': "NF_Dail",
    'Message': "accountid not found",
    'count': 0,
    'ArtPubInfo': None,
    'ActiveDegree': None,
    'ArtPosNeg': None,
    'KeyWord': None
}


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'

    @async
    def listen_task(self):
        while True:
            account_char = self.rcon.blpop(self.queue, 0)[1]
            account = AccountHttp()
            account.name = account_char.decode(encoding="utf-8")
            account.run()
            print("Task get", account_char)

    def prodcons(self, account):
        self.rcon.lpush(self.queue, account)
        print("lpush {} -- {}".format(self.queue, account))


@app.route('/WeiXinArt/AddAccount')
def add_account():
    account = request.args.get('account')
    task = Task()
    task.prodcons(account)
    _id = hash_md5(account)
    add_on = datetime.datetime.now()
    db['newMedia'].update({'id': _id}, {'$set': {'id': _id, 'account': account, 'add_on': add_on}, }, True)
    return _id


@app.route('/WeiXinArt/PublishTimes')
def find_account():
    accountid = request.args.get('accountid')
    print('find', accountid)
    item = db['newMedia'].find_one({'id': accountid, })
    if item:
        result = item.get('data', '未完成')
        return json.dumps(result)
    else:
        return json.dumps(error_result)


if __name__ == '__main__':
    t = Task()
    t.listen_task()
    app.run(port=8009)
