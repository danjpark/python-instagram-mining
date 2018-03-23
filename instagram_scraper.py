import requests
import re
import json

def grab_hashtag(hashtag):
    #define the return array
    ret_array = []

    #define the string we need to ping
    url_string = "https://www.instagram.com/explore/tags/%s/?__a=1" % hashtag

    #we get the responsein json
    req = requests.get(url_string).json()

    #the only part we care about is this part
    d = req['graphql']['hashtag']['edge_hashtag_to_media']

    #write the entire response into a file
    with open('file.txt', 'w') as file:
        # file.write(soup.prettify())
        file.write(json.dumps(req))

    for eachNode in d['edges']:
        if not eachNode['node']['is_video']:
            ret_array.append({
                'description': eachNode['node']['edge_media_to_caption']['edges'][0]['node']['text'],
                'taken_at_timestamp' : eachNode['node']['taken_at_timestamp'],
                'height' : eachNode['node']['dimensions']['height'],
                'width' : eachNode['node']['dimensions']['width'],
                'display_url' : eachNode['node']['display_url'],
                'likes' : eachNode['node']['edge_liked_by'],
                'owner_id' : eachNode['node']['owner']['id'],
                'shortcode':  eachNode['node']['shortcode'],
            })
            ## i also need the comment since that is where the #'s live msot likely
            ## looks like comment doesnt live in this call. we need to make another call
            ## using the shortcode
    return ret_array

print(len(grab_hashtag('cavapoo')))


# data = json.loads(however_youre_getting_the_data('https://www.instagram.com/explore/tags/plebiscito/?__a=1&max_id={}'.format(end_cursors[-1])))


## write a function using the shortcode of an image and looking up the username
# https://www.instagram.com/p/{SHORTCODE}/?__a=1
# https://www.instagram.com/smena8m/?__a=1 <-- if you have the UID

## maybe i'll make a postgres database to put it in

# then i need to update it once in a while with all users and number of followers
