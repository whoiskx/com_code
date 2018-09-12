# -*- coding: utf-8 -*-
import base64
import json
from flask import Flask, request, jsonify
from save_image import ImageSave

app = Flask(__name__)
images = ImageSave()


@app.route('/SaveImage', methods=['POST'])
def hello_world():
    if request.method == 'POST':
        data = request.form
        print(type(data), data)
        content = base64.b64decode(data.get('content'))
        print(type(content))
        account_id = data.get('account_id')
        result = images.images_to_save(account_id, content)
        return jsonify(result)


if __name__ == '__main__':
    app.run(port=1111)
