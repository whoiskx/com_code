""" connection.py 
use
---
defaults.py

used by
-------
dupefilter.py
pipelines.py
scheduler.py

functions
---------
1. get_redis_from_setting mainly handle params
2. get_redis using params to instantize a redis object.
3. get_mysql_from_setting mainly handle params
4. get_mysql using params to instantize a mysql object.

"""

import six

from scrapy.utils.misc import load_object

from . import defaults


# Shortcut maps 'setting name' -> 'paramater name'.
SETTINGS_PARAMS_MAP = {
    'REDIS_URL': 'url',
    'REDIS_HOST': 'host',
    'REDIS_PORT': 'port',
    'REDIS_ENCODING': 'encoding',
}


def get_redis_from_settings(settings):
    """Returns a redis client instance from given Scrapy settings object.

    This function uses ``get_client`` to instantiate the client and uses
    ``defaults.REDIS_PARAMS`` global as defaults values for the parameters. You
    can override them using the ``REDIS_PARAMS`` setting.

    Parameters
    ----------
    settings : Settings
        A scrapy settings object. See the supported settings below.

    Returns
    -------
    server
        Redis client instance.

    Other Parameters
    ----------------
    REDIS_URL : str, optional
        Server connection URL.
    REDIS_HOST : str, optional
        Server host.
    REDIS_PORT : str, optional
        Server port.
    REDIS_ENCODING : str, optional
        Data encoding.
    REDIS_PARAMS : dict, optional
        Additional client parameters.

    """
    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    return get_redis(**params)


# Backwards compatible alias.
from_settings = get_redis_from_settings


def get_redis(**kwargs):
    """Returns a redis client instance.

    Parameters
    ----------
    redis_cls : class, optional
        Defaults to ``redis.StrictRedis``.
    url : str, optional
        If given, ``redis_cls.from_url`` is used to instantiate the class.
    **kwargs
        Extra parameters to be passed to the ``redis_cls`` class.

    Returns
    -------
    server
        Redis client instance.

    """
    redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
    url = kwargs.pop('url', None)
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)

# map mysql settings to function parameters
MYSQL_SETTINGS_PARAMS_MAP = {
    'MYSQL_HOST': 'host',
    'MYSQL_PORT': 'port',
    'MYSQL_USER': 'user',
    'MYSQL_PASSWORD': 'password',
    'MYSQL_DATABASE': 'database',
    'MYSQL_ENCODING': 'charset' ,
}

def get_mysql_from_settings(settings):
    """using defaults settings or user-define settings 
    in Project/settings.py"""
    params = defaults.MYSQL_PARAMS.copy()

    for source, dest in MYSQL_SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``mysql_cls`` to be a path to a class.
    if isinstance(params.get('mysql_cls'), six.string_types):
        params['mysql_cls'] = load_object(params['mysql_cls'])

    params['port'] = int(params['port'])
    return get_mysql(**params)

def get_mysql(**kwargs):
    """Returns a mysql client instance.

    Parameters
    ----------
    **kwargs
        Extra parameters to be passed to the ``redis_cls`` class.

    Returns
    -------
    server
        Mysql client instance.

    """
    mysql_cls = kwargs.pop('mysql_cls', defaults.MYSQL_CLS)
    return mysql_cls(**kwargs)