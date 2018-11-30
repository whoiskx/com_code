# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import re
import uuid
import zipfile
from ftplib import FTP

from lxml import etree


class Ftp(object):
    def __init__(self):
        self.id = 126765002
        self.url = 'https://mp.weixin.qq.com/s?timestamp=1537947825&src=3&ver=1&signature=v6SVkUGz4*u2ygI2jDM64P0h6XSPXRMW0bCBgdC6NxpKJp1SL*6y3zXI*Gtm44PzQ6CMB4MyBnJKjaLC0kwlAauO7Kcf4LSq63pJ8ACjnjfA3verqPIh3HGvTirk2VzruaoHOcbC2*mZEiWfNMt7A2PbDI5eWsoTOS-Z*1bHjD4='
        self.title = '十一国庆小长假，热门旅游线路大汇总'
        self.content = '热门旅游线路大汇总'
        self.author = '唐唐假期'
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.account = 'tangtangaini0516'

    def hash_md5(self, s):
        m = hashlib.md5()
        m.update(s.encode(encoding="utf-8"))
        return m.hexdigest() + '.xml'

    def ftp_dict(self):
        return self.__dict__

    def ftp_note(self):
        note = {
            # 任务ID
            "id": self.id,
            # 任务名
            "name": "微信_{}".format(self.author),
            # 网站名
            "groupName": "微信",
            # 是否境外站点
            "overseas": False,
            # 站点类型
            "category": 14,
            # 站点语言
            "language": 1,
            # 数据类型
            "structure": 1,
            # PageRank
            "pr": 6,
            # 标签id
            "tagID": 0,
            # 是否是首页
            "top": False,
            # 是否是首页
            "home": 0,
            "channel": 20,
            # 采集时间
            "addon": self.time
        }
        note_json = json.dumps(note, ensure_ascii=False)
        return str(note_json)


def create_xml(file_name):
    data = etree.Element("data")
    for k, v in infos.items():
        sub_tag = etree.SubElement(data, k)
        if 'time' in k:
            sub_tag.text = v
            continue
        title_txt = str(v)
        title_txt = etree.CDATA(title_txt)
        sub_tag.text = title_txt
    dataxml = etree.tostring(data, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=True,
                             standalone=None)
    print(dataxml.decode("utf-8"))
    etree.ElementTree(data).write(file_name, encoding='utf-8', pretty_print=True)


def create_zip(file_name, f):
    print('creating archive')
    zf_name = str(uuid.uuid1())
    with zipfile.ZipFile('{}.zip'.format(zf_name), mode='w') as zf:
        zf_comment = f.ftp_note()
        zf.comment = str(zf_comment).encode('gbk')
        zf.write(file_name)


def main():
    ftp = FTP()  # 设置变量
    ftp.connect("110.249.163.246", 21)  # 连接的ftp sever和端口
    ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可
    print('ftp连接成功')
    filepath = datetime.datetime.now().strftime("%Y%m%d")
    filename = '37eadc0a-c160-11e8-8b1e-fc017c3bd1b0.zip'
    cmd = 'STOR /{}/{}'.format(filepath, filename)
    ftp.storbinary(cmd, open(filename, 'rb'))
    print('end')


if __name__ == '__main__':
    f = Ftp()
    infos = f.ftp_dict()
    # print(f.info_list())
    file_name = f.hash_md5(f.url)
    create_xml(file_name)
    create_zip(file_name, f)
