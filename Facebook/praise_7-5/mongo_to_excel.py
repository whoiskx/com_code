from openpyxl import Workbook
from setting import urun

wb = Workbook()
sheet = wb.active

data = urun.praise_88
for i in data.find():
    r  = [i.get('name'), i.get("praise"), i.get('url')]
    sheet.append(r)
wb.save(r"D:\praise_end.xlsx")
