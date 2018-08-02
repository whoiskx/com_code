from setting import urun

d = {}
for i in urun.Group.find():
    i.pop("_id")
    print(i)
    d.update(i)

import json
with open('group.txt', 'w', encoding='utf-8') as f:
    s = json.dumps(d)
    f.write(s)


