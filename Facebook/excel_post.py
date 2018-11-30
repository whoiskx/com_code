from openpyxl import Workbook
from setting import urun

wb = Workbook()
sheet = wb.active

data = urun.facebook_group_members
first_row = ['小组成员', '所在地', '来自', '工作', '学历', '性别', '成员主页']
sheet.append(first_row)
for i in data.find():
    if '曾' in i.get('job'):
        i['degree'] = i.get('job')
        i['job'] = ""
    elif '就读于' in i.get('job'):
        i['degree'] = i.get('job')
        i['job'] = ""
    elif '所在地' in i.get('job'):
        i['location'] = i.get('job')
        i['job'] = ""
    elif '来自' in i.get('job'):
        i['come_form'] = i.get('job')
        i['job'] = ""
    i = [i.get("account_name"), i.get('location'), i.get('come_form'), i.get('job'),
         i.get('degree'), i.get('sex'), i.get("home_page")]
    # i = [i.get("name"), i.get('time'), i.get('praise'), i.get('share'), i.get('content'),
    #      i.get('year'), i.get('month'), i.get("day")]
    sheet.append(i)
wb.save(r"D:\group_members7.xlsx")
