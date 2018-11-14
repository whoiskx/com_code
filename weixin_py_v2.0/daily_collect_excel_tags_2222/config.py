# -*- coding: utf-8 -*-
import pymongo
import time

import pymysql

# 搜狗验证码识别url
GETCAPTCHA_URL = 'http://124.239.144.164:7101/GetCaptcha'
# 主：河北164：23317
GETCAPTCHA_URL_MAIN = 'http://124.239.144.164:7101/GetCaptcha'
# 备用：广外204：38012
GETCAPTCHA_URL_BACKUP = 'http://183.238.76.204:38015/GetCaptcha'

# 补采
# ['bdb1937', 'dgshs2018', 'pd0351', 'guyuanxuanjiang', 'dgrb789']
ADD_COLLECTION = ['gmrb1949', 'tianxiayan2015', 'yuedugongshe', 'liuxuezazhi', 'zhreading', 'guangmingjiangtan',
                  'gmweijiaoyu', 'gmwhcy', 'gmyygs', 'wenzhaibao', 'GM_WenYi', 'dongdajiefive', 'gm_GMAD',
                  'guangmingzhiku', 'gmw_001', 'wangxindangjian', 'kejimingjia', 'Military2016', 'ourcecn', 'ssqs_2016',
                  'koudaijr', 'zbpafda', 'wocaijing11', 'zgjcgycbs', 'zgfzb1986', 'ZG-xyjj', 'ncjrnews', 'smecei',
                  'o2olink', 'VIEW-CBMD', 'jingjizazhi', 'JJZZSLSH', 'jjrbwx', 'cewenhua', 'autocecn', 'fzsbwx',
                  'edpbook_com_cn', 'ceinews', 'smecei', 'cfw-com-cn', 'iceo-com-cn', 'cfnnews', 'flower_floraltime',
                  'chuangyidasai', 'qstheory_001', 'WDANGS', 'XEshixi', 'qiushimp', 'qiushisjb', 'hongqiwengao',
                  'gh_affeebf9ba89', 'CCTV-channel1', 'cctvjrsf ', 'cctvdzw', 'cctvshzck2013', 'CCTV1kaijiangla',
                  'cctvtzbkn', 'CCTV-1leyuan', 'cctvjyxwl', 'cctvxilejie', 'ijiaiwei', 'cctvddc', 'cctv-duihua',
                  'cctv2-XFZZ', 'cctvyscj', 'cctvjysj', 'cctvdysj', 'cctvfh', 'cctvjjyflm', 'cctv-yirenyishijie',
                  'cctv_cj_gl', 'Weareyoung_66', 'cctv2jingxilianlian', 'cctv2pinglun', 'cctv2_cyyxh', 'CWZB_88',
                  'gh_22c6191afa20', 'cctv2sz', 'cctvcbn520', 'CCTVyangshizongyi', 'huangjin100s', 'cctvyzyy',
                  'woaimantangcai', 'cctvwdsj', 'WYSCW_CCTV', 'cctvxxfcf', 'staroad', 'gh_665917744409', 'Cctvhsll',
                  'cctv3wenhuashidian', 'cctvkmdj', 'cctvyilantianxia', 'zongyishengdian', 'CCTV-YSRS', 'cctvqitianle',
                  'yangshifeichang6jia1', 'cctvhuanlexiu', 'gh_530ced15e899', 'gh_06ab3b8bb060', 'CCTV4gbdawx',
                  'cctvkuailehanyu', 'jinriyazhou', 'cctvjrgz', 'cctvyfdj', 'shenduguoji2015', 'cctvzhyy',
                  'CCTV-wgrzzg', 'cctv_zhonghuaqing', 'cctvzgxw', 'cctvcsydy', 'cctv4zgwy', 'cctvhrsj',
                  'gh_28533671d357', 'CCTV-4ZBZG', 'cctv4lxwx', 'T2905956623', 'zhitongtaiwan', 'gh_e80a6b8d2dad',
                  'shijietingwoshuo', 'CCTV-5sportnews', 'jianshendongqilai', 'cctv5hoopark', 'saicheshidai',
                  'shuishiqiuwang', 'cctvxiaojizhe', 'cctv5tiyukaba', 'InteractiveNBA', 'cctvjunshijishi', 'cctvjlrs',
                  'fangwuxgc', 'junmittx', 'junyingdawutai ', 'CAPFnet ', 'cctv7woaiguofang', 'jfjjs7tv', 'cctv7sszjyx',
                  'CCTV-7_Junshi', 'jlwhdsy7', 'cctv7bzjd', 'CCTVygdd', 'CCTV7mlzgxcx', 'cctv-7fazhibianjibu',
                  'A94897456', 'CCTV_MRNJ', 'cctvkjy', 'jujiaosannong', 'xiangcundashijie', 'nongtv', 'nongye7',
                  'cctv7ssdzp', 'xiangyuecctv', 'cctv7xiangtu', 'ntvzaobao', 'cctveight', 'cctvxtj', 'cctv9jilupindao',
                  'cctv1cha', 'cctv-zoujinkexue', 'cctvylrc', 'cctvbaijiajiangtan', 'cctvdushu', 'cctv10_kejiao',
                  'storyboxes', 'cctv10-tansuofaxian', 'fammgc', 'wenmingmima', 'cctv-dajia', 'gh_c3e024997eda',
                  'cctvgby', 'CCTVCSZY', 'cctvpflmj', 'CCTV12pingan365', 'cctvrexian12', 'CCTV_xinlifangtan',
                  'gh_42f7a3741bc3', 'shequyingxiong', 'cctvyixian', 'CCTVFLJT', 'daodeguancha-cctv12', 'cctvchanhuilu',
                  'cctv12xqds', 'yangshitianwang', 'cctvnewscenter', 'cctv_newsweekly', 'xinwendiaochacctv',
                  'xinwenyijiayi', 'jdftcctv', 'cctvgdzg', 'cctv_worldweekly', 'cctv14guonianla', 'cctvxwddk', 'zmxxsn',
                  'gh_4dfff955d985', 'cctvyykd', 'jssn3031', 'CCTV-Children', 'zuiyejiaqi', 'cctv15music2013',
                  'CCTVyiqiyinyueba', 'GlobalChineseMusic', 'cctv-gsywx', 'CCTV_HMYY', 'gh_054ec888a67a', 'cctvfhgy',
                  'CCTV_News_Content', 'gh_06d1dea1491a', 'CCTV-FRANCAIS', 'CCTV-Arabic', 'CCTVADAD', 'cctvgygg',
                  'cctvkandian', 'cctv-vc', 'cctvcomweixin', 'yswshangcheng', 'cntvweixin', 'CNTV-CBox', 'cctv-wlcw',
                  'ipandacom', 'CNTVsports', 'cctvyuedong', 'mongolcntv', 'CNTV_UYGHUR', 'cntv_kazakh',
                  'wangluoxinwenlianbo', 'tushuojzg', 'zchhdhc', 'cctvwish', 'cctv315', 'cctvhjcf',
                  'PhotoWorldMagazine', 'xinhuashefabu1', 'XHSXHSD', 'wobaodao', 'xinhuafoto', 'xinhuapub1979',
                  'zgjzzzs', 'xhszzb', 'lwdflwdf', 'shzqbwx', 'OutlookWeekly1981', 'www_cnstock_com', 'zhczyj',
                  'jjckb-wx', 'nbxdjb', 'xinhuaafrica', 'NX7913', 'newsxinhua', 'sikexh', 'kjcxlcb', 'kjqydst',
                  'kxylydt01', 'jskjqy', 'XMTV-AUTO', 'xinhuaonline_bj', 'xinhuahebei', 'xhwjxpd', 'xhwscxsj',
                  'onncc626', 'xinhuakehuan', 'wjqnxh', 'xinhuashipin', 'xinhuajk', 'xhw-ysc', 'xinhuahouse_nj',
                  'shanxi_toutiao', 'interxinhua', 'bjcankao', 'Chinatopbrands', 'ckxxwx', 'caiguo08', 'GlobeMagazine',
                  'banyuetan-weixin', 'gjxqdb', 'ahxinhuashe', 'chuangke_xinhua', 'kpzgcbzd', 'xh-energy', 'cqhjsx',
                  'gd7744', 'chihuochuangjian', 'bjxuanwen', 'RealTimeChina', 'CHINADAILYWX', 'NEWSPlus', 'cibn123',
                  'duanchun-shuo', 'crihuanqiujunshi', 'hitfmcri', 'gh_c92bcbfd9b97', 'cribbr', 'gh_7e86f2af1dc1',
                  'huanqiuruiping', 'bzbkcri', 'CRI-russian', 'zxfcdcri', 'crionline', 'CRIjpn', 'cridanganjiemi',
                  'RADIOEZFM', 'ezfmmotianlun', 'Radio_cri', 'fm9050', 'sportstalk', 'cri_lao', 'crihqmrf',
                  'criturkish', 'CRIfrench', 'CRI_ESP', 'gh_1ae6140d3b1a', 'laowaikandian', 'cri_indonesia', 'cripor',
                  'gh_d52089dd3ee7', 'myanmar_online', 'hqjy905', 'Mabuhay_CRI', 'cripersian', 'khmerccfr',
                  'watchasean', 'jiluzhemiyaniu', 'crient', 'crinanhai', 'CRI_Nepal', 'CRIzwhq', 'CRIgreek', 'crithai',
                  'Hrvatska1', 'itaiwannews', 'CRI-Poland', 'cri_malay', 'shiliuhaoxinxi', 'Balkanrose',
                  'Delhiin-tsag_2016', 'WORLDWIDECHINESE', 'srilankacri', 'HQQG--CRI', 'zgzs001', 'jjzswx',
                  'musicradio2002?', 'dszs001?', 'wenyi1066?', 'zgxczs720?', 'lnzsam1053?', 'CNEB_CNR?', 'cnr_cnr?',
                  'cnrjunshi', 'zggbzz?', 'xinwenzongheng?', 'jjzsjysk?', 'jyskjlb?', 'CNRTXCJ?', 'wangguan201508?',
                  'lnzsam1053', 'CNS1952', 'cns2012', 'qiaowangzhongguo', 'OverseasChinese_CNS', 'cnsgs-01', 'CNS-SD',
                  'CNS-gd', 'CNS-chaoshan', 'cns-jl', 'siluxgc', 'cns-xj', 'cns-bt', 'cnshebei', 'hubeicns', 'cns_sn',
                  'zhangzhongjiangsu', 'jstvjsxw', 'cnssx0351', 'cns-gx', 'zzxgzwx', 'cns0898', 'sldhslm', 'cns-hlj',
                  'hunanhaowan', 'cns_ln', 'cnsyn-01', 'shiyunnan01', 'CNSxywc', 'qinghaiyys', 'sfscns',
                  'chinanewsweekly', 'chinanews-shanghai', 'gannews', 'cnscqttnews', 'rmrbzbs', 'rmrb_2b',
                  'rmrbqiuzheng', 'rmrbwy', 'dadifukan', 'rmdushu', 'rmwenyuan', 'wenyipl', 'rmrbmssc', 'rmrbpl',
                  'rmrbllb', 'rmrbty', 'rmrbyjb', 'rmrb_hww', 'xiake_island', 'xuexixiaozu', 'peopledigital', 'hqsbwx',
                  'huanqiu-com', 'America_hq', 'huanqiuouzhou123', 'huanqiukorea', 'huanqiutaiwan', 'zhongguoqichebao',
                  'qichezaocan', 'wwwstcncom', 'quanshangcn', 'lianhuacaijingcom', 'zqsbxsb', 'shujubao2015',
                  'chuangyzbh', 'trustway', 'zqsb_cfzx', 'gongsiyuqing', 'Betainvest', 'jksb2013', 'jkzg-nhfpc',
                  'jksb2016', 'gh_abf70cc555e4', 'rmltwz', 'globalpeople2006', 'rmrbpaxy', 'ChinaEconomicWeekly',
                  'msweekly', 'gjrwls', 'peoplevision', 'quan_yue001', 'guolishuhua', 'baidaitrip', 'cnenergy',
                  'depo88', 'guojinengyuancankao', 'dabaxinwen', 'energyinternetclub', 'GlobalTimesNews',
                  'gh_81dcf95743f9', 'gtmetroshanghai', 'LT0385', 'yaonidongwx', 'duxinyanjiusuo', 'tiantianfachi',
                  'muyingribao', 'yansutanxing', 'fcyymwx', 'gjjrb777', 'gh_a1185130b3be', 'chinafundnews', 'Money-Lcq',
                  'sanbanfuweixin', 'qhrb168', 'rmwz365', 'gh_2e81f20bd4d6', 'zhongguochengshibao', 'gh_0c422b3ac3e0',
                  'qichezuweixin', 'qicheyuyundong', 'china_engine', 'jiayongqiche', 'qichepiping', 'zgcsgdjtxh',
                  'ev-qiche', 'canfans_news', 'WDCHN-NES', 'rmrbqmtpt', 'xxdaguo', 'wxpdmi', 'people_rmw', 'cpcnews',
                  'rmwjkpd', 'rmwshipin', 'qglt19990509', 'jxnihao', 'rmhuanbao', 'finance_people', 'renminyx',
                  'rmrbwx', 'rmrbbj', 'baidaitrip', 'gjjrb777', 'rmrbjjsh']
# 直接从数据库拿账号
GET_ACCOUNT_FROM_MYSQL = False


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


# 新调度库
def get_mysql_new():
    """save data"""
    mysql_host = '121.28.84.254'
    mysql_port = 7101
    mysql_user = 'yunrun'
    mysql_password = 'YunRun2018!@#'
    mysql_database = 'test'

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
    config_sql = localhost_mysql()
    db = pymysql.connect(**config_sql)
    cursor = db.cursor()
    # cursor.execute(sql, _tuple)
    # db.commit()
    cursor.close()
    db.close()
