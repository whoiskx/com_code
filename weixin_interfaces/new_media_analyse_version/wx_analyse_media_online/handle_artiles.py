# -*- coding: utf-8 -*-
import json

import datetime
import time
from utils import log

results = {
    'Success': '',
    'Account': '',
    'Message': '',
    'count': '',
    'ArtPubInfo': '',
    'ActiveDegree': '',
}


def all_artcle(article_mongo):
    # 得到7天内的文章
    articles = []
    for info in article_mongo:
        article_datetime = str(info.get('Time'))[:-3]
        if len(article_datetime) == 0:
            log('文章内容错误')
            continue
        article_date = datetime.datetime.fromtimestamp(int(article_datetime))
        # day_diff = datetime.datetime.now() - article_date
        # if day_diff.days <= 6:
        #     articles.append(info)

        day_diff = datetime.date.today() - article_date.date()
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
    date_format = []
    for i in range(7):
        before_date = datetime.date.today() - datetime.timedelta(days=i)
        date_format.append({
            'date': str(before_date),
            'count': 0
        })
    date_format = date_format[::-1]
    for k in day_conut:
        for v in date_format:
            if k.get('date') == v.get('date'):
                v['count'] = k.get('count')
    return date_format


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
    log(time_info)
    # data = []
    # d = {}
    # for k in trans_quan.keys():
    #     # d['time'] = k
    #     # d['activeDegree'] = v
    #     data.append({'time': k, 'activeDegree': trans_quan[k]})
    # 保证顺序 写死
    data = [
        {
            "activeDegree": trans_quan['00:00-06:00'],
            "time": "00:00-06:00"
        },
        {
            "activeDegree": trans_quan['06:00-09:00'],
            "time": "06:00-09:00"
        },
        {
            "activeDegree": trans_quan['09:00-12:00'],
            "time": "09:00-12:00"
        },
        {
            "activeDegree": trans_quan['12:00-15:00'],
            "time": "12:00-15:00"
        },
        {
            "activeDegree":trans_quan['15:00-18:00'],
            "time": "15:00-18:00"
        },
        {
            "activeDegree": trans_quan['18:00-21:00'],
            "time": "18:00-21:00"
        },
        {
            "activeDegree": trans_quan['21:00-00:00'],
            "time": "21:00-00:00"
        }
    ]
    log(data)
    return data


def handle(articles_info):
    # 按天
    articles = all_artcle(articles_info)
    count = len(articles)
    date_info = date_count(articles)
    time_info = counter_time_range(articles)
    results.update({'ArtPubInfo': date_info, 'count': count, 'ActiveDegree': time_info})
    # print(results, type(results))
    # print(json.dumps(results))
    return results


if __name__ == '__main__':
    handle()
    # get_data_format()
    # date_format = []
    # start_date = datetime.date.today()
    # for i in range(7):
    #     before_date = datetime.date.today() - datetime.timedelta(days=i)
    #     date_format.append({
    #         'data': str(before_date),
    #         'count': 0
    #     })
    # print(date_format
