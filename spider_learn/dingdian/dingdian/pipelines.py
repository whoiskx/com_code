# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from dingdian.items import DingdianItem

MYSQL_DB = 'cpo'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
db = pymysql.connect(user=MYSQL_USER, host=MYSQL_HOST, database=MYSQL_DB, charset='utf8')
cur = db.cursor()


# sql_select = """
#     SELECT * FROM  vendors
#
# """
#
# x = cur.execute(sql_select)
# print(cur.fetchall(), type(cur))
# print(x.fetchall(), type(x))


class Sql(object):

    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        # sql = '''
        #     INSERT INTO dd_name (
        #         `xs_name`, `xs_author`, `category`, `name_id`
        #     )
        #     VAlUES (
        #       ('%(xs_name)s', '%(xs_author)s', '%(category)s', '%(name_id)s')
        #     )
        # '''

        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id,
        }

        sql = '''
            INSERT INTO dd_name (
                xs_name, xs_author, category, name_id
            )
            VAlUES (
              '%s', '%s', '%s', '%s'
            )
        ''' % (value['xs_name'], value['xs_author'], value['category'], value['name_id'])

        cur.execute(sql, value)
        db.commit()

    @classmethod
    def select_name(cls, name_id):
        sql = '''
            SELECT EXISTS (SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)
        '''
        values = {
            'name_id': name_id
        }
        cur.execute(sql, values)
        return cur.fetchall()[0]

class DingdianPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, DingdianItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print('already exist')
            else:
                xs_name = item['name']
                xs_author = item['author']
                category = item['category']
                Sql.insert_dd_name(xs_name, xs_author, category, name_id)
                print('开始存小说标题')

        return item
