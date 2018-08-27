import pymysql
from flask import Flask, request

MYSQL_HOST = '120.78.237.213'
MYSQL_PORT = 8002
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'Yunrun2016!@#'
MYSQL_DATABASE = 'urun_statistic'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
    'passwd': MYSQL_PASSWORD,
    'charset': 'utf8',
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()


class EntityTagSite(object):
    def __init__(self):
        self.site_id = ''
        self.tag_code = ''

    def to_dict(self):
        return self.__dict__


app = Flask(__name__)


@app.route('/')
def index():
    cursor.execute('SELECT * FROM tag_site WHERE LENGTH(SignID)>0 AND TagType=2 AND Enabled=1')
    all_tag_site = []
    items = cursor.fetchmany(10)
    for item in items:
        test = EntityTagSite()
        test.site_id = item[15]
        test.tag_code = item[4]
        print(test.to_dict())
        all_tag_site.append(test.to_dict())

    site_id = request.args.get('site_id')
    for tag_site in all_tag_site:
        if site_id == tag_site.get('site_id'):
            return tag_site.get('tag_code')
    return 'not find'


if __name__ == '__main__':
    app.run()
