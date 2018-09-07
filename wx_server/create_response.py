# -*- coding: utf-8 -*-
import json

import pymongo
import datetime

conn = pymongo.MongoClient()
db = conn['test']

results = {
    'Success': '',
    'Account': '',
    'Message': '',
    'count': '',
    'ArtPubInfo': '',
    'ActiveDegree': '',
}


def all_artcle():
    # 得到7天内的文章
    articles = []
    for info in db['wx'].find({}, {'Time': 1, '_id': 0}):
        article_datetime = str(info.get('Time'))[:-3]
        article_date = datetime.datetime.fromtimestamp(int(article_datetime))
        day_diff = datetime.datetime.now() - article_date
        if day_diff.days <= 6:
            articles.append(info)
    return articles


def date_count(articles):
    d = []
    for info in articles:
        article_datetime = str(info.get('Time'))[:-3]
        article_date = datetime.datetime.fromtimestamp(int(article_datetime))
        _date = str(article_date.date())
        d.append(_date)
    from collections import Counter
    date_dict = Counter(d)
    day_conut = []
    for k in date_dict.keys():
        day_conut.append({
            'date': k,
            'count': int(date_dict[k])
        })
    return day_conut


def counter_time_range(articles):
    time_info = []
    for info in articles:
        article_datetime = str(info.get('Time'))[:-3]
        article_date = datetime.datetime.fromtimestamp(int(article_datetime))
        _date = str(article_date.time())
        time_info.append(_date)

    trans_quan = {'00:00-06:00': 0, '06:00-09:00': 0, '09:00-12:00': 0, '12:00-15:00': 0, '15:00-18:00': 0,
                  "18:00-21:00": 0, "21:00-00:00": 0}
    for i in time_info:
        t = int(i[:2])
        if 0 <= t < 6:
            trans_quan['00:00-06:00'] += 1
        elif 6 <= t < 9:
            trans_quan['06:00-09:00'] += 1
        elif 9 <= t < 12:
            trans_quan['09:00-12:00'] += 1
        elif 12 <= t < 15:
            trans_quan['12:00-15:00'] += 1
        elif 15 <= t <= 18:
            trans_quan['15:00-18:00'] += 1
        elif 18 <= t <= 21:
            trans_quan['18:00-21:00'] += 1
        elif 21 <= t <= 24:
            trans_quan['21:00-00:00'] += 1
    data = []
    d = {}
    for k, v in trans_quan.items():
        d['time'] = k
        d['activeDegree'] = v
        data.append(d.copy())
    return data


def main():
    # 按天
    articles = all_artcle()
    count = len(articles)
    date_info = date_count(articles)
    time_info = counter_time_range(articles)
    results.update({'ArtPubInfo': date_info, 'count': count, 'ActiveDegree': time_info})
    print(results, type(results))
    print(json.dumps(results))


if __name__ == '__main__':
    main()
