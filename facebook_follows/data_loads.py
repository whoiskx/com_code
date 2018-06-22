# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import json

from setting import db

data = db.facebook
print(data.find())
results = []
for i in data.find():
    results.append(i)
print(results)