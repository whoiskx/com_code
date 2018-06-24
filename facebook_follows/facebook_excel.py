from openpyxl import Workbook
from setting import urun

wb = Workbook()
sheet = wb.active

data = urun.facebook
for i in data.find():
    i = [i.get("account_name"), i.get('home_page'), i.get('location'), i.get('come_form'), i.get('job'),
         i.get('followers'), i.get('degree'), i.get('sex'), ]
    sheet.append(i)
wb.save(r"D:\example3.xlsx")
