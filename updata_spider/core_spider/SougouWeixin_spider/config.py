# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 文件路径参数配置
# 当前路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 日志文件路径
LOG_PATH = os.path.join(BASE_DIR, 'log.txt')
# 项目文件路径
FILES_DIR = os.path.join(BASE_DIR, 'files')
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
# 项目图片路径
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
# ftp发包存放路径
FTP_DIR = os.path.join(BASE_DIR, 'ftp_files')
if not os.path.exists(FTP_DIR):
    os.makedirs(FTP_DIR)
# ftp发包zip文件路径
ZIPS_DIR = os.path.join(FTP_DIR, 'zips')
if not os.path.exists(ZIPS_DIR):
    os.makedirs(ZIPS_DIR)
# ftp发包xml文件路径
XMLS_DIR = os.path.join(FTP_DIR, 'xmls')
if not os.path.exists(XMLS_DIR):
    os.makedirs(XMLS_DIR)

# 验证码保存名称
CAPTCHA_NAME = 'captcha_0.png'
# 新闻关键词TXT文件完整名称
KEYS_FILE_NAME = 'search_keys.txt'

# 阿布云代理配置
ABUYUN_HOST = "http-dyn.abuyun.com"
ABUYUN_PORT = "9020"
ABUYUN_USER = "HW282117435R626D"
ABUYUN_PASS = "73E6ADCC5C073EC4"

# 打码平台参数配置
# 接口URL
DYTRY_APIURL = 'http://api.dytry.com/ocr.json'
# 用户名
DYTRY_USERNAME = 'uruntest'
# 用户密码
DYTRY_PASSWORD = '0763!@#'
# 题目类型
DYTRY_TYPEID = 9999
# 软件ID
DYTRY_SOFTID = 1107
# 软件KEY
DYTRY_SOFTKEY = '34af19d2ee35e938dbbdc0336eb730cb'

# SQL server参数配置
# SQL server ip端口
SQL_SERVER_HOST = '183.131.241.60:38019'
# SQL server 用户名
SQL_SERVER_USER = 'oofraBnimdA_gz'
# SQL server 密码
SQL_SERVER_PWD = 'fo(25R@A!@8a823#@%'
# SQL server 数据库  微信
SQL_SERVER_DB = 'Winxin'

# FTP server参数配置
# 河北省委电信—主
FTP_HB_TELECOM = {
    'host': '123.182.246.209',
    'port': 21,
    'user': 'dc5',
    'pwd': 'qwer$#@!',
}
# 河北省委联通—备
FTP_HB_UNICOM = {
    'host': '110.249.163.246',
    'port': 21,
    'user': 'dc5',
    'pwd': 'qwer$#@!',
}
# 杭州兴议集群
FTP_HZ_list = [
    {
        'name': '杭州兴议111',
        'FTP_HZ_main': {
            'host': '122.224.105.171',
            'port': 21,
            'user': 'dc5',
            'pwd': 'qwer$#@!',
        },
        'FTP_HZ_backup1': {
            'host': '124.239.144.181',
            'port': 21,
            'user': 'dc15',
            'pwd': 'qwer$#@!',
        },
        'FTP_HZ_backup2': {
            'host': '121.28.84.254',
            'port': 21,
            'user': 'dc15',
            'pwd': 'qwer$#@!',
        }
    },
    {
        'name': '杭州兴议136',
        'FTP_HZ_main': {
            'host': '122.224.105.174',
            'port': 21,
            'user': 'dc5',
            'pwd': 'qwer$#@!',
        },
        'FTP_HZ_backup1': {
            'host': '124.239.144.181',
            'port': 21,
            'user': 'dc45',
            'pwd': 'qwer$#@!',
        },
        'FTP_HZ_backup2': {
            'host': '121.28.84.254',
            'port': 21,
            'user': 'dc45',
            'pwd': 'qwer$#@!',
        }
    },
]

# 接口参数配置
# 搜狗验证码识别接口
# 主：河北164：23317
GetCaptcha_URL_main = 'http://124.239.144.164:7101/GetCaptcha'
# 备用：广外204：38012
GetCaptcha_URL_backup = 'http://183.238.76.204:38015/GetCaptcha'

# 获取AccountID接口
GetAccountId_URL = 'http://60.190.238.178:38010/search/common/wxaccount/select'
GetAccountId_TOKEN = '9ef358ed-b766-4eb3-8fde-a0ccf84659db'
# 获取AccountID接口2
GetAccountId_URL2 = 'http://183.131.241.60:38011/MatchAccount'

# 微信判重（获取url）接口：主接口
GetCacheWx_URL_main = 'http://47.100.53.87:8008/Schedule/GetCacheWx'
# 微信判重（获取url）接口： 备用接口
GetCacheWx_URL_backup = 'http://183.238.76.203:38015/Schedule/GetCacheWx'

# 微信判重（添加url）接口：主接口
CacheWx_URL_main = 'http://47.100.53.87:8008/Schedule/CacheWx'
# 微信判重（添加url）接口： 备用接口
CacheWx_URL_backup = 'http://183.238.76.203:38015/Schedule/CacheWx'

# 新版任务调度接口
ScheduleDispatch_URL = 'http://dispatch.yunrunyuqing.com:38082/ScheduleDispatch/dispatch?type=5'

# 发包接口
# 1.普通采集  2.元搜索
SOURCENODES = 2
# 1.文章  2.微信  3.微博
SOURCETYPE = 2
# 微信底层两个接口
SEND_URL_1 = 'http://115.231.251.252:26016'
SEND_URL_2 = 'http://60.190.238.168:38015'
# 三合一底层接口
SEND_URL_3 = 'http://222.184.225.246:8171'
# 数据中心转发接口
SEND_URL_datacenter_main = 'http://27.17.18.131:38072'
# 长啥备用转发接口
SEND_URL_datacenter_backup = 'http://119.39.84.12:7104'

# 本地XML和ZIP数量最大保存数量，超过则清空：50
MAX_XML_NUM = 50

# 开关参数配置
# 运行线程数
THREAD_NUM = 3
# 识别验证码方法：1：打码平台，2：验证码识别接口
GETCAPTCHA_TYPE = 2
# 采集时间范围：1：任务补采版本，2：日常采集
DEMO_TYPE = 2
# 关键词获取：1：补采txt，2：任务调度
TXT_ENABLED = 2

# 是否启用阿布云代理
ABUYUN_ENABLED = True
# 是否处理验证码
CAPTCHA_ENABLED = True
# 公众号增源
SOURCE_ADD_ENABLED = True
# 判重
SENTENCED_ENABLED = True
# 发包
SEND_PACKAGE_ENABLED = True


class Logger(object):
    def __init__(self):
        # 初始化日志模块
        self.logger = logging.getLogger('sougouweixin_spider')
        self.logger.setLevel(logging.INFO)
        # 输出的日志文件名
        fmt = logging.Formatter("%(asctime)s - %(levelname)-8s: %(message)s")
        # 保存最近五天的日志
        hdlr = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='midnight', interval=1, backupCount=3,
                                                         encoding='utf-8')
        hdlr.setFormatter(fmt)
        self.logger.addHandler(hdlr)

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()

# UA池
UA_POOL = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
    'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like ',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-ch) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.8.36217; WOW64; en-US)',
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
    'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
    'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01',
    'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; ',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; .NET CLR 2.7.58687; SLCC2; Media Center PC 5.0; Zune 3.4; Tablet PC 3.6; ',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
    'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01',
    'Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
]
