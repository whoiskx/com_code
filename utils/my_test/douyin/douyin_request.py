import requests

url = 'https://api.amemv.com/aweme/v1/feed/?type=0&max_cursor=0&min_cursor=0&count=6&volume=0.0&pull_type=1&need_relieve_aweme=0&filter_warn=0&req_from=&ts=1531726203&app_type=normal&manifest_version_code=200&_rticket=1531726203503&ac=wifi&device_id=47188961508&iid=37927009090&os_version=8.0.0&channel=huawei&version_code=200&device_type=BKL-AL00&language=zh&resolution=1080*2040&openudid=6f4f5b8b94dba483&update_version_code=2002&app_name=aweme&version_name=2.0.0&os_api=26&device_brand=HONOR&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a105b4542bf77bf9ac4355&cp=477eb051b9c04c98e1KqSu&mas=00bdf58e7c6e46f6d8450b460b414a1780acaccc2cc6869c6646ec'
headers = {'Host': 'api.amemv.com', 'Connection': 'keep-alive',
           'Cookie': 'odin_tt=2a4afe1350f4815e63d3a1f26f6e2aea8ead562300b8980a371bbc52814828a1eaa47e8eb1b29a5a42b0e572ba474995; sid_guard=53672998a610a50910664e885e4990a9%7C1531016437%7C2592000%7CTue%2C+07-Aug-2018+02%3A20%3A37+GMT; uid_tt=e31e4f19e40e449c6be3a83f13c41347; sid_tt=53672998a610a50910664e885e4990a9; sessionid=53672998a610a50910664e885e4990a9; install_id=37927009090; ttreq=1$536f377876c0756f8cee3051d6204933f449fb07',
           'Accept-Encoding': 'gzip', 'X-SS-REQ-TICKET': '1531726203497',
           'User-Agent': 'com.ss.android.ugc.aweme/200 (Linux; U; Android 8.0.0; zh_CN_#Hans; BKL-AL00; Build/HUAWEIBKL-AL00; Cronet/58.0.2991.0)'}
resp = requests.get(url, headers=headers)

print(resp.text)