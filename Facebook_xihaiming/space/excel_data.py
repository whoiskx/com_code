from openpyxl import Workbook
from setting import urun

wb = Workbook()
sheet = wb.active

data = urun.spacedata280
save = urun.spacedata_zzzzz
first_row = ['具体时间', '原创/非原创', '留言数', '分享数', '点赞数', '年', '月', '日', '小时', '内容',]
sheet.append(first_row)
for i in data.find():
    save.insert(i.pop('_id'))
    "{'time': '1月15日', 'original': '原创', 'comment_sum': 0, 'share': '', 'praise': '8', 'content': '', 'year': 2018, 'month': '1', 'day': '15日'}"
    i = [i.get("time"), i.get('original'), i.get('comment_sum'), i.get('share'),
         i.get('praise'), i.get("year"), i.get("month"), i.get("day"),i.get('hours'), i.get('content')]
    # i = [i.get("name"), i.get('time'), i.get('praise'), i.get('share'), i.get('content'),
    #      i.get('year'), i.get('month'), i.get("day")]
    sheet.append(i)

data = urun.spacedata_end1
for i in data.find():
    save.insert(i.pop('_id'))
    "{'time': '1月15日', 'original': '原创', 'comment_sum': 0, 'share': '', 'praise': '8', 'content': '', 'year': 2018, 'month': '1', 'day': '15日'}"
    i = [i.get("time"), i.get('original'), i.get('comment_sum'), i.get('share'),
         i.get('praise'), i.get("year"), i.get("month"), i.get("day"),i.get('hours'), i.get('content')]
    # i = [i.get("name"), i.get('time'), i.get('praise'), i.get('share'), i.get('content'),
    #      i.get('year'), i.get('month'), i.get("day")]
    sheet.append(i)

data = urun.spacedata_end2
for i in data.find():
    save.insert(i.pop('_id'))
    "{'time': '1月15日', 'original': '原创', 'comment_sum': 0, 'share': '', 'praise': '8', 'content': '', 'year': 2018, 'month': '1', 'day': '15日'}"
    i = [i.get("time"), i.get('original'), i.get('comment_sum'), i.get('share'),
         i.get('praise'), i.get("year"), i.get("month"), i.get("day"),i.get('hours'), i.get('content')]
    # i = [i.get("name"), i.get('time'), i.get('praise'), i.get('share'), i.get('content'),
    #      i.get('year'), i.get('month'), i.get("day")]
    sheet.append(i)

# wb.save(r"D:\space_data20.xlsx")