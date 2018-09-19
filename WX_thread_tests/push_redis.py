# -*- coding: utf-8 -*-
import redis


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(db=8)
        self.queue = 'analyse'

    def prodcons(self, account):
        self.rcon.lpush(self.queue, account)

# chaoliunvren88 2015年的文章
account = ['novonordisktsyds', 'shengxiao_55', 'dqsj66', 'cy2915', 'sschaoliu',
           'duzhe3650', 'mlketang', 'nnm668', 'weicnjr', 'gh_670031e375a0', 'qiyangtongcom', 'sbsb65', 'xxooshimei',
           'gh_4aba38755586', 'qqwrd007', 'jrhycom', 'bxlcwcom', 'nanren94188', 'zyyst99', 'mykd2014', 'pm6668888',
           'immissi', 'nvren3778', 'zhs66688', 'wpt886', 'nv5788', 'lizhi743', 'yyoo778', 'hulianwangtoutiao',
           'niudaoouba', 'scgc1213', 'fcwm520', 'hanguoxingyule', 'EXOlll', 'remen366', 'inernv', 'xchangshi',
           'mmmfff66', 'xgrasx', 'YWTVshopping', 'shmeishizixun', 'gh_007b238ac9b0', 'rqxxdt', 'lehuozsy',
           'yieredu_daai', 'gzxldsm', 'QTXM777', 'vipnannv', 'kawa01', 'ichuanyidaban', 'charming-shanghai', 'vipy866',
           'meng638', 'tpylhlc', 'caijingxinwenyan', 'abcmedia', 'kzg1213', 'xuezhishi121', 'huakui2', 'gdboy520',
           'meirongbar', 'GZ_2898168', 'xinxingfengqingwang', 'gh_477767e8f367', 'mcq886', 'av4550', 'keyi-gz',
           'Metro1071', 'mdwm-luu', 'chi-_-huo', 'tjfood', 'singeat8', 'shenghuocswx', 'zjgdfcwz', 'tongledao2011',
           'weanswer', 'yg8292311', 'gh_708484f5c1c1', 'metro_st121', 'DukesFashion2014', 'gh_55f18d173d5b',
           'qdtimephoto', 'wendengsheying', 'duzhecn', 'AotemanLife', 'zhs6667', 'gh_43707986b418', 'SmartDiary',
           'wxkj6868', 'ToneStudio', 'gh_151468fc305a', 'ceceapp', 'aibeipiao', 'golfimpress-lee', 'www0550com',
           'muyingwenda', 'paceglobal']
t = Task()
for i, a in enumerate(account):
    t.prodcons(a)
    # break
    # if i > 5:
    #     break
    print(i)
print('end')