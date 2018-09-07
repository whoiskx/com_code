# -*- coding: utf-8 -*-
import pymongo

import time

import redis
from flask import Flask, request
from setting import hash_md5

conn = pymongo.MongoClient('120.78.237.213', 27017)
db = conn.WeChat


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
            account.run(db)

            print("Task get", account_char)

    def prodcons(self, account):
        self.rcon.lpush(self.queue, account)
        print("lpush {} -- {}".format(self.queue, account))
        return "ok"


app = Flask(__name__)


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
    print("af")
    accountid = request.args.get('accountid')

    result = db['newMedia'].find({'id': accountid, })
    print(list(result))
    articles = result.get('data')

    return 'ok'


def main():
    consumer = Task()
    consumer.listen_task()


if __name__ == '__main__':
    app.run(port=38015)
