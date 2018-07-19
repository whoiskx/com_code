from flask import jsonify, request, Blueprint
from qq import vlogin

app = Blueprint('QQCaptcha', __name__)

@app.route('/')
def index():
    print("start")

    print(request.args)
    user = request.args.get('user')
    password = request.args.get('password')
    print(user, type(password))
    cookies = vlogin.vlogin_qq(user, password)
    return cookies


