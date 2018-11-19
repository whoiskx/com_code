# -*- coding: utf-8 -*-
import os
import json
import uuid
import hashlib
import zipfile
import datetime
from lxml import etree
from ftplib import FTP
from config import *


class FtpUtil(object):
    def __init__(self):
        pass

    def ftp_note(self, send_ftp_result):
        note = {
            # 任务ID
            "id": send_ftp_result.get('id'),
            # 任务名
            "name": "微信_{}".format(send_ftp_result.get('author')),
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
            "addon": send_ftp_result.get('time')
        }
        note_json = json.dumps(note, ensure_ascii=False)
        return str(note_json)

    def create_xml(self, send_ftp_result):
        xml_name = self.hash_md5(send_ftp_result.get('url')) + '.xml'
        print('创建XML：{}'.format(xml_name))
        xml_path = os.path.join(XMLS_DIR, xml_name)
        data = etree.Element("data")
        for k, v in send_ftp_result.items():
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
        etree.ElementTree(data).write(xml_path, encoding='utf-8', pretty_print=True)
        return xml_name

    def create_zip(self, xml_name, zip_name, send_ftp_result):
        print('创建ZIP：{}'.format(zip_name))
        zip_path = os.path.join(ZIPS_DIR, zip_name + '.zip')
        with zipfile.ZipFile(zip_path, mode='w') as zf:
            zf_comment = self.ftp_note(send_ftp_result)
            zf.comment = str(zf_comment).encode('gbk')
            xml_path = os.path.join(XMLS_DIR, xml_name)
            zf.write(xml_path, xml_name)

    def hash_md5(self, url):
        m = hashlib.md5()
        m.update(url.encode(encoding="utf-8"))
        return m.hexdigest()

    def send(self, zip_name):
        ftp = FTP(timeout=5)  # 设置变量
        ftp.set_debuglevel = 1
        ftp.connect("110.249.163.246", 21)  # 连接的ftp sever和端口
        ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可
        print('FTP连接成功')
        filepath = datetime.datetime.now().strftime("%Y%m%d")
        filename = zip_name + '.zip'
        zip_path = os.path.join(ZIPS_DIR, filename)
        cmd_str = 'STOR /{}/{}'.format(filepath, filename)
        zip_f = open(zip_path, 'rb')
        send_ok = 0
        try:
            ftp.storbinary(cmd_str, zip_f)
            print('FTP发送成功：{}'.format(zip_name))
            send_ok = 1
        except Exception as e:
            print('FTP超时发送成功：{},{}'.format(zip_name, e))
            send_ok = 1
        finally:
            zip_f.close()
        return send_ok

    def del_xml_zip(self):
        xml_list = os.listdir(XMLS_DIR)
        for xml_name in xml_list:
            xml_path = os.path.join(XMLS_DIR, xml_name)
            os.remove(xml_path)

        zip_list = os.listdir(ZIPS_DIR)
        for zip_name in zip_list:
            zip_path = os.path.join(ZIPS_DIR, zip_name)
            os.remove(zip_path)


my_ftp = FtpUtil()
