import sys
import time
import string

from lxml import etree

# 设置默认字符集为UTF8 不然有些时候转码会出问题


class Ftp(object):
    def __init__(self):
        self.url = '2'
        self.title = '3'
        self.content = ''
        self.author = ''
        self.time = ''
        self.account = ''

    def info_list(self):
        return self.__dict__


def create_xml():
    data = etree.Element("data")
    for k, v in infos.items():
        sub_tag = etree.SubElement(data, k)
        title_txt = v
        title_txt = etree.CDATA(title_txt)
        sub_tag.text = title_txt
    dataxml = etree.tostring(data, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=True,
                             standalone=None)
    print(dataxml.decode("utf-8"))
    etree.ElementTree(data).write("text.xml", pretty_print=True)


if __name__ == '__main__':
    f =Ftp()
    infos = f.info_list()
    # print(f.info_list())
    create_xml()

