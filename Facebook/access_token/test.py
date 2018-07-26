
access_token = 'EAAYR7BRnoaEBAGTSqhS5R9gX0c9CDZAlQuKqNZARVtCRQvRvzpBP5PcnVu6pJn5NUZCOAI3oPG0HCWF554WU0LpY57MjZBZAZAnD3ZB2a6RurtDjm7ROU6aZABvpkxTOtLAcpTXxLLkpZBGRkDSBfCOhZA8jMXHd9BVzFNHHoniFl79bJn4SBsVUGQJdwFbR2SIq4ZD'

# import facebook
# proxies = {'https': "https://localhost:1080"}
# graph = facebook.GraphAPI(access_token=access_token, proxies=proxies)
# post = graph.get_object(id='10209698838182695', fields='message')
# print(post['message'])


# app_id = "1231241241"
# canvas_url = "https://domain.com/that-handles-auth-response/"
# perms = ["manage_pages","publish_pages"]
# fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
# print(fb_login_url)


"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""
import facebook
import requests


def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(post['created_time'])


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = access_token
# Look at Bill Gates's profile for this example by using his Facebook id.
user = 'BillGates'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break