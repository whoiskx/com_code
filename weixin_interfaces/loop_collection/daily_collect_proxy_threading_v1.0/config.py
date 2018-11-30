# -*- coding: utf-8 -*-
import pymongo
import time

import pymysql


# 新调度库
def get_mysql_new():
    """save data"""
    mysql_host = '121.28.84.254'
    mysql_port = 7101
    mysql_user = 'yunrun'
    mysql_password = 'YunRun2018!@#'
    mysql_database = 'info_src'

    config_mysql = {
        'host': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        'passwd': mysql_password,
        'db': mysql_database,
        'charset': 'utf8',
        'connect_timeout': 15,
    }
    return config_mysql


def get_account_form_weixin():
    _db = pymysql.connect(**get_mysql_new())
    _cursor = _db.cursor()
    sql = """
        SELECT * FROM weixin WHERE pause=0 LIMIT 7000;
    """
    _cursor.execute(sql)
    data = _cursor.fetchall()
    account_list = []
    for account_info in data:
        account_list.append(account_info[2])
    return account_list


# 搜狗验证码识别url
GETCAPTCHA_URL = 'http://124.239.144.164:7101/GetCaptcha'
# 主：河北164：23317
GETCAPTCHA_URL_MAIN = 'http://124.239.144.164:7101/GetCaptcha'
# 备用：广外204：38012
GETCAPTCHA_URL_BACKUP = 'http://183.238.76.204:38015/GetCaptcha'

# 补采
# ['bdb1937', 'dgshs2018', 'pd0351', 'guyuanxuanjiang', 'dgrb789']
ADD_COLLECTION = ['Shantou4', 'chenhzxiang', 'kxtiandi', 'chenghaiqushi', 'CH-NEW', 'csjc_LC', 'batoubbs', 'CTQAOE',
                  'cdzzpwvip', 'cdwbvip', 'cwp348', 'cyzb0754', 'XCTong888', 'cyshw1688', 'cy515100', 'CYJZZXFW93',
                  'CYHXSHQ', 'youlidszx', 'GD-CSQ', 'chao6666shan', 'CS-LTT', 'gh_191e435814b0', 'pacn0754', 'cnxs8888',
                  'cnwsqw168', 'chaonantai', 'LGTV0754', 'stcnlm', 'cncy8888', 'chaoshan889', 'xilu2015',
                  'gh_2198f77baaec', 'Guraowang', 'GURAOLL', 'ugurao', 'GuRaoZiXunPingTai', 'uguiyu', 'HJFY007',
                  'dahao515071', 'HPQ6699', 'jiazcs', 'jinrixilu', 'jinzaoshiyixiang', 'smg0754', 'LYR-01',
                  'hjshq515071', 'love-st0754', 'stjinri', 'STweidao', 'tpshdq', 'ituopu', 'waisharen_weixin',
                  'woaichendian', 'xiluw1688', 'xs87778', 'xiashanDA', 'xx360net', 'yanhongshenghuo', 'yxsh0796',
                  'CNlugang', 'CNsimapu', 'tuopuu', 'STCHGA', 'cyxcfb', 'STCN_CNZX', 'haojiangxuanchuan', 'stshjq',
                  'st-longhu', 'wsdzb0754', 'stslhwm', 'gh_aa29a1a37296', 'naxgqt', 'WMShanTou', 'stchedu', 'stfzjz',
                  'stsrmjcy', 'stlhgafj', 'shantouyouth', 'shantourenshe', 'chqyjb', 'stszfyjb', 'l3646631',
                  'gh_946ba171c4f6', 'gh_eb04bcbf5738', 'stchwst', 'chrchs', 'chrm0754', 'cdxchenghai', 'cd7222',
                  'cyq0754', 'cy-bbs', 'csrm111', 'hbcs99', 'jrch20150601', 'guiyuweishenghuo', 'J-599999', 'CH-BST',
                  'www_hepan_com', 'weinanao114', 'stucaogenbobao', 'gh_f7c73e058c77', 'edaynew', 'shantoubang',
                  'gh_53f4bbb8d2db', 'stdsbxw', 'stganlantai', 'stgz0754', 'minshengdangan', 'strm0754', 'st-daily',
                  'sttqwb', 'sttvnews', 'STYiXian', 'ssst201509', 'mldl257', 'wzshantou', 'wmch0754', 'zmcqds',
                  'loveinswatow', 'ASHM0754', 'hepannews', 'csbolan', 'DOU754', 'chyx200', 'ddzxdy', 'chwl0754',
                  'chbtsx', 'chenghaiyibai', 'CDWBPT0754', 'cyzx515100', 'cyrm0754', 'cyjz1688', 'cyhx0754',
                  'haimen0754', 'cygb0754', 'cswhyjy', 'cyjp0754', 'cscstv', 'css_sty', 'jzg516538', 'csr540',
                  'ischaoshan', 'cnshq0754', 'chaonanquan', 'gd_st001', 'guraochihuo', 'guraoquan', 'guanbu000',
                  'guiyushequ', 'GYSL88', 'gywsh0813', 'hepu515098', 'LJCS5533', 'huodongcheng520', 'jinrichaoyang',
                  'jujiao0754', 'gh_bd00c5c8bd05', 'nanaobest', 'nadqgw', 'naha868', 'stnanaoly', 'Nanao_SC', 'nihaost',
                  'cohere', 'quanqiugurao', 'chi0754', 'is0754', 'shantoudxs', 'stualumni', 'stu_news', 'shantouzx',
                  'stouquan', 'HOT0754', 'stlives', 'stshjz', 'stshiwan', 'shantouqiaolian', 'hey0754', 'ST07542016',
                  'cycy0754', 'shendu0754', 'sdst0754', 'cccsp1017', 'tongyuzx', 'wanbaoshantou', 'women0754',
                  'xilu-ren', 'xiluw515163', 'XSweishenghuo888', 'ultraplus_cross', 'xianhua-3']

# 补采方式 二 从数据库获取账号
# ADD_COLLECTION = get_account_form_weixin()

# 直接从数据库拿账号
GET_ACCOUNT_FROM_MYSQL = False
# 判重
JUDEG = True
# 使用代理
USE_PROXY = True

# 线程数
TREAD_COUNT = 1
# 进程数
PROCESS_COUNT = 1


def mysql_tag_code():
    # 接口 site_id -> tag_code
    mysql_host = '120.78.237.213'
    mysql_port = 8002
    mysql_user = 'yunrun'
    mysql_password = 'Yunrun2016!@#'
    mysql_database = 'urun_statistic'

    config_mysql = {
        'host': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        'db': mysql_database,
        'passwd': mysql_password,
        'charset': 'utf8',
    }
    return config_mysql


# 微信旧库
def get_mysql_old():
    mysql_host = '183.131.241.60'
    mysql_port = 38019
    mysql_user = 'oofraBnimdA_gz'
    mysql_password = 'fo(25R@A!@8a823#@%'
    mysql_database = 'Winxin'

    config_mysql = {
        'server': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        'database': mysql_database,
        'password': mysql_password,
        'charset': 'utf8',
        'connect_timeout': 10
    }
    return config_mysql


def localhost_mysql():
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_database = 'comm'

    config_mysql = {
        'host': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        # 'passwd': mysql_password,
        'db': mysql_database,
        'charset': 'utf8',
        'connect_timeout': 10,
    }
    return config_mysql


def mongo_conn():
    conn = pymongo.MongoClient('120.78.237.213', 27017)
    _db = conn.account_count
    return _db


if __name__ == '__main__':
    # config_sql = localhost_mysql()
    # db = pymysql.connect(**config_sql)
    # cursor = db.cursor()
    # # cursor.execute(sql, _tuple)
    # # db.commit()
    # cursor.close()
    # db.close()
    print(get_account_form_weixin())
