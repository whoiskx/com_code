headers = """Host: api.amemv.com
Connection: keep-alive
Cookie: odin_tt=2a4afe1350f4815e63d3a1f26f6e2aea8ead562300b8980a371bbc52814828a1eaa47e8eb1b29a5a42b0e572ba474995; sid_guard=53672998a610a50910664e885e4990a9%7C1531016437%7C2592000%7CTue%2C+07-Aug-2018+02%3A20%3A37+GMT; uid_tt=e31e4f19e40e449c6be3a83f13c41347; sid_tt=53672998a610a50910664e885e4990a9; sessionid=53672998a610a50910664e885e4990a9; install_id=37927009090; ttreq=1$536f377876c0756f8cee3051d6204933f449fb07
Accept-Encoding: gzip
X-SS-REQ-TICKET: 1531726203497
User-Agent: com.ss.android.ugc.aweme/200 (Linux; U; Android 8.0.0; zh_CN_#Hans; BKL-AL00; Build/HUAWEIBKL-AL00; Cronet/58.0.2991.0)"""



items = headers.split("\n")
# print(items)
d = {}
for item in items:
    k, v = item.split(": ", 1)

    d[k] = v.strip()
print(d)
