import requests
import re
import json

tag = 'cavapoo'
url_string = "https://www.instagram.com/explore/tags/%s/?__a=1" % tag

req = requests.get(url_string).json()
d = req['graphql']['hashtag']['edge_hashtag_to_media']

print(len(d['edges']))

with open('file.txt', 'w') as file:
    # file.write(soup.prettify())
    file.write(json.dumps(req))

for eachNode in d['edges']:
    comment = eachNode['node']['edge_media_to_caption']['edges'][0]['node']['text']
    taken_at_timestamp = eachNode['node']['taken_at_timestamp']
    height = eachNode['node']['dimensions']['height']
    width = eachNode['node']['dimensions']['width']
    display_url = eachNode['node']['display_url']
    likes = eachNode['node']['edge_liked_by']
    is_video = eachNode['node']['is_video']
    owner = eachNode['node']['owner']['id']
    print(owner)


# data = json.loads(however_youre_getting_the_data('https://www.instagram.com/explore/tags/plebiscito/?__a=1&max_id={}'.format(end_cursors[-1])))


## write a function using the shortcode of an image and looking up the username
# https://www.instagram.com/p/{SHORTCODE}/?__a=1
# https://www.instagram.com/smena8m/?__a=1 <-- if you have the UID

## maybe i'll make a postgres database to put it in

# then i need to update it once in a while with all users and number of followers
