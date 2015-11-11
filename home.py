# -*- coding: utf-8 -*-
import os
from decimal import Decimal, getcontext
from collections import Counter
from urlparse import urlparse, parse_qs
from flask import Flask, jsonify, render_template
from flask.ext.cors import CORS
from TwitterAPI import TwitterAPI, TwitterRestPager
from instagram import client, subscriptions
from constants import STOP_WORDS_PT_BR, PONTOS_POLARIDADE

config = {
    'instagram': {
        'CLIENT_ID': '228de91db6d645219393b0a9d258ac58',
        'CLIENT_SECRET': '7d529257792447938c680696ac9ebcb7',
        'ACCESS_TOKEN': '40392665.1fb234f.d8cb76e769844633b6c4c4c766132b69'
    },
    'twitter': {
        # Dados de acesso da API
        'CONSUMER_KEY': '84807B0PDDfuoNRqJQPHrJWrb',
        'CONSUMER_SECRET': 'xqzQSFRNndyK80nByRjBfivrgD52s6ZbPG8xWsqcYrumoaZkAH',
        'ACCESS_TOKEN_KEY': '211253736-EPwl1euBiQAIMaFUG40CyGkSKaYSdsyds0RqdrVO',
        'ACCESS_TOKEN_SECRET': 'rdcJR4RD2uQJqDJdOSd6WDK3aNBLrdUNMMCQh1Xp6PuAD',
    }

}

# objetos das APIs
twitter_api = TwitterAPI(config['twitter']['CONSUMER_KEY'],
                 config['twitter']['CONSUMER_SECRET'],
                 config['twitter']['ACCESS_TOKEN_KEY'],
                 config['twitter']['ACCESS_TOKEN_SECRET'])

instagram_api = client.InstagramAPI(
                    access_token=config[ 'instagram']['ACCESS_TOKEN'],
                    client_secret=config[ 'instagram']['CLIENT_SECRET'])

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/')
def hello():
    return render_template('index.html')

"""
    ROUTE TO QUERY TWITTER
"""
@app.route('/query_twitter/<hashtag>', defaults={'depth': 1})
@app.route('/query_twitter/<hashtag>/<int:depth>')
def query_twitter(hashtag, depth):
    print('Querying hashtag %s with depth %s' % (hashtag, depth))

    #requisição
    r = twitter_api.request('search/tweets', {'q': '#'+hashtag.strip(), 'lang': 'pt', 'count':(10 * depth)})

    #impressão
    tweets = [
        {
            'url': '',
            'id': item['id_str'],
            'likes': item['retweet_count'],
            'text': item['text'].encode('utf8'),
            'normalized_text': normalize_text(item['text']),
            'user': item['user']['name']
        }
        for item in r
    ]

    # polarity measure
    for tweet in tweets: tweet['polarity'] = polarity_measure(tweet['normalized_text'])

    words_in_tweets = ''.join([ item['normalized_text'] for item in tweets ]).split()
    most_used_words = Counter(words_in_tweets).most_common(10)

    # TO-DO: http://stackoverflow.com/questions/3594514/how-to-find-most-common-elements-of-a-list

    return jsonify(data=tweets, top_words=most_used_words)

"""
    ROUTE TO QUERY INSTAGRAM
"""
@app.route('/query_instagram/<hashtag>', defaults={'depth': 1})
@app.route('/query_instagram/<hashtag>/<int:depth>')
def query_instagram(hashtag, depth):
    photos = []

    tag_recent_media, next = instagram_api.tag_recent_media(tag_name=hashtag.strip(), count=10)
    qs = parse_qs(urlparse(next).query)

    # Executa ate ter terminado o peso
    while next and depth > 0:
        photos = photos + [
            {
                'url': x.get_standard_resolution_url(),
                'id': x.id,
                'likes': x.like_count,
                'text': x.caption.text,
                'normalized_text': normalize_text(x.caption.text),
                'user': ''
            }
            for x in tag_recent_media
        ]

        # Get the next page
        depth -= 1
        tag_recent_media, next = instagram_api.tag_recent_media(tag_name=hashtag.strip(), count=10, max_id=qs['max_tag_id'])

    # Polarity
    for photo in photos: photo['polarity'] = polarity_measure(photo['normalized_text'])

    words_in_captions = ''.join([ item['normalized_text'] for item in photos ]).split()
    most_used_words = Counter(words_in_captions).most_common(10)

    return jsonify(data=photos, top_words=most_used_words)

# util
def normalize_text(text):
    return ' '.join([ unicode(word) for word in text.lower().split() if word not in STOP_WORDS_PT_BR])

def polarity_measure(text):
    def _get_points(word):
        if(PONTOS_POLARIDADE.has_key(word)):
            return PONTOS_POLARIDADE[word]
        return 0

    getcontext().prec = 6

    points_per_word = [ (word, _get_points(word)) for word in text.split() ]
    word_count = len(points_per_word)

    happy = [ x[0] for x in points_per_word if x[1] > 0 ]
    happy_percent = Decimal(len(happy)) / Decimal(word_count) * 100 if len(happy) > 0 else 0

    sad = [ x[0] for x in points_per_word if x[1] < 0 ]
    sad_percent = Decimal(len(sad)) / Decimal(word_count) * 100 if len(sad) > 0 else 0

    polarity_sum = sum([x[1] for x in points_per_word])

    return {
        #'points_per_word': points_per_word,
        'happy_words': happy,
        'happy_percent': happy_percent,
        'sad_words': sad,
        'sad_percent': sad_percent,
        'polarity': polarity_sum,
        'word_count': word_count
    }


if __name__ == '__main__':
    app.run()
