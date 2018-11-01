# -*- coding:utf-8 -*-
import base64
import functools
import json
import uuid

from bson import json_util


def singleton(func):
    """线程不安全的单例模式"""

    @functools.wraps(func)
    def wrapper(*args, **kw):
        if not hasattr(func, 'attr'):
            func.attr = func(*args, **kw)
        return func.attr

    return wrapper


def create_guid():
    return str(uuid.uuid1()).decode('utf-8').lower()


def json2pyobj(json_str, encoding="utf-8"):
    """能将datetime反序列化"""
    return json.loads(json_str, object_hook=json_util.object_hook, encoding=encoding)


def pyobj2json(py_obj, encoding="utf-8"):
    """能将datetime序列化"""
    return json.dumps(py_obj, default=json_util.default, encoding=encoding)


def base64_to_string(base64_str):
    return base64.standard_b64decode(base64_str)


def string_to_base64(string):
    return base64.standard_b64encode(string)


def get_md5(string):
    import hashlib
    hash_md5 = hashlib.md5(string)
    return hash_md5.hexdigest()


def is_aliyun():
    import os
    return os.path.exists('/usr/local/cloudmonitor/')
