

import requests

url = "https://data.wxb.com/searchResult?kw=%E8%A7%86%E8%A7%89%E5%BF%97&page=1"
url = "https://www.baidu.com"
usage = ""
cookie = {'visit-wxb-id': '7c5736cc99cda0e635c8958831967045', 'PHPSESSID': '8hvca5bejg47la3q10q96rsjm3', 'wxb_fp_id': '3774451913', 'Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91': '1528359684', 'Hm_lpvt_5859c7e2fd49a1739a0b0f5a28532d91': '1528360627'}
r = requests.get(url)
print(r.text)
