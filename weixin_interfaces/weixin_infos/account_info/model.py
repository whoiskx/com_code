# `ID` int(10) unsigned NOT NULL COMMENT '自增id',
#   `Name` varchar(50) DEFAULT NULL COMMENT '名微信公众号称',
#   `Account` varchar(50) DEFAULT NULL COMMENT '微信公众号账号',
#   `Biz` varchar(50) DEFAULT NULL COMMENT '微信链接参数',
#   `Url` varchar(300) DEFAULT NULL COMMENT '微信url',
#   `ScheduleID` int(10) unsigned DEFAULT NULL COMMENT '调度id',
#   `Interval` smallint(5) unsigned DEFAULT NULL COMMENT '采集间隔时间，单位分钟',
#   `LabelID` tinyint(3) unsigned DEFAULT NULL COMMENT '类型：8：全局采集，13：三合一采集',
#   `DestinationID` smallint(5) unsigned DEFAULT NULL COMMENT 'Destinationid(暂时无用)',
#   `Authentication` varchar(500) DEFAULT NULL COMMENT '认证(公司名)',
#   `Introduction` varchar(300) DEFAULT NULL COMMENT '微信公众号介绍，采集而来',
#   `LogoPath` varchar(150) DEFAULT NULL COMMENT '头像图片路径',
#   `Weight` tinyint(3) unsigned DEFAULT NULL COMMENT '任务权重（暂时没用）',
#   `AddOn` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
#   `Pause` tinyint(1) DEFAULT NULL COMMENT '是否暂停：0:不暂停，1：暂停',
#   `UpdateOn` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   `CollectionTime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最近采集时间，客户端采集该账号完成会更新此时间',
#   `Status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态（1正常 0删除）',
#   `CreateUserID` varchar(50) DEFAULT NULL COMMENT '添加人ID',
#   `CreateUserName` varchar(50) DEFAULT NULL COMMENT '添加人名称',
#   `UpdateUserID` varchar(50) DEFAULT NULL COMMENT '最近修改人ID',
#   `UpdateUserName` varchar(50) DEFAULT NULL COMMENT '最近修改人名称',
import pymysql
from config import get_mysql_new
from utils import log


class Account(object):
    def __init__(self, info):
        # self.ID = ''
        self.Name = info.get('Name')
        self.Account = info.get('Account')
        self.Biz = info.get('Biz')
        self.Url = ''
        # self.ScheduleID = ''
        self.Interval = 1440
        self.LabelID = 8
        # self.DestinationID = ''
        self.Authentication = info.get('Certification')
        self.Introduction = info.get('Feature')
        self.LogoPath = info.get('ImageUrl')
        # self.Weight = ''
        self.AddOn = ''
        self.Pause = 0
        # self.UpdateOn = ''
        # self.CollectionTime = ''
        self.Status = 1
        # self.CreateUserID = ''
        # self.CreateUserName = ''
        # self.UpdateUserID = ''
        # self.UpdateUserName = ''

    def to_mysql_weixin(self):
        config_mysql_old = get_mysql_new()
        db = pymysql.connect(**config_mysql_old)
        cursor = db.cursor()
        try:
            sql_insert = """    
                               INSERT INTO weixin (`Name`, Account, Biz, `Interval`, LabelID, Authentication, Introduction, LogoPath, Pause, Status)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql_insert, (
                self.Name,
                self.Account,
                self.Biz,
                self.Interval,
                self.LabelID,
                self.Authentication,
                self.Introduction,
                self.LogoPath,
                self.Pause,
                self.Status

            ))
            db.commit()
            log('插入数据成功 {}'.format(self.Name))
            # log("当前账号id为0 需要添加 {}".format(self.name))
        except Exception as e:
            log('插入数据错误 {} '.format(e))
            db.rollback()


if __name__ == '__main__':
    info = {'Name': '河北省明德公益基金会', 'Account': 'gh_4d3319272897',
            'Feature': '河北省明德公益基金会旨在资助贫困地区或欠发达地区教育事业,以及贫困家庭的孩子完成学业.同时对孤儿院给予资助,改善其环境,提高孤儿们生活水平.此外还将资助贫困地区孤寡老人,改善老人们的生活质量.',
            'Certification': '河北省明德公益基金会',
            'ImageUrl': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt2BhFXTECL9n58Fgr9h40F8',
            'Biz': 'MzU1NTQ5MTE3MQ=='}
    _account = Account(info)
    _account.to_mysql_weixin()
