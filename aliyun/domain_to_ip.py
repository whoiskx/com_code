import socket

url = 'test.yunrunyuqing.com'
url = 'test.yunrunyunqing.com'
ip = socket.gethostbyname(url)
print(ip)

from urllib.parse import urlparse
url = 'http://test.yunrunyunqing.com:19002/test.html'
parsed_url = urlparse(url)

print(parsed_url.netloc)