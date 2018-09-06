# -*- coding: utf-8 -*-
import pymongo
import datetime

conn = pymongo.MongoClient()
db = conn['test']

day = datetime.datetime.now()
print(day)
day_seven_ago = day - datetime.timedelta(days=7)
print(day_seven_ago)
day_seven_ago_date = day_seven_ago.date()
print(day_seven_ago_date)

article_in_seven = []
for info in db['wx'].find({}, {'Time': 1, '_id': 0}):
    article_datetime = str(info.get('Time'))[:-3]
    article_date = datetime.datetime.fromtimestamp(int(article_datetime))
    day_diff = day - article_date
    if day_diff.days <= 6:
        article_in_seven.append(info)

print(article_in_seven)
count = len(article_in_seven)

results = {
    'Success': True,
    'Account': "NF_Daily",
    'Message': "",
    'count': count,
    'ArtPubInfo': {
        'count': count,
        'data': []
    },
    'ActiveDegree': {
        'data': []
    }
}

day_conut = []
now = datetime.datetime.now()
for i in range(7):
    day_conut.append({
        'date': str((day - datetime.timedelta(days=i)).date()),
        'count': 0,
    })

print(day_conut)


d = {}

for info in article_in_seven:
    article_datetime = info.get("Time")
    article_datetime = str(info.get('Time'))[:-3]
    article_date = datetime.datetime.fromtimestamp(int(article_datetime))
    # print(article_date)
    _date = str(article_date.date())
    print(_date, type(_date))
    if len(d) == 0:
        dd['date'] = _date
        dd['count'] = 0
        d.append(dd)
    for dd in d:
        if dd.get('date') == _date:
            t = int(dd.get('count'))
            t += 1
            dd['count'] = t
        else:
            dd['date'] = _date
            dd['count'] = 0
            d.append(dd)
print(d)