import json

with open('members_url.txt', 'r', encoding='utf-8') as f:
    url_dict = json.load(f)

print(url_dict)
print(len(url_dict))