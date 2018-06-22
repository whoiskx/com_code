from openpyxl import Workbook
from setting import urun

wb = Workbook()
sheet = wb.active

data = urun.post_year
for i in data.find():
    i = [i.get("name"), i.get('time'), i.get('praise'), i.get('share'), i.get('content'),
         i.get('year'), i.get('month'), i.get("day")]
    sheet.append(i)
wb.save(r"D:\post.xlsx")
