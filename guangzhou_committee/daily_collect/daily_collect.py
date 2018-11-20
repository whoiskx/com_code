# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
import time

import requests
import json

from lxml import etree

from pyquery import PyQuery as pq
from models import JsonEntity, Article, Account, Backpack, Ftp
from config import get_mysql_new, GETCAPTCHA_URL, mongo_conn, ADD_COLLECTION, GET_ACCOUNT_FROM_MYSQL, JUDEG
from utils import uploads_mysql, get_log, driver, get_captcha_path, time_strftime, save_name

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
from verification_code import captch_upload_image

current_dir = os.getcwd()
log = get_log('daily_collect')


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = ''
        self.search_name = ''
        self.tags = ''
        self.s = requests.Session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.106 Safari/537.36',
        }
        self.cookies = {'SUID': '4A72170E2613910A000000005BAC759D', 'ABTEST': '3|1538028956|v1', 'SUIR': '1538028956',
                        'IPLOC': 'CN4401', 'SNUID': '5960051C121665C656C04D9E13C88607',
                        'PHPSESSID': '80l6acdo9sq3uj357t00heqpg1', 'seccodeRight': 'success',
                        'SUV': '00F347B50E17724A5BAC759DBEFB6849', 'successCount': '1|Thu, 27 Sep 2018 06:20:59 GMT',
                        'refresh': '1', 'JSESSIONID': 'aaa73Xexaf2BmgEL80Bvw'}
        self.driver = driver
        self.driver.set_page_load_timeout(15)
        self.driver.set_script_timeout(15)
        self.wait = WebDriverWait(self.driver, 5)

    def account_homepage(self):
        # 搜索账号并返回公众号主页
        count = 0
        while True:
            count += 1
            if count > 3:
                log.info('多次账号异常，跳过账号:'.format(self.name))
                return
            log.info('start account {}'.format(self.search_name))
            search_url = self.url.format(self.search_name)
            resp_search = self.s.get(search_url, headers=self.headers, cookies=self.cookies)
            e = pq(resp_search.text)
            log.info('当前搜狗标题：{}'.format(e('title').text()))
            if '搜狗' not in e('title').text():
                log.info('初始化session')
                self.s = requests.session()
            if self.search_name == e(".info").eq(0).text().replace('微信号：', ''):
                account_link = e(".tit").find('a').attr('href')
                self.name = e(".tit").eq(0).text()
                homepage = self.s.get(account_link, cookies=self.cookies)
                if '<title>请输入验证码 </title>' in homepage.text:
                    self.crack_sougou(account_link)
                    homepage = self.s.get(account_link, cookies=self.cookies)
                return homepage.text
            elif len(e(".tit").eq(0).text()) > 1:
                log.info("不能匹配正确的公众号: {}".format(self.search_name))
                return
            if '相关的官方认证订阅号' in resp_search.text:
                log.info("找不到该公众号: {}".format(self.search_name))
                return
            if '搜狗' in e('title').text():
                log.info('{} :搜索结果无文字'.format(self.search_name))
                return
            else:
                # 处理验证码
                log.info(search_url)
                log.info('验证之前的cookie'.format(self.cookies))
                try_count = 0
                while True:
                    try_count += 1
                    self.crack_sougou(search_url)
                    if '搜公众号' in self.driver.page_source:
                        log.info('------开始更新cookies------')
                        cookies = self.driver.get_cookies()
                        new_cookie = {}
                        for items in cookies:
                            new_cookie[items.get('name')] = items.get('value')
                        self.cookies = new_cookie
                        log.info('------cookies已更新------'.format(self.cookies))
                        break
                    elif try_count > 4:
                        log.info("浏览器验证失败")
                        break
                log.info("验证完毕")
                time.sleep(2)
                continue

    @staticmethod
    def get_account():
        # try:
        #     url = 'http://10.194.12.106:8002/GetWeixinTask?name=&name_array=&Name_word=&channel=&pageno=1&pagesize=12&local=False&token=082c5e82-a168-4c2e-a8e6-00760225c93a_wechat&page=1&rows=12&sort='
        #     resp = requests.get(url, timeout=30)
        #     data = json.loads(resp.text).get('weixin')
        #     account_list = []
        #     for account_info in data:
        #         account_list.append(account_info.get('account'))
        #     return account_list
        # except Exception as e:
        #     log.info(e)
        # return ['rmrb_2b', 'rmrbqiuzheng', 'rmrbwy', 'dadifukan', 'rmdushu', 'rmwenyuan', 'wenyipl', 'rmrbmssc',
        #         'rmrbpl', 'rmrbllb', 'rmrbty', 'rmrbyjb', 'rmrb_hww', 'xiake_island', 'xuexixiaozu', 'peopledigital',
        #         'hqsbwx', 'huanqiu-com', 'America_hq', 'huanqiuouzhou123', 'huanqiukorea', 'huanqiutaiwan',
        #         'zhongguoqichebao', 'qichezaocan', 'wwwstcncom', 'quanshangcn', 'lianhuacaijingcom', 'zqsbxsb',
        #         'shujubao2015', 'chuangyzbh', 'trustway', 'zqsb_cfzx', 'gongsiyuqing', 'Betainvest', 'jksb2013',
        #         'jkzg-nhfpc', 'jksb2016', 'gh_abf70cc555e4', 'rmltwz', 'globalpeople2006', 'rmrbpaxy',
        #         'ChinaEconomicWeekly', 'msweekly', 'gjrwls', 'peoplevision', 'quan_yue001', 'guolishuhua', 'baidaitrip',
        #         'cnenergy', 'depo88', 'guojinengyuancankao', 'dabaxinwen', 'energyinternetclub', 'GlobalTimesNews',
        #         'gh_81dcf95743f9', 'gtmetroshanghai', 'LT0385', 'yaonidongwx', 'duxinyanjiusuo', 'tiantianfachi',
        #         'muyingribao', 'yansutanxing', 'fcyymwx', 'gjjrb777', 'gh_a1185130b3be', 'chinafundnews', 'Money-Lcq',
        #         'sanbanfuweixin', 'qhrb168', 'rmwz365', 'gh_2e81f20bd4d6', 'zhongguochengshibao', 'gh_0c422b3ac3e0',
        #         'qichezuweixin', 'qicheyuyundong', 'china_engine', 'jiayongqiche', 'qichepiping', 'zgcsgdjtxh',
        #         'ev-qiche', 'canfans_news', 'WDCHN-NES', 'rmrbqmtpt', 'xxdaguo', 'wxpdmi', 'people_rmw', 'cpcnews',
        #         'rmwjkpd', 'rmwshipin', 'qglt19990509', 'jxnihao', 'rmhuanbao', 'finance_people', 'renminyx', 'rmrbwx',
        #         'rmrbbj', 'baidaitrip', 'gjjrb777', 'rmrbjjsh', 'PhotoWorldMagazine', 'xinhuashefabu1', 'XHSXHSD',
        #         'wobaodao', 'xinhuafoto', 'xinhuapub1979', 'zgjzzzs', 'xhszzb', 'lwdflwdf', 'shzqbwx',
        #         'OutlookWeekly1981', 'www_cnstock_com', 'zhczyj', 'jjckb-wx', 'nbxdjb', 'xinhuaafrica', 'NX7913',
        #         'newsxinhua', 'sikexh', 'kjcxlcb', 'kjqydst', 'kxylydt01', 'jskjqy', 'XMTV-AUTO', 'xinhuaonline_bj',
        #         'xinhuahebei', 'xhwjxpd', 'xhwscxsj', 'onncc626', 'xinhuakehuan', 'wjqnxh', 'xinhuashipin', 'xinhuajk',
        #         'xhw-ysc', 'xinhuahouse_nj', 'shanxi_toutiao', 'interxinhua', 'bjcankao', 'Chinatopbrands', 'ckxxwx',
        #         'caiguo08', 'GlobeMagazine', 'banyuetan-weixin', 'gjxqdb', 'ahxinhuashe', 'chuangke_xinhua', 'kpzgcbzd',
        #         'xh-energy', 'cqhjsx', 'gd7744', 'chihuochuangjian', 'bjxuanwen', 'qstheory_001', 'WDANGS', 'XEshixi',
        #         'qiushimp', 'qiushisjb', 'hongqiwengao', 'gh_affeebf9ba89', 'gmrb1949', 'tianxiayan2015',
        #         'yuedugongshe', 'liuxuezazhi', 'zhreading', 'guangmingjiangtan', 'gmweijiaoyu', 'gmwhcy', 'gmyygs',
        #         'wenzhaibao', 'GM_WenYi', 'dongdajiefive', 'gm_GMAD', 'guangmingzhiku', 'gmw_001', 'wangxindangjian',
        #         'kejimingjia', 'Military2016', 'ourcecn', 'ssqs_2016', 'koudaijr', 'zbpafda', 'wocaijing11',
        #         'zgjcgycbs', 'zgfzb1986', 'ZG-xyjj', 'ncjrnews', 'smecei', 'o2olink', 'VIEW-CBMD', 'jingjizazhi',
        #         'JJZZSLSH', 'jjrbwx', 'cewenhua', 'autocecn', 'fzsbwx', 'edpbook_com_cn', 'ceinews', 'smecei',
        #         'cfw-com-cn', 'iceo-com-cn', 'cfnnews', 'flower_floraltime', 'chuangyidasai', 'RealTimeChina',
        #         'CHINADAILYWX', 'zgzs001', 'jjzswx', 'musicradio2002?', 'dszs001?', 'wenyi1066?', 'zgxczs720?',
        #         'lnzsam1053?', 'CNEB_CNR?', 'cnr_cnr?', 'cnrjunshi', 'zggbzz?', 'xinwenzongheng?', 'jjzsjysk?',
        #         'jyskjlb?', 'CNRTXCJ?', 'wangguan201508?', 'lnzsam1053', 'CCTV-channel1', 'cctvjrsf ', 'cctvdzw',
        #         'cctvshzck2013', 'CCTV1kaijiangla', 'cctvtzbkn', 'CCTV-1leyuan', 'cctvjyxwl', 'cctvxilejie', 'ijiaiwei',
        #         'cctvddc', 'cctv-duihua', 'cctv2-XFZZ', 'cctvyscj', 'cctvjysj', 'cctvdysj', 'cctvfh', 'cctvjjyflm',
        #         'cctv-yirenyishijie', 'cctv_cj_gl', 'Weareyoung_66', 'cctv2jingxilianlian', 'cctv2pinglun',
        #         'cctv2_cyyxh', 'CWZB_88', 'gh_22c6191afa20', 'cctv2sz', 'cctvcbn520', 'CCTVyangshizongyi',
        #         'huangjin100s', 'cctvyzyy', 'woaimantangcai', 'cctvwdsj', 'WYSCW_CCTV', 'cctvxxfcf', 'staroad',
        #         'gh_665917744409', 'Cctvhsll', 'cctv3wenhuashidian', 'cctvkmdj', 'cctvyilantianxia', 'zongyishengdian',
        #         'CCTV-YSRS', 'cctvqitianle', 'yangshifeichang6jia1', 'cctvhuanlexiu', 'gh_530ced15e899',
        #         'gh_06ab3b8bb060', 'CCTV4gbdawx', 'cctvkuailehanyu', 'jinriyazhou', 'cctvjrgz', 'cctvyfdj',
        #         'shenduguoji2015', 'cctvzhyy', 'CCTV-wgrzzg', 'cctv_zhonghuaqing', 'cctvzgxw', 'cctvcsydy', 'cctv4zgwy',
        #         'cctvhrsj', 'gh_28533671d357', 'CCTV-4ZBZG', 'cctv4lxwx', 'T2905956623', 'zhitongtaiwan',
        #         'gh_e80a6b8d2dad', 'shijietingwoshuo', 'CCTV-5sportnews', 'jianshendongqilai', 'cctv5hoopark',
        #         'saicheshidai', 'shuishiqiuwang', 'cctvxiaojizhe', 'cctv5tiyukaba', 'InteractiveNBA', 'cctvjunshijishi',
        #         'cctvjlrs', 'fangwuxgc', 'junmittx', 'junyingdawutai ', 'CAPFnet ', 'cctv7woaiguofang', 'jfjjs7tv',
        #         'cctv7sszjyx', 'CCTV-7_Junshi', 'jlwhdsy7', 'cctv7bzjd', 'CCTVygdd', 'CCTV7mlzgxcx',
        #         'cctv-7fazhibianjibu', 'A94897456', 'CCTV_MRNJ', 'cctvkjy', 'jujiaosannong', 'xiangcundashijie',
        #         'nongtv', 'nongye7', 'cctv7ssdzp', 'xiangyuecctv', 'cctv7xiangtu', 'ntvzaobao', 'cctveight', 'cctvxtj',
        #         'cctv9jilupindao', 'cctv1cha', 'cctv-zoujinkexue', 'cctvylrc', 'cctvbaijiajiangtan', 'cctvdushu',
        #         'cctv10_kejiao', 'storyboxes', 'cctv10-tansuofaxian', 'fammgc', 'wenmingmima', 'cctv-dajia',
        #         'gh_c3e024997eda', 'cctvgby', 'CCTVCSZY', 'cctvpflmj', 'CCTV12pingan365', 'cctvrexian12',
        #         'CCTV_xinlifangtan', 'gh_42f7a3741bc3', 'shequyingxiong', 'cctvyixian', 'CCTVFLJT',
        #         'daodeguancha-cctv12', 'cctvchanhuilu', 'cctv12xqds', 'yangshitianwang', 'cctvnewscenter',
        #         'cctv_newsweekly', 'xinwendiaochacctv', 'xinwenyijiayi', 'jdftcctv', 'cctvgdzg', 'cctv_worldweekly',
        #         'cctv14guonianla', 'cctvxwddk', 'zmxxsn', 'gh_4dfff955d985', 'cctvyykd', 'jssn3031', 'CCTV-Children',
        #         'zuiyejiaqi', 'cctv15music2013', 'CCTVyiqiyinyueba', 'GlobalChineseMusic', 'cctv-gsywx', 'CCTV_HMYY',
        #         'gh_054ec888a67a', 'cctvfhgy', 'CCTV_News_Content', 'gh_06d1dea1491a', 'CCTV-FRANCAIS', 'CCTV-Arabic',
        #         'CCTVADAD', 'cctvgygg', 'cctvkandian', 'cctv-vc', 'cctvcomweixin', 'yswshangcheng', 'cntvweixin',
        #         'CNTV-CBox', 'cctv-wlcw', 'ipandacom', 'CNTVsports', 'cctvyuedong', 'mongolcntv', 'CNTV_UYGHUR',
        #         'cntv_kazakh', 'wangluoxinwenlianbo', 'tushuojzg', 'zchhdhc', 'cctvwish', 'cctv315', 'cctvhjcf',
        #         'NEWSPlus', 'cibn123', 'duanchun-shuo', 'crihuanqiujunshi', 'hitfmcri', 'gh_c92bcbfd9b97', 'cribbr',
        #         'gh_7e86f2af1dc1', 'huanqiuruiping', 'bzbkcri', 'CRI-russian', 'zxfcdcri', 'crionline', 'CRIjpn',
        #         'cridanganjiemi', 'RADIOEZFM', 'ezfmmotianlun', 'Radio_cri', 'fm9050', 'sportstalk', 'cri_lao',
        #         'crihqmrf', 'criturkish', 'CRIfrench', 'CRI_ESP', 'gh_1ae6140d3b1a', 'laowaikandian', 'cri_indonesia',
        #         'cripor', 'gh_d52089dd3ee7', 'myanmar_online', 'hqjy905', 'Mabuhay_CRI', 'cripersian', 'khmerccfr',
        #         'watchasean', 'jiluzhemiyaniu', 'crient', 'crinanhai', 'CRI_Nepal', 'CRIzwhq', 'CRIgreek', 'crithai',
        #         'Hrvatska1', 'itaiwannews', 'CRI-Poland', 'cri_malay', 'shiliuhaoxinxi', 'Balkanrose',
        #         'Delhiin-tsag_2016', 'WORLDWIDECHINESE', 'srilankacri', 'HQQG--CRI', 'CNS1952', 'cns2012',
        #         'qiaowangzhongguo', 'OverseasChinese_CNS', 'cnsgs-01', 'CNS-SD', 'CNS-gd', 'CNS-chaoshan', 'cns-jl',
        #         'siluxgc', 'cns-xj', 'cns-bt', 'cnshebei', 'hubeicns', 'cns_sn', 'zhangzhongjiangsu', 'jstvjsxw',
        #         'cnssx0351', 'cns-gx', 'zzxgzwx', 'cns0898', 'sldhslm', 'cns-hlj', 'hunanhaowan', 'cns_ln', 'cnsyn-01',
        #         'shiyunnan01', 'CNSxywc', 'qinghaiyys', 'sfscns', 'chinanewsweekly', 'chinanews-shanghai', 'gannews',
        #         'cnscqttnews', 'cctvnewscenter', 'cctvcomweixin', 'baguaconghua', 'apptoday', 'baguaconghua',
        #         'baoliao-020', 'bazaarstar', 'bmsh_gz', 'by168com', 'cctvcomweixin', 'chinamobilegame', 'chuangyezone',
        #         'CN440001', 'consumer-report', 'DPCHRDZX', 'Fang-com1999', 'fangjia-gz', 'fangyimai2013', 'FC510370',
        #         'fzg360gz', 'GDAPER', 'gdfood2011', 'gdsjyt', 'gep2013', 'gh_840f04e9f9e8', 'gongzhonghao001',
        #         'greenovation', 'gswmcc', 'guancha006', 'guangzhou3456', 'guangzhouhouse', 'guangzhouplus',
        #         'guangzhoutop1', 'gz-focus', 'gzbgyyz', 'GZBNGS', 'gzcankao', 'gzcmbchina', 'gzeducation', 'gzjzfb',
        #         'gzqz020', 'gzrb1212', 'GZSBS1314', 'gzshis', 'gzwangyifangchan', 'houseifeng', 'houseqq_gz', 'housezc',
        #         'ihuichi', 'iiChuangYi', 'InGuangzhouCity', 'kenjinrong', 'LandRove711', 'longdongshenghuo',
        #         'LUOGANGJIAYUANWANG', 'manshiguang3', 'mlddxypdzhz', 'ndkuayue', 'nfrbsy', 'nfxxsc', 'njusky',
        #         'plusyouth', 'py2456', 'qingniankongjian706', 'qq296836288', 'redianweiping', 'shangdao999',
        #         'shenghuodiaochatuan', 'shenmagame', 'smr669', 'solidarity4ever', 'SP-666888', 'sunbushu123',
        #         'Talkpark', 'tianheshangquan', 'wangxinguangdong', 'weiguangzhou1314', 'welianapp', 'wuxiaobopd',
        #         'xc020chao', 'xdnphb', 'xinby2016', 'xxsbejtbj', 'xxsbejtxc', 'XYGC_China', 'ycwbwhcb', 'yeascnu',
        #         'yezhulecom', 'yueshanghuigd', 'YuLe100Fen', 'yuqing_fw', 'ZC173-COM', 'zcshenghuo666', 'zcsht2014',
        #         'ZGGZFABU', 'zgzyscw', 'zhaoqingzhiku', 'zhenghedao', 'zhijuzk', 'zjshzsh', 'zzswgx', 'a221250',
        #         'baobzhu', 'bilingongren', 'bjshengyun', 'CantonRadio', 'caogenzhiku', 'casszhongjun', 'dagongmama',
        #         'faith-in-one', 'fazegongyi', 'Feminists2016', 'FeministsLGBTQAI', 'FFeminist', 'gdufetns',
        #         'gh_67f7eff9f590', 'GICS2013', 'GLCAC-01', 'GSEC123', 'GuyuStory', 'gzld1688', 'gzlntzkss2014',
        #         'GZxmtnx', 'hzjinshazhou', 'kanpei2015', 'lang-club', 'laobinglaobing121', 'LGBTRights', 'lingdaoquna',
        #         'lvxing020', 'meilihuangbu', 'mimeng7', 'msgzms', 'nandugz', 'NewHoriEnter', 'New_Austral', 'ngocn05',
        #         'potu_groundbreaking', 'qinyouhui002', 'qiubaifree', 'sanlouyouthspace301', 'sysudin', 'SYSU_rainbow',
        #         'trans-center', 'TrendEntLife', 'vloveit', 'weyiqi', 'ycwbxiaomanyao', 'youngdust', 'youxi248',
        #         'zcnaxie', 'zgztlm', 'ZHITONG_CHINA', 'zhuojianzhuojian', 'zqb_caolin', 'cctvnewscenter', 'cdqqcom',
        #         'chinainternationnews', 'cns2012', 'conghuakx', 'daqinwang', 'dayanhs2015', 'fenghuangxinmeiti',
        #         'fmgz1061', 'foshanxinwen', 'G4news', 'GDGGDVXC', 'gdsinazw', 'gdtoutiao', 'GDTVZJPD2013', 'gd_xkb',
        #         'GRshequ', 'guanchacn', 'guangzhouyouth', 'gzdailybl', 'gzrbszxw', 'GZTV-M', 'Gz_byss', 'hantiang-1',
        #         'hpggguancha', 'huaduzc', 'igznews', 'intozine', 'jinjibaodao', 'jjbd21', 'jjxxtimes', 'kingoldmedia01',
        #         'linyiforefront', 'luogangwang', 'msweekly', 'nbweekly', 'nddaily', 'NF-dushi', 'nfdaily3c', 'nfncb289',
        #         'nfsyyjjb', 'NF_Daily', 'oeeeend', 'panyuribao', 'Peopleweekly', 'qzdt986', 'renwuzaixian',
        #         'thepapernews', 'timeweekly', 'tvscsts', 'tvszuixinwen', 'wanbaoweixin', 'wenhuidaily', 'wwpnethk',
        #         'wwwhdbbsnet', 'XKB-CBD-NEWS', 'xkbfs888', 'xkbshenduxinwen', 'xkbxmt', 'xxrbfzxwvx', 'xxrbvx',
        #         'xxrbycxwlin', 'xxsb2012', 'ycdtb2012', 'ycwbbaoliao', 'ycwbjiazhang001', 'ycwbyzj', 'ycwbzzj',
        #         'ycwb_jyw', 'yixian300', 'zc-news', 'zhiboguangzhou', 'zhihuribao', 'zjxwy630', 'bcgguangzhou',
        #         'conghuagongan', 'gcdyweixin', 'gh_4eecb3856810', 'gh_e7dbb197901e', 'guangzho007', 'GuangzhouMTR',
        #         'GZ-ZCGA', 'GzByYjb', 'gzchxf119', 'gzhdfb', 'gzhpfb', 'gzhzfb', 'gzliwanfabu', 'gzpyfb', 'gzszcgs',
        #         'gzyxfb', 'gz_baiyunfabu', 'gz_nsxf', 'huaduguoshui', 'huangpu119', 'huangpudishui', 'huangpuguoshui',
        #         'nanshaguoshui', 'nfrbzsgc', 'nssqxt', 'panyuguoshui', 'panyuxiaofangdadui', 'py168-com', 'tianhefabu',
        #         'tianheguoshui', 'WMGuangDong', 'yxgswx', 'zcxfdd', 'igznews', 'Rainieyang060477', 'ererose888',
        #         'everose888', 'gzwangyifangchan', 'bmsh_gz', 'casszhongjun', 'xsgongshe', 'wuyoushui123', 'newsxinhua',
        #         'baoliao-020', 'bazaarstar', 'apptoday', 'apptoday', 'newsxinhua', 'cns2012', 'cctvnewscenter',
        #         'shijieribaoph', 'aucntv', 'angolanews', 'GEStudio', 'ssdaily', 'jianhuadaily', 'LaVozChina',
        #         'zhongwendaobao', 'chineseinla_com', 'chinapress', 'ChinesePress', 'newsca', 'shangbaoindo',
        #         'oushi1983', 'uk-chinese', 'Zimbabwe_ChineseWeb', 'euchinesejournal', 'SingtaoEU', 'angkortime',
        #         'yuhsrb', 'onemex-com', 'aozhouhuarenwang', 'ukdajiatan', 'Channel-Chinese', 'qiaowangzhongguo',
        #         'We-sa2cn', 'udnbkk', 'cctvcomweixin', 'fenghuangxinmeiti', 'cctvnewscenter', 'zhaoqingfabu', 'gdgyfb',
        #         'gh_aaeb341631a1', 'citicbankchina', 'gh_365752ae0ea1', 'gh_0be17657d15b', 'citiccpamc ',
        #         'citiccpamc_weixin', 'citichuyu', 'CiticAgriculture', 'citic-hic', 'citic-hic-jw', 'ccc_hr',
        #         'ccc_qywhb', 'VivaAfrica', 'citic_fzqzx', 'znszvhr', 'CADI-Group', 'CADIwh', 'cadi_ghdzb',
        #         'CADI-culture', 'CITICPRU-Official', 'citicmh', 'zxxy2002', 'zxxyspermbank', 'hzzxyy1985', 'dz541zyy',
        #         'Zxhzyy120', 'PHIS-CITIC', 'swsfybjy', 'ZXDTSC', 'citic_healthcare', 'citictour', 'zj_citic',
        #         'CITIC-MICE', 'sh-citic', 'i4007701700', 'sh021666', 'zhongxintuoguan', 'CITICS', 'CIITCS_Tourism',
        #         'CITICS_OverseasResearch', 'citics_strategy', 'ZXZQDCYJ', 'CiticsMacro', 'Citics_homeappliance',
        #         'CITCS-Retails', 'CITCS_NEEQ', 'CITICSYIYAO', 'gh_08cda1e1d7ff', 'CiticsMachinery', 'gh_15b911e55e42',
        #         'gh_21c573a56db3', 'gh_294e097afc75', 'gh_0017730a38b2', 'MediaBBS', 'feiyinguandian', 'ZXJGYJ',
        #         'maigaobank', 'gh_5edf2ad8dfe3', 'Fashion_forefront', 'zhongxinjiaoyun', 'citics_food-beverage',
        #         'citics_bj', 'xinEtou', 'czcitics', 'cdrmnl', 'CITICS-CTU', 'CITICS-DL', 'citics_db', 'citicsdg',
        #         'fszxzq', 'citicsfj', 'zxzq-fushun', 'citicsgd', 'pyzxzq', 'hrb600030', 'zxzqhk', 'CiticsHM',
        #         'zxzqhz95548', 'zxzqdxl', 'snjjxzyyb', 'citicshf', 'zxzqhhht', 'zxzqhbfgs', 'zxzqhz', 'citicsjs',
        #         'citics_jx', 'citics', 'ZXZQNC', 'citicsnn', 'citicnbfgs', 'zxzqnbttb', 'zxzqnbzs', 'zxzqnh',
        #         'zxzqphyyb', 'CiticsQD', 'zxzqst', 'citics-shhf', 'zxzqshsh', 'Citics_changshou', 'zxzq_szqh',
        #         'zxszfgs', 'zxzqfhyl', 'zxzqszlg', 'zxzq_sz', 'citics-szwhl', 'zxzqsjz', 'CITICS_suzhou', 'Wujiang_zx',
        #         'zxzqty', 'zxzqtangshan', 'gh_e436cccada94', 'zxzqtjdg', 'zxzqhhd', 'ZXZQTJYYL', 'zxzqtx', 'zxzqwz',
        #         'citicswx509', 'jsddyyb', 'xddjyyb', 'xa88236158', 'zxzqxzyyb', 'zxzqyy', 'zxzq-changchun', 'citicszj',
        #         'zxxlyyb', 'zxzqsdbz', 'zxwtzzyyb', 'zxzqcfgl', 'zxzqhzyyb', 'zxwtjnyyb', 'zxwtjmyyb', 'Zxlc95548',
        #         'zxzqjn', 'zxwtlzyyb2275566', 'zxwt_jijunlin', 'zxzqlk', 'zxzqlyyyb', 'Zxwtbsl600030', 'dzlwtzq',
        #         'zxzqjdl', 'zxzqsdjsql', 'zxzqkfq', 'zxwtnjlcfgl', 'zxzq_sdl', 'ZXWTWHL', 'citicwt', 'zxwtzqcfgl',
        #         'zxzqsdzbmsj', 'zxzqsdzc', 'zxzqzp', 'Citics95548', 'i_option', 'citicscfgl', 'zxqh_yjb', 'citicsf-zz ',
        #         'taiji-qq', 'zxhjjs', 'XGL_lighting', 'ydianting  ', 'weixintingche', 'ake19970602', 'zxkycitic',
        #         'thjweixin', 'zxjzjs-gm', 'aqniu-wx', 'freebuf', 'i77169', 'alijaq', 'XuanwuLab', 'a301zls',
        #         'YunTouTiao', 'youxia-org', 'AnZer_SH', 'lookvul', 'oschina2013', 'mcbang_com', 'lazy-thought',
        #         'seebug_org', 'gh_ec13b31de182', 'icqedu', 'wushengxinxi', 'KnewSec', 'DJ_notes', 'NUKE404', 'taosay',
        #         'safeapp', 'nbdnews', 'NF_Daily', 'nddaily', 'stpbscm', 'sttvnews', 'strm0754', 'haochimei0663',
        #         'stliantong', 'STYiXian', 'shantoutop', 'stsrmjcy', 'stmsa01', 'stchedu', 'PorscheSTDB', 'edaynew',
        #         'gdst_oil', 'ssst201509', 'jujiao0754', 'STWGXJ', 'shantoudxs', 'shantoulvshi', 'lvshixuqincheng',
        #         'gwtlvshi', 'gh_4bd61ea7ad6d', '2936022', '2936022', 'stchedu', 'stmsa01', 'stsrmjcy', 'chqyjb',
        #         'chenghaixiaofangV', 'chqyjb', 'stchedu', 'stmsa01', 'stsrmjcy', 'chqyjb', 'stchedu', 'stmsa01',
        #         'stsrmjcy', 'chenghaixiaofangV', 'chqyjb', 'stchedu', 'stmsa01', 'stsrmjcy', 'rmrbwx', 'XHSXHSD',
        #         'cacweixin', 'xinhuashefabu1', 'xiaoshanwlm', 'yxgc99', 'cacweixin', 'xszcwx', 'Xszclt', 'wxslife',
        #         'wxswsh', 'ipozm00036', 'my19lou', 'Xiaoneiwangcom', 'wwwzaixscom', 'Xs163-net', 'xshavefun',
        #         'kuahuqiaocom', 'xiaoshanwlm', 'Xszn89757', 'gl311241 ', 'gualixxs', 'xszcxw', 'xsgbdst', 'xsgdxwzx',
        #         'XSFM1079', 'xstvxsj', 'Hi_xiaoshan', 'xiaoshanribao', 'Elite_QTH', 'xsrb_jjzk', 'QC88666',
        #         'xiaoshan-360', 'NEWXIAOSHANG', 'xiaokashow', 'xsrbjrtk', 'xsrbdzzj ', 'xstownpublish', 'lblm-gfwx',
        #         'hzrbjrdjd', 'xsrbxjz2004', 'djdxjz', 'xsnetcn', 'xianghuxsnet', 'Xsrb_wxxs', 'xiaoshanjiaoyu',
        #         'xianghuclub', 'weifanggongan', 'weifangfabu', 'E安全', 'E安全', 'EAQapp', 'njxz025', 'ipandacom',
        #         'ultraplus_cross', 'dagaotegao', 'loushishiguangji', 'gongansihuafuwu', 'rmrbwx', 'cctvnewscenter',
        #         'thepapernews', 'guanchacn', 'ckxxwx', 'ourcecn', 'xwzc021', 'nddaily', 'chinanewsweekly',
        #         'capitalnews', 'xiake_island', 'xjbzse', 'wepolitics', 'hqsbwx', 'newsbro', 'finance_ifeng', 'gzadmin',
        #         'qqgentle', ' gh_acbbcdd3fcd2', 'gh_62dfc109892d', 'Petrochem-Forum', 'ICIS_China_LiLi', 'hg707_com',
        #         'Hydrocracking', 'dsxp688', 'qianqianchuangtou', 'zui0580', 'Zf0580', 'ayawawavip', 'FB-xitong',
        #         'tm0851', 'Cool-Guiyang', 'gytv851', 'guiyangtong', 'zbgy5822222', 'xsxianhua', 'nesw97', 'nbnw666666',
        #         'zhegu8', 'ultraplus_cross', 'travelread', 'gzgajg', 'gzsedu', 'gysjyw', 'gzespt', ' citics_strategy',
        #         ' thjweixin', 'feiyinguandian', 'i_option', 'gh_21c573a56db3', 'citics_food-beverage', 'citic-hic',
        #         'dz541zyy', 'CITICSYIYAO', 'citicbankchina', 'Citics95548', 'citicsproducts', 'citicscfgl', 'zxqh_yjb',
        #         'citicsf-zz ', 'taiji-qq', 'zxjzjs-gm', 'gh_5edf2ad8dfe3', 'Fashion_forefront', 'zhongxinjiaoyun',
        #         ' citics_strategy', ' thjweixin', 'feiyinguandian', 'i_option', 'gh_21c573a56db3',
        #         'citics_food-beverage', 'citic-hic', 'dz541zyy', 'CITICSYIYAO', 'citicbankchina', 'Citics95548',
        #         'citicsproducts', 'citicscfgl', 'zxqh_yjb', 'citicsf-zz ', 'taiji-qq', 'zxjzjs-gm', 'gh_5edf2ad8dfe3',
        #         'Fashion_forefront', 'zhongxinjiaoyun', 'citics_strategy', 'thjweixin', 'feiyinguandian', 'i_option',
        #         'gh_21c573a56db3', 'citics_food-beverage', 'citic-hic', 'dz541zyy', 'CITICSYIYAO', 'citicbankchina',
        #         'Citics95548', 'citicsproducts', 'citicscfgl', 'zxqh_yjb', 'citicsf-zz ', 'taiji-qq', 'zxjzjs-gm',
        #         'gh_5edf2ad8dfe3', 'Fashion_forefront', 'zhongxinjiaoyun', 'citics_strategy', 'thjweixin',
        #         'feiyinguandian', 'i_option', 'gh_21c573a56db3', 'citics_food-beverage', 'citic-hic', 'dz541zyy',
        #         'CITICSYIYAO', 'citicbankchina', 'Citics95548', 'citicsproducts', 'citicscfgl', 'zxqh_yjb',
        #         'citicsf-zz ', 'taiji-qq', 'zxjzjs-gm', 'gh_5edf2ad8dfe3', 'Fashion_forefront', 'zhongxinjiaoyun',
        #         'yes0717', 'ycyd-10086', 'yichang188 ', 'finance_ifeng', 'newsxinhua', 'Zhongguojiaoyubao', 'jybxwb',
        #         'yzwb20102806', 'xsgbdst', 'zjsjyksywx', 'nbdnews', 'gzgycyjy', 'gzgycyjy', 'aisiqingnian',
        #         'gh_24fdcfee9407', 'gh_d99f17a3c0ab', 'weikjsh', 'TrendEntLife', 'EntFront', 'upooxx', 'yuleshiang',
        #         'vvxixi', 'cosmochina', 'TrendLifeRemit', 'jiankangssbk', 'GuangzhouMTR', 'gzchihuo7', 'zouqilx',
        #         'gzchihuo7', 'weikjsh', 'TrendEntLife', 'gh_ea38249bc86e', 'gzvworld', 'safe01', 'gzuniversity',
        #         'cn0851com', 'tfb0662', 'education-today', 'cernet', 'shijiejiaoyu', 'edreview', 'ictedu',
        #         'jiaoyuxinwenwang', 'Chinaedu2014', 'zgjyxxh', 'irenminjiaoyu', 'cityetv68', 'zgjyxxh', 'ictedu',
        #         'stganlantai', 'cityetv68', 'CantonRainbowGroup', 'gh_75ab47bb3210', 'assy224300', 'gh_97b725ee8500',
        #         'gh_69a6c35f0654', 'ai_sheyang', 'syq5388', 'XingfuHaihe', 'atsyr0515', 'syxsy0515', 'gh_bf4c29b37bc6',
        #         'syrjcom', 'syw320924', 'jzxt666', 'cnsheyang', 'sheyangcheng', 'zhsheyang', 'dasheyang', 'syjiacc',
        #         'ycrd01', 'dywt0515', 'yccs6199', 'ycbaixing', 'weishuzi58', 'wmdeyc', 'xskd0515', 'binhaizx',
        #         'bhwangcn', 'xbinhaibbs', 'dongtaiwsg', 'vyc0515', 'chwl0515', 'tv0515', 'baixingdiyi', 'yc2min',
        #         'ycyanxunwang', 'zhuhai6677', 'botofilm', 'doumen0756', 'DM-LYJ', 'Q1871101820', 'AomenHr', 'MacauWX',
        #         'zhuhairx', 'm4006116063', 'zhuhaizp', 'gh_8e2fdd6761dc', 'zhch0756', 'zhportnews', 'gh_2660451e2715',
        #         'zhhy345', 'nfrbzhgc', 'wd0756', 'wazhuhai', 'zhuhaixxs', 'jinbushanglv', 'zhhsh8', 'shimuwang-net',
        #         'xiguawman', 'DWQ8991', 'zhuhaishenghuo', 'gh_64d4697dc852', 'yodewo', 'knowjluzh', 'nvsheng-zl',
        #         'jzlm365', 'zhweishi365', 'zhcptjgyxsdzb', 'LSJLL666', 'zhcptweixin', 'chaozh0756', 'gkygfwx',
        #         'gh_099b867cb5c3', 'UIC_ZH', 'jzdwxcb', 'zmushelian', 'zh-zcsw', 'JNU-Zhuhai', 'zhuhaihuishenghuo8',
        #         'sysuxtw', 'ygashq8', 'zhhouse163', 'zhdmsc', 'pingan-dm', 'JWren0756', 'w-zhuhai', 'zhdxwsyyt',
        #         'hopesungroup', 'sdytxl', 'sddkby', 'sdjiangong', 'shandongjinrui', 'sdjbjtyxgs', 'sdzywhfz',
        #         'sd-qiquan', 'GIECO_dy', 'tsingtaosd', 'sdtv96005900', 'ljsd22', 'mrsd22', 'sdjjgb', 'sdxjrd', 'HB6754',
        #         'shandongpeople', 'sdbd168', 'sd_weifang', 'SD1809622102', 'wjshandongzd', 'sdxfxc_119',
        #         'shandonggaofa', 'sdjiancha', 'gh_08cdf4e399d2', 'sdjyfb', 'gh_08a701c6f59b', 'dongyingzhijian',
        #         'gmrb1949', 'CHINADAILYWX', 'qstheory_001', 'ycdysj2233555', 'xinhuashefabu1', 'XHSXHSD', 'zgzs001',
        #         'cnr_cnr', 'CNS1952', 'cns2012', 'wa0759', 'zhanjiangguoshui', 'gh_887f53ea398f', 'qqnba-wx',
        #         'tctxw67812728', 'hntcjcy', 'hntcgs', 'tcxszglj', 'hntcxfdd', 'zstc99', 'gh_2825c0b8533d',
        #         'gh_2c6a6bb1c4b3', 'gh_8b50a2298a97', 'tcxzfw', 'jishikandian', 'hnjdxmt', 'hngfgzh', 'hnyzy2016',
        #         'hainangongan110', 'hain119', 'gh_0e9ba8e1d7b8', 'chqyjb', 'chenghaixiaofangV', 'shanxigonganjiaojing',
        #         'xianyangjiaojing122', 'xa-police', 'gh_2a75991a8cd3', 'gh_3c09b0284b37', 'hzjf110', 'gh_84945317e1f3',
        #         'gh_23315ba9693f', 'hzsgajbbfj', 'hezhoujiaojing', 'gossipleague', 'girlnba', 'dqmmiss',
        #         'gh_8b1d23dbd0b2', 'cctvnewscenter', 'xinlang-xinwen', 'changjianggongan', 'pagz110', 'gzepb12369',
        #         'gzminzheng', 'gzsfzhggwyh', 'gzsjtw', 'wenminggz', 'guangzhoujiancha', 'gzsgxw', 'gh_609018f1f8e5',
        #         'gzsswj', 'gzwsjs', 'gzaic2017', 'guangzhoudishui', 'hain119', 'cidugongan', 'hainangongan110',
        #         'gh_0e9ba8e1d7b8', 'fjrbwx', 'i_fjtvnews', 'myfzqq', 'xianhua-3', 'libinlian710', 'yxh18971558290',
        #         'qymlj1949', 'shangpinlianghui', 'gh_d0694dcbc929', 'libinlian710', 'Beinger33 ', 'zgwmjy_gm ',
        #         'feitong88000', 'gh_713e3c0d0d96 ', 'ss-ytsc88', 'KM33JY ', 'ssjgyx', 'ss-bll ', 'crds333', 'xsxianhua',
        #         'xs-xianhua', 'gzjiaojing', 'gz-rst', 'gzssfj', 'gzzfcxjs', 'gh_bd6773a90306', 'lianjieguangzhou',
        #         'tyzzlc', 'TYjinrijiaotomg', 'taiyuangongan-110', 'sxwbsxtt', 'sxtyjjzd', 'TY_FM107', 'tyty114',
        #         'shanxiribaowang', 'sxxwlbgw', 'shanxiwanbao', 'datongchuanmei', 'datongnews', 'DTGZXX', 'datongcm',
        #         'v037300', 'sxttszh', 'szjjxcjy', 'sz0349888', 'szxww0349', 'szgawx110', 'jizhezhan99999', 'CBXZ0350',
        #         'zxanjj', 'sxfzbxzjzz', 'sxxzga', 'cszx0350', 'jzzxcc', 'yqxww0353', 'sxyqrb', 'yqcc0353', 'meetyq',
        #         'lvliangzaixian', 'lldyms', 'LLJTGB', 'lltt0358', 'kanlvliang', 'sxxwlbgw', 'jzwsh999', 'tgxrmzfbgs',
        #         'sxjzfulian', 'jinrijinzhong', 'czgj521', 'czhsh8', 'czxww0355', 'cbczwx', 'changzhiribaoshe', 'lfjjzd',
        #         'fm8890357', 'lfdigov', 'linfenzixun', 'wenminglinfen', 'jcgz0356', 'jczxwx2014', 'jctt668', 'JinCnews',
        #         'jcwsxx', 'ychengcom', 'shengweidayuan001', 'sxycjjzd', 'ycwzx8', 'ycbl01', 'xhwjxpd', 'jiangxifabu',
        #         'jiangxiweishixinwen', 'lianjiejiangxi', 'jxgagfwx', 'fm962gz', 'ycwbvlife', 'iceo-com-cn',
        #         'nanfangplus', 'southernweekly', 'southcn_news', 'NFWSchannel', 'gdtvjrgz', 'GRT-LNXQ', 'fm10771077',
        #         'ilove1036', 'GRT_QMFQS', 'gh_8731cb794259', 'grtgdnews', 'GDLZTV', 'radio914', 'SouthReviews',
        #         'chudian-news', 'www-21so-com', 'gdtvtyzj', 'gdggpd', 'hsl02061293110', 'gdgbxw', 'gdfabu0710',
        #         'GuangzhouMTR', 'bdbguangzhou', 'funs360', 'gztv630', 'ganzhougongan', 'gzsjyj2016', 'yuanchengfabu',
        #         'hyycga', 'heyuan_cn', 'xxsb2012', 'czrbicz', 'czlook2011', 'changzhixinwen', 'tangjingdj',
        #         'guangzhoudaily', 'xxsbejtyjds', 'hain119', 'hainangongan110', 'hngfgzh', 'hdqcxh', 'hdqcpj',
        #         'changan_020', 'qcqzx365', 'CarHotInformation', 'hdtvnews', 'hddtfm1005', 'huadushb', 'huaduzc',
        #         'wwwhdbbsnet', 'gzrbhuadusqb', 'HuaDuWSH', 'hdbnews', 'Shilinggov', 'happyjianshen', 'shiling18',
        #         'gh_c5760bddfada', 'gdjrgzt', 'GDGGDVXC', 'gzlsfb', 'iconghua', 'jskd', 'jscszh', 'dihuokuangbiao',
        #         'csdcsc', 'jishikandian']
        return ['infusha', 'gh_0364574547c8', 'wei528400', 'wei528467', 'tzsh-2001', 'ruyi2368', 'dsx-life528463',
                'gh_7d09a49f50f3', 'goshenwan', 'zsgzsh', 'gangkoulife', 'ja88756088', 'BUDS-EDUCATION', 'tzzyjn',
                'xiaolanhot', 'xiaolantoutiao', 'zsfusha', 'house10000', 'zsvolvo', 'xhz011', 'sanxiangquan', 'zsjypd',
                'gh_6e0a533566e6', 'sj48hgg', 'gh_15f50aee4d77', 'tzzwsjs', 'gzxfdd119', 'dongfengxuanchuan', 'SXWS-YS',
                'dfqn54', 'ZSTZLG', 'zhongshanshuzhan', 'gh_4c909259f51d', 'gh_417326357165', 'sanjiaoshegong',
                'dddspd', 'gzyihuavip', 'zhongshandayongxf', 'zhongshandaily', 'zshuangpu', 'MZMSQ666', 'ntfj110',
                'gzdsb2012', 'XLMJ_076022832789', 'XLURARA', 'gh_df086bf073c7', 'ixiaolan_com', 'Mt_WuGui_Nature',
                'im0760', 'AYDHJD', 'gzjw22359610', 'nfrbzsgc', 'ZY88330306', 'MinZhongFB', 'gaoboedu', 'dongshengsy',
                'gh_756b5ba24dce', 'gh_fee95eacc524', 'gzzwhz', 'zschihewanle', 'guzhendengdu', 'zhaopin0760',
                'oncity-cc', 'zs_dsyy', 'zsbfsh', 'shaxi0760', 'chowtinxl', 'oncity2014', 'tanzhoujunyuan',
                'TPR-dongqu', 'minzhongtong', 'gh_b3bf87cd3ebe', 'zssq5dgz', 'dongfengtiny', 'zhongshandongfeng',
                'zsnews2012', 'lovetanzhou', 'sxkhly', 'zstz760', 'sqtpxx', 'xiaolanaiwei', 'k-city', 'zczs88',
                'dnyey2011', 'love-gangkou', 'tzws0301', 'gh_6a5191bb6d55', 'GDGGDVXC', 'gdzstour', 'ZSYYWY-3377',
                'zsdachong', 'Doubi989', 'mysanjiao', 'zszqtzyyb', 'sxzwjj123', 'gztv8888', 'crider0760',
                'Saturday-SPA', 'zsdongfeng1', 'fsnaxie', 'ZSjiuxie', 'SJ-15602820794', 'gzsq168', 'heshengxiaoxue',
                'zsnanlang', 'huangpu0760', 'tzlife888', 'minshengshaxi', 'gh_e972f569bc60', 'gofusha', 'zsxqwh',
                'zays076022550018', 'zs-tzyy', 'gh_156fbec2bd60', 'xiaolanren0760', 'zsqpfy', 'yesfusha', 'TTYC-XLD',
                'guzhenanjian', 'zsdqga', 'zstzahxx', 'panyuetouzhen', 'zszswx', 'dqhysq', 'NLZXQ01', 'CUIHUA_huahua',
                'dachong0760', 'zsquan0760', 'zs-wzxl', 'wgs_0760', 'Belle-LEGO', 'xingfuwa888', 'z_ssh666',
                'shenwanqingnian', 'ZSHJGA', 'gh_70f480001a04', 'city0760', 'banfufabu', 'gh_0bc30723f419',
                'zsdqzx-RobotTeam', 'zsdqfb', 'tzxdyy120', 'zs_news', 'daxingpost', 'zsdfjdb', 'zstzfb', 'sxtv-ws',
                'zsbfgafj', 'haoyibandao', 'tzkjyk', 'yhqn54', 'xldianshang', 'zsdf110', 'ZGHJ-XLD', 'gh_92e844d484f6',
                'yesnantou', 'zsyzsys', 'fushazixun', 'gh_1ab72b4615b8', 'gh_6c9b3cfa89fd', 'sjzmryb',
                'gh_9debbc7ed67f', 'ZH88229777', 'huolinantou', 'gh_cd0dba8b6fbd', 'ZSHL119', 'zhongshanfabu',
                'gh_1e1ca3cef86f', 'js88222888', 'zhongguodengdu', 'gh_09dd4b8e1a21', 'nantouxiaofang',
                'zsshenghuowang', 'autozsnews', 'chenshanzhuangyuan', 'mjyg01', 'yesguzhen', 'sanjiao0760', 'nanqudxs',
                'zstanzhou1', 'zstsj0760', 'weishaxi', 'oppoer-888', 'zssx760', 'zhongshannanqu', 'zsxlymh',
                'jordanroad-xiaolan', 'wzsanxiang', 'zsshengpingwang', 'izhongshan86', 'gh_36b5ce37e0c6', 'yesdongfeng',
                'sxwshsq', 'xiaolanyidacinemas', 'Xiaolan_Culture', 'sanxiangfb', 'happy_every_bay', 'KF13590710723',
                'dongshenglife', 'zshuatu', 'gh_571fd2959244', 'zhongshanhl', 'hcqzgq1982', 'xlqn22118811', 'zsmzga',
                'gh_31f41a1589e8', 'xiaolanwenhuaquan', 'zhao528400', 'yhzqzsgz', 'PAHL110', 'fushablackstone',
                'wedding0760', 'lttqcyp', 'XLCHJD', 'dchmjj', 'dachongfabu', 'TanZhouNongYe', 'zssgzrmyy',
                'dachonglife', 'Sanjiao-tong', 'ju0760', 'xiaolan789789', 'love-nantou', 'jcsp20150920', 'YLW_HP',
                'xinfumeixue', 'gh_83a1404b297a', 'lovehuangpu', 'jinribanfu', 'zs_dqqn', 'XiaoLanLibrary', 'zstzxf',
                'TZmiumiuclub', 'xiaolanu', 'guosenzsb95536', 'zssanxiang', 'gh_320db9a04df1', 'gangnanjx',
                'zshlschool', 'ayb88581333', 'hemeigangdong', 'gz-lightingfair', 'guzhenshequxueyuan', 'tanzhou_com_cn',
                'gh_5251ca4547d9', 'longzhenshixiang', 'XIAOL-WB', 'zstzlg2017', 'dengduguzhen', 'bmshlx', 'zsxlwgz',
                'dongfengbd', 'zhongshandsxf119', 'zsnantouo', 'xl-jfr', 'whp528429', 'ZSHL01', 'zshptw', 'zssanjiao',
                'zssdfrmyy', 'gh_24a70eeb7153', 'shiqimeizhouyifa', 'gh_070385afa268', 'zswksx', 'topmall2013',
                'zhongshanclf', 'zsltjy', 'SMUSEGZ', 'zsdashijian', 'fumaorongweimg', 'zsxljs', 'zs_zaixian',
                'DQboai100', 'nanlanglife', 'gh_8f30d04bb79a', 'HP_Finder', 'zsdongsheng', 'tzajfj', 'xiaolan-yhz',
                'zszyqnzyzxh', 'xltvnews', 'jiulifang0760', 'gh_9e7dd82a4e5a', 'SSWW-SSWW', 'zsnanqu', 'zsxlcg',
                'dswsjs', 'PAXL110', 'DADI-xiaolan', 'xlggr2929', 'happy528463', 'gh_33721ab94639', 'xiaolanlibaitang',
                'xlxfcd8317', 'zsbf760', 'tzjb-sport', 'xlxland', 'dszsqwsfw', 'zstztw', 'zsdsfb', 'FSWJ_23401508',
                'gh_c96f4bd16b90', 'HP-Fun', 'jianai_dongqu', 'zsnews0760', 'DC99520', 'dongfeng0760', 'zsql88881863',
                'youpeng2007', 'gh_5b8ad275b3b9', 'sqgadj', 'gh_fd24a6954845', 'nanqugwh', 'wzzs0760', 'yesxiaolan',
                'xiaolan_xiaofang', 'jianyue1208', 'sqqfcjzx', 'minzhonglife', 'TZWGY2015', 'vivi231131288', 'sjgafj',
                'womendefusha', 'xccchwl', 'W18218090479', 'ntqn520', 'ZS_sjdd', 'zsswgswjj', 'dongquzhudian',
                'cscmwyh', 'city528425', 'henglan0760', 'ZSSJYT', 'WGSVPA', 'xlphoto888', 'xiaolan-yiqu', 'wohenlan418',
                'hgsz87666888', 'changyou0760', 'ixl0760', 'XiaoLanSOHO', 'Xiaolan-XBA', 'zssohobar', 'zshd168',
                'zsdsgz', 'zsmytophome', 'scieduce', 'sxliangxindangjian', 'gh_ec9e03e62415', 'zhongshanshaxiwenhua',
                'wanzaishiqi', 'zsgzwj', 'zsxiqu', 'gh_16ee39ea8e96', 'ilove-xiaolan', 'FSWB528434', 'xiaolanton',
                'Jycinema-ZSXL', 'xljinyuan', 'gzdspd', 'wgszzb', 'gh_a4608adcfd67', 'henglanxinxianshi', 'NQ-YEA',
                'love-fusha', 'fww22131767', 'zszydc', 'tzwoman', 'nanlang2015', 'NanlangSQ', 'xlhm_cn',
                'gh_24eb901be9fa', 'xlxbqh', 'zs_dfdd', 'dfweijiju', 'zswgsfb', 'ZSHPFABU', 'SJ-0760', 'sxxf_119',
                'zsxq0760', 'zs-wxd', 'ilovent88', 'haizhoucun', 'Xiaolan_Sports', 'sxzxnjxxfb', 'zsqfnqsg',
                'dqtysq88330848', 'XiaoLanRenShe', 'xl-post', 'yesbanfu', 'XL-haoyeah', 'myzhongshan', 'decathlon_zs',
                'zszqshcnlyyb', 'sakurashow', 'LJ15813152080', 'gh_24c8f486e0d1', 'gh_f0664e66334a', 'xlzdlh',
                'BTKFXLD', 'hesheng86788889', 'WXL528415', 'lqwdt205', 'shaxidangjian', 'xiaolanjcb', 'qfwjwh',
                'ZS163668', 'zsedpw', 'A13923308500', 'yang7815226', 'gh_e65cd4224548', 'sanjiaofb', 'gz718zs',
                'SheratonZhongshan', 'i5200760', 'dqqwsq2016', 'zsdfwgz', 'ZSSJQN2015', 'gh_868ef75b133f', 'HP_9394',
                'seaportcity6688', 'GZH156', 'msxl2010', 'wensa_zs', 'skl88389938', 'zsdswj110', 'longquanchazhuanghs',
                'zs_xiaolan', 'zsbanfu1', 'HLDGZ13420373336', 'SXanjian', 'TanZhouLife', 'zswuguishan', 'zsbtvclub',
                'sx87798470', 'xiaolanjijianjiancha', 'gh_a3f5b9213b35', 'WGSZSmineralwater', 'Fm-BYD', 'anlewo-zszy',
                'zsweimin', 'tanzhoujingxin', 'gh_30cd8c1823cc', 'izs0760', 'gh_01b1eb408b56', 'gh_8f3ade379051',
                'YF85330660', 'xhj2542', 'gh_a31d818da6dc', 'sqguiyuan', 'mjqmyey', 'xizhongzhiguang', 'zgwhblc',
                'zsmisen', 'sanxiangtong', 'udnbkk', 'shangbaoindo', 'euchinesejournal', 'jianhuadaily',
                'shijieribaoph', 'angkortime', 'ukdajiatan', 'ChinesePress', 'qiaowangzhongguo', 'We-sa2cn', 'aucntv',
                'ssdaily', 'sdqbzb', 'zhongwendaobao', 'uk-chinese', 'oushi1983']

    @staticmethod
    def urls_article(html):
        collection_name = 'run_counts'
        items = re.findall('"content_url":".*?,"copyright_stat"', html)
        urls = []
        for item in items:
            url_last = item[15:-18].replace('amp;', '')
            url = 'https://mp.weixin.qq.com' + url_last
            # 部分是永久链接
            if '_biz' in url_last:
                url = re.search('http://mp.weixin.qq.*?wechat_redirect', url_last).group()
                urls.append(url)
                continue
            # 有的文章链接被包含在里面，需再次匹配
            if 'content_url' in url:
                item = re.search('"content_url":".*?wechat_redirect', url).group()
                url = item[15:].replace('amp;', '')
            urls.append(url)
        return urls

    @staticmethod
    def save_to_mysql(entity):
        # 上传数据库
        # log.info('开始上传mysql')
        sql = '''   
                INSERT INTO 
                    account_http(article_url, addon, account, account_id, author, id, title) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)
        '''
        _tuple = (
            entity.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author,
            entity.id,
            entity.title
        )
        try:
            config_mysql = get_mysql_new()
            uploads_mysql(config_mysql, sql, _tuple)
        except Exception as e:
            log.info('数据库上传错误 {}'.format(e))
        # log.info('上传mysql完成')

    @staticmethod
    def save_to_mongo(entity):
        db = mongo_conn()
        entity['collection'] = time_strftime()
        db['daily_collection'].insert(entity)

    @staticmethod
    def create_xml(infos, file_name):
        # log.info('创建xml文件')
        if not os.path.exists(os.path.join(current_dir, 'xml')):
            os.mkdir('xml')
        data = etree.Element("data")
        for k, v in infos.items():
            sub_tag = etree.SubElement(data, k)
            if 'time' in k:
                sub_tag.text = v
                continue
            title_txt = str(v)
            title_txt = etree.CDATA(title_txt)
            sub_tag.text = title_txt
        # dataxml = etree.tostring(data, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=True,
        #                          standalone=None)
        # print(dataxml.decode("utf-8"))
        file_name = os.path.join(current_dir, 'xml', file_name)
        etree.ElementTree(data).write(file_name, encoding='utf-8', pretty_print=True)
        # log.info('完成xml文件')

    def get_tags(self):
        url = 'http://10.194.12.107:8002/GetTag?account={}'.format(self.search_name)
        resp = requests.get(url)
        log.info(resp.text)
        return resp.text

    @staticmethod
    def dedup(account_name):
        date_today = str(datetime.date.today().strftime('%Y%m%d'))
        bottom_url = 'http://60.190.238.178:38010/search/common/weixin/select?sort=Time%20desc&Account={}&rows=2000&starttime=20180430&endtime={}&fl=id,CrawlerType'.format(
            account_name, date_today)
        get_ids = requests.get(bottom_url, timeout=21)
        ids = get_ids.text
        if ids:
            results = json.loads(ids).get('results')
            for item in results:
                if item.get('CrawlerType') == '2' or item.get('CrawlerType') == 2:
                    replace_id = item.get('ID')
                    ids = ids.replace(replace_id, '____')
        return ids

    def run(self):
        count = 0
        while True:
            # count += 1
            # log.info('第{}次'.format(count))
            # ADD_COLLECTION 补采账号  get_account 日常采集； 使用account_list 兼容单个账号和账号列表
            account_list = ADD_COLLECTION if ADD_COLLECTION else self.get_account()
            log.info('一共获取{}账号'.format(len(account_list)))
            if account_list is None:
                log.info('调度队列为空，休眠5秒')
                time.sleep(5)
            for account_name in account_list:
                count += 1
                log.info('第{}次'.format(count))
                # if count < 752:
                #     continue
                try:
                    self.search_name = account_name
                    html_account = self.account_homepage()
                    if html_account:
                        html = html_account
                    else:
                        log.info('{}|找到不到微信号'.format(account_name))
                        continue
                    urls_article = self.urls_article(html)
                    # 确定account信息
                    account = Account()
                    account.name = self.name
                    account.account = account_name
                    account.tags = self.get_tags()
                    account.get_account_id()
                    if not account.account_id:
                        log.info('没有account_id'.format(self.name))
                        # todo 广州市委没有account_id
                        account.account_id = ''
                        continue
                    # 判重
                    ids = self.dedup(account_name) if JUDEG else ''
                    entity = None
                    backpack_list = []
                    for page_count, url in enumerate(urls_article):
                        # if page_count < 15:
                        #     continue
                        article = Article()
                        try:
                            article.create(url, account)
                        except RuntimeError as run_error:
                            log.info('找不到浏览器 {}'.format(run_error))
                        log.info('第{}条 文章标题: {}'.format(page_count, article.title))
                        log.info("当前文章url: {}".format(url))
                        entity = JsonEntity(article, account)
                        log.info('当前文章ID: {}'.format(entity.id))
                        if entity.id in ids and JUDEG is True:
                            log.info('当前文章已存在，跳过0')
                            # continue
                        backpack = Backpack()
                        backpack.create(entity)
                        backpack_list.append(backpack.create_backpack())
                    log.info("开始发包")
                    if entity and backpack_list:
                        entity.uploads(backpack_list)
                        log.info("发包完成")
                except Exception as e:
                    log.exception("解析公众号错误 {}".format(e))
                    if 'chrome not reachable' in str(e):
                        raise RuntimeError('chrome not reachable')
                    continue

    def crack_sougou(self, url):
        log.info('------开始处理未成功的URL：{}'.format(url))
        if re.search('weixin\.sogou\.com', url):
            log.info('------开始处理搜狗验证码------')
            self.driver.get(url)
            time.sleep(2)
            if '搜公众号' in self.driver.page_source:
                log.info('浏览器页面正常' + '直接返回')
                return
            try:
                img = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeImage')))
                log.info('------出现验证码页面------')
                location = img.location
                size = img.size
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                screenshot = self.driver.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                captcha = screenshot.crop((left, top, right, bottom))
                captcha_path = get_captcha_path()
                captcha.save(captcha_path)
                captcha_name = os.path.basename(captcha_path)
                try:
                    captch_input = ''
                    files = {'img': (captcha_name, open(captcha_path, 'rb'), 'image/png', {})}
                    res = requests.post(url=GETCAPTCHA_URL, files=files)
                    res = res.json()
                    if res.get('Success'):
                        captch_input = res.get('Captcha')
                except Exception as e:
                    log.info('搜狗验证码获取失败'.format(e))
                    with open(captcha_path, "rb") as f:
                        filebytes = f.read()
                    captch_input = captch_upload_image(filebytes)
                    # log.info('------验证码：{}------'.format(captch_input))
                log.info('------验证码：{}------'.format(captch_input))
                if captch_input:
                    input_text = self.wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                    input_text.clear()
                    input_text.send_keys(captch_input)
                    submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                    submit.click()
                    time.sleep(2)
                    try:
                        if '搜公众号' not in self.driver.page_source:
                            log.info('验证失败')
                            return
                        log.info('------验证码正确------')
                    except Exception as e:
                        log.info('--22222222----验证码输入错误------ {}'.format(e))
            except Exception as e:
                log.info('------未跳转到验证码页面，跳转到首页，忽略------ {}'.format(e))

        elif re.search('mp\.weixin\.qq\.com', url):
            log.info('------开始处理微信验证码------')
            cert = random.random()
            image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
            respones = self.s.get(image_url, cookies=self.cookies)
            captch_input = captch_upload_image(respones.content)
            log.info('------验证码：{}------'.format(captch_input))
            data = {
                'cert': cert,
                'input': captch_input
            }
            r = self.s.post(image_url, cookies=self.cookies, data=data)
            log.info('------cookies已更新------{}'.format(r.status_code))


if __name__ == '__main__':
    # test = None
    while True:
        try:
            test = AccountHttp()
            log.info("初始化")
            test.run()
            if ADD_COLLECTION:
                log.info('补采完成')
                break
        except Exception as error:
            log.exception('获取账号错误，重启程序{}'.format(error))
        # finally: # 会导致程序崩溃
        #     driver.quit()
