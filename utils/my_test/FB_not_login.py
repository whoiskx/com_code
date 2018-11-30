import requests

url = 'https://www.facebook.com/pages_reaction_units/more/?page_id=172348966125763&cursor=%7B%22timeline_cursor%22%3A%22timeline_unit%3A1%3A00000000001530235154%3A04611686018427387904%3A09223372036854775800%3A04611686018427387904%22%2C%22timeline_section_cursor%22%3A%7B%7D%2C%22has_next_page%22%3Atrue%7D&surface=www_pages_home&unit_count=8&dpr=1&__user=0&__a=1&__dyn=5V8WXBzamaUmgDBzFHpUR1ycCzSczVbGAdyeGBXrWqF1eU8EnGdwIhEnUF7yWCHAxiESmqaxuqE88HyWxeipi28gyElWAAzppenKtqx2AcUhz998iGtxifGcgLAKidzoKnGh4-9AZ4gO48nyp8Fecx2egHy4mEepoGmXBxeumuibBDJ3o9FWxmK7VECqQh0wCxaE_AJp8GrxjDUG6aJUhxR4gScz99FXyoSaCzU94q4rG-GKdV8hAnykGmV7Giumqyboyut9wxk-32ibKbF1hyVriCUKbwFxC4eby9o-8DGCXV8W9xheEWbAzAulaayKjyFVEviAypEGQ4UiyUSmiinBAgV4K4pUV1iqay8CuiuiazazoK7WGucy44bAAx1eq4bAKdCKh2osyUOm4p8CjgKULwAG&__req=9&__be=-1&__pc=PHASED%3ADEFAULT&__rev=4128604'
headers = {'Host': 'www.facebook.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
           'Accept': '*/*', 'Referer': 'https://www.facebook.com/kaifulee/', 'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cookie': 'datr=OxkjW4MYaIelucIws97V02xW; sb=_R0jWyoRctx7GnDrlLyCjFE2; locale=zh_CN; reg_fb_gate=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAfdmrme287GtQ8lDAYck8Hr1EdS4sblomJegt_cx_mNGnKKQO8KxWztiQLmh6lcwzVEu-tx2eWAUqsb3p3xRDLA6Cq6PAIhCF7sRsBm6B_N-XQ%26smuh%3D17460%26lh%3DAc-qSkVMZrAqy38q; reg_fb_ref=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAfdmrme287GtQ8lDAYck8Hr1EdS4sblomJegt_cx_mNGnKKQO8KxWztiQLmh6lcwzVEu-tx2eWAUqsb3p3xRDLA6Cq6PAIhCF7sRsBm6B_N-XQ%26smuh%3D17460%26lh%3DAc-qSkVMZrAqy38q; fr=0ICeTuNMbW3ThPfuj.AWWZ32_QLPFYehoSyw0JOzFUdOA.BbHxb1.s-.AAA.0.0.BbVTf9.AWU-qwyh; wd=1920x946'}
resp = requests.get(url)

print(resp.text)

from pyquery import PyQuery as pq

e = pq(resp.text)

print(e(".profileLink").text())
print(e('.timestampContent').text())
