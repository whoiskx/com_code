""" pipelines.py implements a RedisPipelines
use
---
connection.py
defaults.py

functions
---------
handle the item, including encode item as json-format
and write into redis server it holds
__init__ init a server called by from_settings
process_item is the core function, _process_item store
items into redis server
"""
import zipfile
import json
import xml.dom.minidom as dom
import ftplib
import re
import os
from uuid import uuid1

from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

from . import connection, defaults
from .utils import url2md5
from .weiboUtils import time_format

default_serialize = ScrapyJSONEncoder().encode


class RedisPipeline(object):
    """Pushes serialized item into a redis list/queue

    Settings
    --------
    REDIS_ITEMS_KEY : str
        Redis key where to store items.
    REDIS_ITEMS_SERIALIZER : str
        Object path to serializer function.

    """

    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        """Initialize pipeline.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        key : str
            Redis key where to store items.
        serialize_func : callable
            Items serializer function.

        """
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.

        Override this function to use a different key depending on the item
        and/or spider.

        """
        return self.key % {'spider': spider.name}


class ZipfilePipeline(object):

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        xmlname    = self._get_xmlname(item['url'])
        xmlcontent = self._get_xmlcontent(item['xmlcontent'])
        comment    = self._get_comment(item['comment'])

        zfname = "%s.zip" % uuid1() 
        with zipfile.ZipFile(zfname, mode='w') as zf:
            zf.writestr(xmlname, xmlcontent)
            zf.comment = comment
        return item

    def _get_xmlname(self, url):
        return url2md5(url) + '.xml'

    def _get_xmlcontent(self, content):
        doc = dom.Document()
        root = doc.createElement('data')
        doc.appendChild(root)
        # hard coding
        nodenames = {"id", "name", "url", "title", "content", "author", 
                     "from", "time", "image"}
        for nodename in nodenames:
            node = doc.createElement(nodename)
            if nodename in content:
                text = content[nodename]
                if type(text) != type('stringType'):
                    text = "|".join(text)
                cdata = doc.createCDATASection(text)
                node.appendChild(cdata)
            root.appendChild(node)
        return doc.toprettyxml()
        
    def _get_comment(self, comment):
        # pop out scrapy items
        try:
            comment.pop('download_latency')
            comment.pop('download_slot')
            comment.pop('download_timeout')
        except:
            pass
        comment_str = json.dumps(comment, ensure_ascii=None, separators=(",",":"))
        return comment_str.encode('gbk')

class ZipfilePipelineWithFTP(ZipfilePipeline):

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        xmlname    = self._get_xmlname(item['url'])
        xmlcontent = self._get_xmlcontent(item['xmlcontent'])
        comment    = self._get_comment(item['comment'])
        ftp        = self._get_ftp(item['ftp'])

        # FIXME: send zip file without creating it locally
        zfname = "%s.zip" % uuid1() 
        with zipfile.ZipFile(zfname, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(xmlname, xmlcontent)
            zf.comment = comment
        try:
            with open(zfname, 'rb') as f:
                ftp.storbinary("STOR `%s`" % zfname, f, 1024)
        except Exception as e:
            print(e)    
        finally:
            os.remove(zfname)
            ftp.close()

        return item

    def _get_ftp(self, ftpstr):
        host, _, user, passwd = re.split('[;:]', ftpstr)
        return ftplib.FTP(host=host, user=user, passwd=passwd)


class WeiboPipelineWithFTP(ZipfilePipelineWithFTP):
    
    def _get_xmlcontent(self, content):
        doc = dom.Document()
        root = doc.createElement('Blog')
        root.setAttribute('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
        root.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        doc.appendChild(root)

        def xml_textNode(name, text):
            if type(text) != type('text'):
                text = str(text)
            node = doc.createElement(name)
            textNode = doc.createTextNode(text)
            node.appendChild(textNode)
            root.appendChild(node)

        def xml_emptyNode(name):
            node = doc.createElement(name)
            root.appendChild(node)

        # hard coding
        xml_emptyNode('person')
        xml_textNode('place', ' '.join([content['User']['province'], content['User']['city']]))
        xml_emptyNode('companies')
        xml_emptyNode('brands')
        xml_textNode('content', content['content'])
        xml_textNode('quote', content['quote'])
        xml_textNode('quoteID', content.get('quoteID', ""))
        xml_textNode('qurl', content['qurl'])
        xml_textNode('author', content['author'])
        xml_textNode('time', content['time'])
        xml_textNode('url', content['url'])
        xml_textNode('authorID', content['authorID'])
        xml_textNode('quoteAuthorID', content.get('quoteAuthorID', ""))
        xml_textNode('imageUrl', content['imageUrl'])
        xml_textNode('transtmis', content['transtmis'])
        xml_textNode('comments', content['comments'])
        xml_textNode('blogid', content['blogid'])
        xml_textNode('uid', content['uid'])
        xml_textNode('imgUrl', content['imgUrl'])
        xml_textNode('imgCounts', content['imgCounts'])
        xml_textNode('qimgCounts', content['qimgCounts'])
        xml_textNode('quoteImgUrl', content['quoteImgUrl'])
        xml_textNode('qouteAuthor', content['quoteAuthor'])
        xml_textNode('quoteUid', content['quoteUid'])
        xml_textNode('quoteTime', content['quoteTime'])
        xml_textNode('source', content['source'])

        # 处理user
        userNode = doc.createElement('User')
        user = content['User']
        def add_userNode(name, text):
            # helper function
            if type(text) != type('text'):
                text = str(text)
            text = 'true' if text == 'True' else text
            text = 'false' if text == 'False' else text
            node = doc.createElement(name)
            textNode = doc.createTextNode(text)
            node.appendChild(textNode)
            userNode.appendChild(node)

        add_userNode('name', user['name'])
        add_userNode('url', user['url'])
        add_userNode('headurl', user['headurl'])
        add_userNode('province', user['province'])
        add_userNode('city', user['city'])
        add_userNode('follows', user['follows'])
        add_userNode('fans', user['fans'])
        add_userNode('posts', user['posts'])
        add_userNode('favourites', user['favourites'])
        add_userNode('descrption', user['description'])
        add_userNode('vip', user['vip'])
        add_userNode('verifiedReason', user['verifiedReason'])
        add_userNode('verified_type', user['verified_type'])
        add_userNode('registerTime', time_format(user['registerTime']))
        add_userNode('sex', user['sex'])
        add_userNode('uid', user['uid'])
        add_userNode('site', user['site'])
        add_userNode('tags', user['tags'])
        add_userNode('nature', user['nature'])
        add_userNode('qqnum', 0)
        add_userNode('addon', '0001-01-01T00:00:00')
        add_userNode('atTotal', 0)
        add_userNode('listen', 0)
        add_userNode('audience', 0)
        root.appendChild(userNode)

        phraseNode = doc.createElement('phrase')
        def add_phraseNode(name, text):
            if type(text) != type('text'):
                text = str(text)
            node = doc.createElement(name)
            textNode = doc.createTextNode(text)
            node.appendChild(textNode)
            phraseNode.appendChild(node)
        add_phraseNode('content', "")
        add_phraseNode('author', content['author'])
        add_phraseNode('quote', "")
        add_phraseNode('qauthor', "")
        add_phraseNode('tags', "")
        add_phraseNode('description', user['description'])
        add_phraseNode('verifiedReason', user['verifiedReason'])
        root.appendChild(phraseNode)

        xml_textNode('attitudes_count', content['attitudes_count'])
        xml_textNode('favorite_count', user['favourites'])
        
        timeList = doc.createElement('timeList')
        dateTime = doc.createElement('dateTime')
        dateTime.appendChild(doc.createTextNode(content['time']))
        timeList.appendChild(dateTime)
        root.appendChild(timeList)

        quoteTimeList = doc.createElement('quoteTimeList')
        dateTime = doc.createElement('dateTime')
        dateTime.appendChild(doc.createTextNode(content['time']))
        quoteTimeList.appendChild(dateTime)
        root.appendChild(quoteTimeList)

        md5s = doc.createElement('md5s')
        md5s.appendChild(doc.createElement("shortUrlMD5"))
        md5s.appendChild(doc.createElement("topicNameMD5"))
        md5s.appendChild(doc.createElement('qblogidMd5'))
        root.appendChild(md5s)

        # FIXME
        xml_textNode('keywords', "")
        xml_textNode('shortUrlInfo', "")
        xml_textNode('qshortUrlInfo', "")

        atSomeone = doc.createElement('atSomeone')
        atSomeone.appendChild(doc.createElement('names'))
        atSomeone.appendChild(doc.createElement('keyword'))
        root.appendChild(atSomeone)

        xml_textNode('picUrls', content['picUrls'])
        xml_textNode('qpicUrls', content['qpicUrls'])
        xml_textNode('isComments', 0)
        xml_textNode('PlaceSeat', "")
        xml_textNode("Paragraphs", 0)
        xml_textNode("IsGarbage", 0)
        xml_textNode('Positive', 0)
        xml_textNode('Negative', 0)

        return doc.toprettyxml()

    def _get_comment(self, comment):
        # pop out scrapy items
        try:
            comment.pop('download_latency')
            comment.pop('download_slot')
            comment.pop('download_timeout')
            comment.pop('depth')
        except:
            pass
        
        comment['Time'] = comment['Time'].strftime("%Y-%m-%d %H:%M:%S")
        comment['Type'] = 1
        comment['Task'] = url2md5(comment['Name'])
        comment_str = json.dumps(comment, ensure_ascii=None, separators=(",",":"))
        comment_str = re.sub('["{}]', "", comment_str)
        return comment_str.encode('gbk')