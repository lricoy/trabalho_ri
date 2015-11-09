from instagram import client, subscriptions

SEARCH_VALUE = input('Digite o tag desejada:')

client_id = '228de91db6d645219393b0a9d258ac58'
client_secret = '7d529257792447938c680696ac9ebcb7'
access_token = '40392665.1fb234f.d8cb76e769844633b6c4c4c766132b69'

api = client.InstagramAPI(access_token=access_token, client_secret=client_secret)

tag_search = api.tag_search(q="dog")

print(tag_search)

tag_search, next_tag = api.tag_search(q=SEARCH_VALUE.strip())
tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
photos = []

for tag_media in tag_recent_media:
        print(tag_media.get_standard_resolution_url())
        print(tag_media.like_count)

