from setting import test

for item in test['img_header_url_8000'].find():
    blogger_id = item.get('post_id')
    item.update({'blogger_id': blogger_id})
    test['img_herder_merge'].save(item)