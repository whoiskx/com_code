with open("error_test.html", "r", encoding='utf-8') as f:
    index_html = f.read()

import re
profile = re.findall(r'<div id="intro_container_id">.*?</ul></div>', index_html)
print(profile[0])