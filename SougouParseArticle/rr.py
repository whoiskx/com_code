import requests
import json
for i in range(10):
    data = {"title": "用二倍速追剧的日子", "content": "用二倍速追剧的日子用二倍速追剧的日子用二倍速追剧的日子用二倍速追剧的日子", "timestamp": 1536376503}
    # get_id_url = 'http://182.245.126.226:8012/WeiXinArt/GetArticleId'
    # parse_title_url = 'http://182.245.126.226:8012/WeiXinArt/SingleParse'

    get_id_url = 'http://127.0.0.1:8012/WeiXinArt/GetArticleId'
    # parse_title_url = 'http://127.0.0.1:8012/WeiXinArt/SingleParse'

    res = requests.post(get_id_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    # res = requests.get(parse_title_url, params={'ArticleId':'f3ecd4501544942033c83d22e98654eb'})

    # print(type(res.content), res.content)
    print(json.dumps(res.json(), indent=4, ensure_ascii=False))