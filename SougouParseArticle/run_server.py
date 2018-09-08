# -*- coding: utf-8 -*-
import redis
import hashlib
import requests
from flask import Flask, request, jsonify
from threading import Thread
from SougouParseArticle.config import *
from SougouParseArticle.mongo_util import mongo_col
from SougouParseArticle.sougou_parser_title import SougouWexin


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(host=REDIS_HOST, db=REDIS_DB)
        self.queue = REDIS_QUEUE

    @async
    def listen_task(self):
        while True:
            ArticleId = self.rcon.brpop(self.queue, 0)[1]
            if len(ArticleId):
                print("blpop {}:{}".format(self.queue, ArticleId))
                requests.post('http://127.0.0.1:8012/WeiXinArt/SingleParse', data={'ArticleId': ArticleId})
                print('ArticleId ok', ArticleId)

    def prodcons(self, ArticleId):
        self.rcon.lpush(self.queue, ArticleId)
        print("lpush {}:{}".format(self.queue, ArticleId))
        print('ArticleId add', ArticleId)


app = Flask(__name__)


@app.route('/WeiXinArt/GetArticleId', methods=['POST'])
def GetArticleId():
    if request.method == 'POST':
        # 参数：文章标题，内容，发文时间戳
        data = request.json
        print(type(data), data)
        title = data.get('title')
        content = data.get('content')
        timestamp = data.get('timestamp')
        if title and timestamp:
            title_timestamp = title + str(timestamp)
            h1 = hashlib.md5()
            h1.update(title_timestamp.encode(encoding='utf-8'))
            md5_key = h1.hexdigest()
            # 添加ArticleId相关信息到mongodb
            mongo_col.add_ArticleId(ArticleId=md5_key, title=title, content=content, timestamp=timestamp)
            # 添加到redis队列
            task = Task()
            task.prodcons(ArticleId=md5_key)
            return jsonify({'ArticleId': md5_key, 'Success': True, 'Message': ''})
        else:
            return jsonify({'ArticleId': '', 'Success': False, 'Message': 'title和timestamp不能为空'})


@app.route('/WeiXinArt/SingleParse', methods=['POST', 'GET'])
def ParseTitle():
    if request.method == 'POST':
        # 参数：标题时间戳md5值
        ArticleId = request.form.get('ArticleId')
        if ArticleId:
            data = mongo_col.find_ArticleId(ArticleId)
            if data.get('title') and int(data.get('timestamp')):
                new_data = {
                    'title': data.get('title'),
                    'content': data.get('content'),
                    'timestamp': int(data.get('timestamp')),
                }
                result = SougouWexin(new_data).run()
                mongo_col.updata_ArticleId(ArticleId=ArticleId, data=result)
                # 给前端返回完成状态:3分析成功
                params = {
                    'type': 4,
                    'analysisId': ArticleId,
                    'status': 3,
                }
                # requests.get(STATUS_API_URL, params=params)
                return jsonify(result)
            else:
                return jsonify({'ArticleId': ArticleId, 'Success': False, 'Message': '该ArticleId的标题或时间戳为空'})
        else:
            return jsonify({'ArticleId': ArticleId, 'Success': False, 'Message': 'ArticleId不能为空'})
    elif request.method == 'GET':
        # 参数：标题时间戳md5值
        ArticleId = request.args.get('ArticleId')
        result = mongo_col.get_data(ArticleId=ArticleId)
        if result:
            data = result['data']
            return jsonify(data)
        else:
            # 给前端返回未完成状态:4分析失败
            params = {
                'type': 4,
                'analysisId': ArticleId,
                'status': 4,
            }
            # requests.get(STATUS_API_URL, params=params)
            return jsonify({'ArticleId': ArticleId, 'Success': False, 'Message': '没有该ArticleId'})


if __name__ == '__main__':
    # 实时监听redis队列进行分析
    Task().listen_task()
    # 开启服务,linux内网端口：8005，外网端口：8012
    app.run(port=8012, debug=True)
