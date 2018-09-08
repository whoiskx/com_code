# -*- coding: utf-8 -*-
import pymongo
from SougouParseArticle.config import *


class MONGO:
    def __init__(self):
        self.host = MONGO_HOST
        self.port = MONGO_PORT
        self.db = MONGO_DB
        self.collection = MONGO_COLLECTION

        if not self.db:
            raise (NameError, "没有设置数据库信息")
        client = pymongo.MongoClient(host=self.host, port=self.port)
        db = client[self.db]
        self.col = db[self.collection]

    # 添加ArticleId的信息
    def add_ArticleId(self, ArticleId, title, content, timestamp):
        res_num = 0
        for i in self.col.find({'ArticleId': ArticleId}):
            res_num += 1
        if res_num == 0:
            self.col.insert(
                {'ArticleId': ArticleId, 'title': title, 'content': content, 'timestamp': timestamp, 'data': []})
            print('ArticleId:{},插入成功'.format(ArticleId))
        else:
            print('ArticleId:{},该ArticleId已存在'.format(ArticleId))

    # 查询ArticleId的信息
    def find_ArticleId(self, ArticleId):
        new_data = self.col.find_one({'ArticleId': ArticleId})
        result = {
            'title': new_data.get('title'),
            'content': new_data.get('content'),
            'timestamp': new_data.get('timestamp'),
        }
        return result

    # 更新ArticleId的解析数据
    def updata_ArticleId(self, ArticleId, data):
        myquery = {'ArticleId': ArticleId}
        newvalues = {'$set': {'data': data}}
        self.col.update(myquery, newvalues)
        print('ArticleId:{},更新成功'.format(ArticleId))

    # 获取ArticleId的解析数据
    def get_data(self, ArticleId):
        new_data = self.col.find_one({'ArticleId': ArticleId})
        return new_data


mongo_col = MONGO()

if __name__ == '__main__':
    mongo_col.get_data('88b0939c79b17bed9c52a1d1fcd1fefb11111')
