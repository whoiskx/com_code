# -*- coding: utf-8 -*-
import os
import json
import time
import uuid
import random
import socket
import hashlib
import zipfile
import datetime
from lxml import etree
from ftplib import FTP
from config import *

print = logger.info


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
            "addon": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
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

    def conn_send(self, cmd_str, zip_f, zip_name, ftp_settings):
        host = ftp_settings.get('host')
        port = ftp_settings.get('port')
        user = ftp_settings.get('user')
        pwd = ftp_settings.get('pwd')
        send_ok = 0
        try:
            ftp = FTP(timeout=3)  # 超时FTP时间设置为3秒
            ftp.set_debuglevel = 1
            ftp.connect(host, port)  # 连接的ftp sever和端口
            ftp.login(user, pwd)  # 连接的用户名，密码如果匿名登录则用空串代替即可
            ftp.storbinary(cmd_str, zip_f)
            ftp.quit()
            send_ok = 1
        except Exception as e:
            print('host：{}，FTP发送失败：{},{}'.format(host, zip_name, e))
            logger.error('host：{}，FTP发送失败：{},{}'.format(host, zip_name, e))

        return send_ok

    def send(self, zip_name):
        filepath = datetime.datetime.now().strftime("%Y%m%d")
        filename = zip_name + '.zip'
        zip_path = os.path.join(ZIPS_DIR, filename)
        cmd_str = 'STOR /{}/{}'.format(filepath, filename)
        zip_f = open(zip_path, 'rb')

        # 河北省委集群
        send_hb_ok = 0
        for i in range(20):
            send_hb_ok = self.conn_send(cmd_str=cmd_str, zip_f=zip_f, zip_name=zip_name, ftp_settings=FTP_HB_TELECOM)
            if send_hb_ok == 0:
                send_hb_ok = self.conn_send(cmd_str=cmd_str, zip_f=zip_f, zip_name=zip_name, ftp_settings=FTP_HB_UNICOM)
            if send_hb_ok == 1:
                print('河北省委集群，FTP发送成功：{}'.format(zip_name))
                break

        # 杭州兴义集群
        send_hz_ok = 0
        for i in range(20):
            ftp_hz_srtting = random.choice(FTP_HZ_list)
            send_hz_ok = self.conn_send(cmd_str=cmd_str, zip_f=zip_f, zip_name=zip_name,
                                        ftp_settings=ftp_hz_srtting.get('FTP_HZ_main'))
            if send_hz_ok == 0:
                send_hz_ok = self.conn_send(cmd_str=cmd_str, zip_f=zip_f, zip_name=zip_name,
                                            ftp_settings=ftp_hz_srtting.get('FTP_HZ_backup1'))
            if send_hz_ok == 0:
                send_hz_ok = self.conn_send(cmd_str=cmd_str, zip_f=zip_f, zip_name=zip_name,
                                            ftp_settings=ftp_hz_srtting.get('FTP_HZ_backup2'))
            if send_hz_ok == 1:
                print('杭州兴义集群，FTP发送成功：{}'.format(zip_name))
                break

        # 关闭文件
        zip_f.close()
        if send_hb_ok == 1 and send_hz_ok == 1:
            return 1
        else:
            return 0

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
