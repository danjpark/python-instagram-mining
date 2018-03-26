import re
import requests
import json
import pandas as pd


from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

def db_connection():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return create_engine(URL(**config))

def extract_hashtags(extraction, type):
    # extraction is either a list of comments objects (type == 'comments')
    # or is a string (the descirption) (type == 'string')
    ret_array = []

    if type == 'string':
        foo = re.split(' |,|\n', extraction)
        for eachWord in foo:
            if eachWord.startswith('#'):
                ret_array.append(eachWord)
    elif type == 'comments':
        for eachNode in extraction:
            foo = re.split(' |,|\n', eachNode['node']['text'])
            for eachWord in foo:
                if eachWord.startswith('#'):
                    ret_array.append(eachWord)
    return ret_array

def grab_data(hashtag):
    #define the return array
    ret_array = []

    #define the string we need to ping
    url_string = "https://www.instagram.com/explore/tags/%s/?__a=1" % (hashtag)
    req = requests.get(url_string).json()
    d = req['graphql']['hashtag']['edge_hashtag_to_media']

    while(d['page_info']['has_next_page']):
        if len(ret_array) > 20: break

        for eachNode in d['edges']:
            if not eachNode['node']['is_video']:
                try:
                    # first we grab all the hashtags from the comments
                    if not eachNode['node']['comments_disabled']:
                        shortcode_url = 'https://www.instagram.com/p/%s/?__a=1' % (eachNode['node']['shortcode'])
                        shortcode_req = requests.get(shortcode_url).json()
                        if shortcode_req['graphql']['shortcode_media']['edge_media_to_comment']['count'] > 0:
                            comment_hashtags = extract_hashtags(shortcode_req['graphql']['shortcode_media']['edge_media_to_comment']['edges'], 'comments')
                    caption_hashtags = extract_hashtags(eachNode['node']['edge_media_to_caption']['edges'][0]['node']['text'], 'string')
                    hashtags = comment_hashtags + caption_hashtags

                    if eachNode['node']['shortcode'] == 'Bgw3fcdnBLw':
                        print(eachNode['node']['edge_media_to_caption']['edges'][0]['node']['text'])
                        print(hashtags)

                    # second we grab all the hashtags from the description (aka caption)
                    ret_array.append({
                        'taken_at_timestamp' : eachNode['node']['taken_at_timestamp'],
                        'height' : eachNode['node']['dimensions']['height'],
                        'width' : eachNode['node']['dimensions']['width'],
                        'display_url' : eachNode['node']['display_url'],
                        'likes' : eachNode['node']['edge_liked_by']['count'],
                        'owner_id' : eachNode['node']['owner']['id'],
                        'shortcode':  eachNode['node']['shortcode'],
                        'hashtags': hashtags
                    })

                except Exception as e:
                    print("######## ERROR #############\n",e)


        # still in while loop, now we refresh the page
        url_string = "https://www.instagram.com/explore/tags/%s/?__a=1&max_id=%s" \
                    % (hashtag, d['page_info']['end_cursor'])
        req = requests.get(url_string).json()
        d = req['graphql']['hashtag']['edge_hashtag_to_media']


    return pd.DataFrame(ret_array)

def write_to_table(df, table_name):
    engine = db_connection()

    df.to_sql(table_name,
              engine,
              if_exists='append',
              index=False)


write_to_table(grab_data('cavadoodle'),
               'danpark')


## TODO:
## split getting the hashtags into a different function
## where we only get it after we have all the shortcodes
## this way we can grab allt he user inforation from it as well (like followers)


## write a function using the shortcode of an image and looking up the username
# https://www.instagram.com/p/{SHORTCODE}/?__a=1
# https://www.instagram.com/smena8m/?__a=1 <-- if you have the UID

##figure out how to update a row
