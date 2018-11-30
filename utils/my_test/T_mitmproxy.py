import mitmproxy.http
from mitmproxy import ctx

num = 0


def request(flow: mitmproxy.http.HTTPFlow):
    global num
    num = num + 1
    ctx.log.info("We've seen %d flows" % num)