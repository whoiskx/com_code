import pymysql
import redis
import time
from scrapy.utils.reqser import request_to_dict, request_from_dict
from scrapy.http import Request
from exts import utils, defaults, picklecompat


# weibo
apiformat = "https://api.weibo.com/2/statuses/user_timeline.json?source=82966982&uid={}&page=1&count=1"

def setup_mysql(**kwargs):
    params = defaults.MYSQL_PARAMS.copy()
    params.update(kwargs)
    # FIXME: pop up mysql_cls
    params.pop('mysql_cls')
    return pymysql.Connection(**params)


def enqueue(requests, redis_server, redis_key):
    for request in requests:
        obj = request_to_dict(request)
        data = picklecompat.dumps(obj)
        score = -request.priority
        redis_server.execute_command('ZADD', redis_key, score, data)
    print("Enqueue %s requests into redis server" % len(requests)) 

def records2requests(records):
    """
    records: mysql returns records
    """
    recordicts = [utils.sql_tuple2dict_with_ftp(record) for record in records]
    for recordict in recordicts:
        url = recordict.pop('url')
        try:
            req = Request(url, meta=recordict, dont_filter=True)
        except Exception as e:
            print(e, url)
        else:
            yield req

def read_mysql(mysql_server, sqls, many=None):
    with mysql_server.cursor() as cursor:
        count = cursor.execute(sqls)
        if many:
            count = many
        ret = cursor.fetchmany(count)
    return ret

def records2requests_weibo(records):
    """
    records: mysql returns records
    """
    recordicts = [utils.sql_weibo_tuple2dict_with_ftp(record) for record in records]
    for recordict in recordicts:
        url = apiformat.format(recordict.pop('uid'))
        yield Request(url, meta=recordict, dont_filter=True)
        
if __name__ == '__main__':
    # setup
    mysql_server = setup_mysql(host='localhost', port=3306, user='', password='', database='info_sct')
    redis_server = redis.StrictRedis()

    while True:
        if not mysql_server.open:
            mysql_server.connect()

        # article
        sqls = utils.sql_query_with_ftp()
        records = read_mysql(mysql_server, sqls, 200)
        print("get %s record from mysql: " % len(records))
        requests = list(records2requests(records))
        enqueue(requests, redis_server, "test:requests")

        # weibo
        sqls_weibo = utils.sql_weibo_with_ftp()
        records = read_mysql(mysql_server, sqls_weibo, 200)
        print("get %s record from mysql: " % len(records))
        requests = list(records2requests_weibo(records))
        enqueue(requests, redis_server, "weibo:requests")

        time.sleep(3600)