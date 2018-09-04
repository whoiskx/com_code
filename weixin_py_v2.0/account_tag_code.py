import pymysql
from flask import Flask, request
from config import mysql_tag_code, log


class EntityTagSite(object):
    def __init__(self):
        self.site_id = ''
        self.tag_code = ''

    def to_dict(self):
        return self.__dict__


app = Flask(__name__)
config_mysql = mysql_tag_code()


@app.route('/tag_code')
def index():
    """
    input: site_id
    output: tag_code
    """
    db = pymysql.connect(**config_mysql)
    cursor = db.cursor()
    resp = ''
    try:
        cursor.execute('SELECT TagCode, SignID FROM tag_site WHERE LENGTH(SignID)>0 AND TagType=2 AND Enabled=1')
        items = cursor.fetchall()
        all_tag_site = []
        for item in items:
            test = EntityTagSite()
            test.tag_code = item[0]
            test.site_id = item[1]
            all_tag_site.append(test.to_dict())
        site_id = request.args.get('site_id')
        for tag_site in all_tag_site:
            # 多个tag_site 例如 XHSXHSD
            if site_id == tag_site.get('site_id'):
                resp += tag_site.get('tag_code') + ','
    except Exception as e:
        log(e)
    finally:
        cursor.close()
        db.close()
    return resp[:-1]


if __name__ == '__main__':
    app.run()
