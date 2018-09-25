# -*- coding: utf-8 -*-
import datetime

from lxml import etree


class Ftp(object):
    def __init__(self):
        self.url = 'http://mp.weixin.qq.com/s?timestamp=1536170465&src=3&ver=1&signature=KpIapyYuvtUSvw7wCLI4OSsAm12*lWAnsM*H*8860gITXE6RPKovNzf7cJUk012NVTKNVD-dNFUKJ-z6q3JmLWLXNs80*EJhlPkbpaP9b7Yl-q*WUOYZ9BCJzWnhup4D-ajh0Lr1uqpE-z*wdEhTyVSTMecSQvfaELEnGCRwNdo='
        self.title = '星聚城私人影院特惠包夜仅售68元/晚（可容纳8人）'
        self.content = '【产品亮点】：&nbsp;独立私密空间，最新大片抢先看，免费K歌，免费空调，超洁净的卫生条件，更免费赠送娃娃机抓娃娃，无限抓娃娃'
        self.author = '唐唐假期'
        self.time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.account = 'tangtangaini0516'

    def info_list(self):
        return self.__dict__


def create_xml():
    data = etree.Element("data")
    for k, v in infos.items():
        sub_tag = etree.SubElement(data, k)
        if 'time' in k:
            sub_tag.text = v
            continue
        title_txt = v
        title_txt = etree.CDATA(title_txt)
        sub_tag.text = title_txt
    dataxml = etree.tostring(data, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=True,
                             standalone=None)
    print(dataxml.decode("utf-8"))
    etree.ElementTree(data).write("text2.xml",encoding='utf-8', pretty_print=True)


if __name__ == '__main__':
    f = Ftp()
    infos = f.info_list()
    # print(f.info_list())
    create_xml()
