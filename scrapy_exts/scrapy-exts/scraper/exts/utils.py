import six
import xml.etree.ElementTree as ET
from io import StringIO
import hashlib


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


def sql_query():
    sqls = ("SELECT ge.id, ge.Name, ge.groupid, gr.name AS groupnmae, ge.url, c.template AS template, "
            "ge.overseas, ge.category, ge.language, ge.coverage, ge.weight, ge.homepage, ge.channel, "
            "ge.country FROM `group` gr, general ge, custom c WHERE ge.groupID = gr.ID AND ge.customid = c.id")
    return sqls


def sql_query_with_ftp():
    sqls = ("SELECT ge.id, ge.Name, ge.groupid, gr.name AS groupnmae, ge.url, c.template AS template, "
            "ge.overseas, ge.category, ge.language, ge.coverage, ge.weight, ge.homepage, ge.channel, "
            "ge.country, s.config FROM `group` gr, general ge, custom c, `storage` s    "
            "WHERE ge.groupID = gr.ID AND ge.customid = c.id AND s.pause = 0")
    return sqls


def sql_tuple2dict_with_ftp(record):
    """ accept a raw sql record and transform to a dict. 
    
    Note:
        Order matters! Order must be same as `<function> sql_query`
    """
    return {'id': record[0],
            'name': record[1],
            'groupID': record[2],
            'groupName': record[3],
            'url': record[4],
            'template': record[5],
            'overseas': True if record[6] == b'\x01' else False,
            'category': record[7],
            'language': record[8],
            'coverage': record[9] if record[9] else 0,
            'weight': record[10] if record[10] else 0,
            'homepage': record[11] if record[11] else 0,
            'channel': record[12],
            'country': record[13],
            'ftp': record[14]}


def sql_tuple2dict(record):
    """ accept a raw sql record and transform to a dict. 
    
    Note:
        Order matters! Order must be same as `<function> sql_query`
    """
    return {'id': record[0],
            'name': record[1],
            'groupID': record[2],
            'groupName': record[3],
            'url': record[4],
            'template': record[5],
            'overseas': True if record[6] == b'\x01' else False,
            'category': record[7],
            'language': record[8],
            'coverage': record[9] if record[9] else 0,
            'weight': record[10] if record[10] else 0,
            'homepage': record[11] if record[11] else 0,
            'channel': record[12],
            'country': record[13]}


def sql_template2xpath(template):
    """accept a recordict return by `<function> sql_tuple2dict`. """
    xml = StringIO(template)
    root = ET.parse(xml).getroot()
    # hard code attribute `name`
    xpath = {node.get('name'): node.text for node in root}
    return xpath


def url2md5(url):
    md5 = hashlib.md5()
    md5.update(url.encode())
    return md5.hexdigest()


def sql_weibo_with_ftp():
    sqls = 'SELECT wb.Name, wb.Site, wb.addOn, wb.UID, s.config FROM weibo wb, `storage` s WHERE wb.site = 1 AND s.pause = 0;'
    return sqls


def sql_weibo_tuple2dict_with_ftp(record):
    return {
        'Name': record[0],
        'Site': record[1],
        'Time': record[2],
        'uid': record[3],
        'ftp': record[4],
    }
