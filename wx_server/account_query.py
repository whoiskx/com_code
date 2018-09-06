# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify

app = Flask(__name__)

path = '/WeiXinArt/PublishTimes'


@app.route(path)
def find_account():
    if request.method == 'GET':
        query = request.args.get('account')
        print(query)

    results = {
        'Success': True,
        'Account': "NF_Daily", }
    return jsonify(results)


if __name__ == '__main__':
    app.run(port=38015)
