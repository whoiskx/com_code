""" defaults settings
used by
-------
connection.py 
dupefilter.py
pipelines.py

functions
---------
1. dupefilter_key
2. pipeline_key
3. redis settings
4. scheduler settings
5. start_urls settings
"""

import redis
import pymysql

# For standalone use.
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

PIPELINE_KEY = '%(spider)s:items'

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}

# Mysql settings
MYSQL_CLS = pymysql.Connection
MYSQL_ENCODING = 'utf8'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = None
MYSQL_PASSWORD = None
MYSQL_DATABASE = None
MYSQL_PARAMS = {
    'mysql_cls': MYSQL_CLS,
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE, 
    'charset': MYSQL_ENCODING,
}
# FIXME: still not support
MYSQL_BATCH_SIZE = 1000


SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'exts.queue.PriorityQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'exts.dupefilter.RFPDupeFilter'

START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False
