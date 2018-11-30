# -*- coding: utf-8 -*-
import base64
import json

from flask import Flask, request, jsonify, send_file, Response
import os


class ImageRead(object):
    def __init__(self):
        self.BASE_DIR = r'D:\WXSchedule'
        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)

    def images_to_read(self, path):
        image_path = os.path.join(self.BASE_DIR, str(path))
        try:
            with open(image_path, 'rb') as f:
                img_b = f.read()
            img_s = base64.b64encode(img_b)
            return img_s
        except Exception as e:
            return ''


app = Flask(__name__)
images = ImageRead()


@app.route('/ReadImage')
def get_imge():
    return send_file('static/img/logo.png', mimetpe='image/png')

@app.route("/image/<imageid>")
def index(imageid):
    with open('', 'rb') as f:
        resp = Response(f, mimetype="image/jpeg")
    return resp
from flask import render_template, jsonify



if __name__ == '__main__':
    app.run(port=1111)
