# -*- coding: utf-8 -*-

import redis
from flask import Flask, request


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(host='192.168.1.162', db=8)
        self.queue = 'analyse'

    def listen_task(self):
        while True:
            task = self.rcon.blpop(self.queue, 0)[1]
            from articles_info import AccountHttp
            account = AccountHttp()
            account.name = task
            account.run()

            print("Task get", task)

    def prodcons(self, account):
        self.rcon.lpush(self.queue, account)
        print("lpush {} -- {}".format(self.queue, account))
        return "ok"


app = Flask(__name__)

path = '/WeiXinArt/WeixinParse'


@app.route(path)
def get_account():
    account = request.args.get('account')
    task = Task()
    task.prodcons(account)
    return 'ok'


if __name__ == '__main__':
    app.run(port=38015)
