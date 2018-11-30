from flask import Flask

app = Flask(__name__)


@app.route('/<ids>/<ids2>')
def hello_world(ids=1, ids2=None):
    return 'Hello World!{} {}'.format(ids, ids2)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=38014)
