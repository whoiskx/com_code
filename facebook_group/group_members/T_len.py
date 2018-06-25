import json

with open('members_url.txt', 'r', encoding='utf-8') as f:
    url_dict = json.load(f)

print(len(url_dict))
for i, item in enumerate(url_dict):
    for ii, item2 in enumerate(url_dict):
        if ii > i and item == item2:
            print(item)
            url_dict.remove(item)
with open('members_url_filter.txt', 'w', encoding='utf-8') as f:
    s = json.dumps(url_dict,  indent=2, ensure_ascii=False)
    f.write(s)
print(len(url_dict))