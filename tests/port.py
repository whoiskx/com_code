# -*- coding: utf-8 -*-
import json

from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    s = {'Certification': '', 'message': True, 'Feature': '分享你的感受 让我们倾听并给你分析和安慰',
         'ImageUrl': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFtxGA2LtUiwHt4bKeBERtYFI', 'Account': 'yixiaojh',
         'Name': '医者部落 一笑而过笑笑就好', 'status': 1}
    print(s)
    ss = json.dumps(s)
    print(json.loads(ss))
    return ss


if __name__ == '__main__':
    app.run(port=8005)
    # r = requests.get('http://182.245.126.226:21012/WeiXinArt/WeiXinInfo?account=yixiaojh')
    # s = json.loads(r.text)
    # print(s)
