# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
#     return """<html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>账号头像</title>
# </head>
# <body>
# <img {} alt="test"/>
# </body>
# </html>""".format(url_for('static', filename='images/test.jpg'))
    return render_template('index.html')


def return_img_stream(img_stream):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = base64.b64encode(img_stream)
    return img_stream


@app.route('/')
def hello_world():
    img_path = '/home/hogan/Googlelogo.png'
    img_stream = return_img_stream(img_path)
    return render_template('index.html',
                           img_stream=img_stream)


if __name__ == '__main__':
    app.run()
