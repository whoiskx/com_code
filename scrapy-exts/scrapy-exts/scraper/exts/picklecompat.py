"""A pickle wrapper module with protocol=-1 by default.

used by
-------
queue.py

"""


import pickle


def loads(s):
    return pickle.loads(s)


def dumps(obj):
    return pickle.dumps(obj, protocol=-1)
