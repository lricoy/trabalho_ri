# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify
from TwitterAPI import TwitterAPI, TwitterRestPager

app = Flask(__name__)
#app.debug = True

# Dados de acesso da API
CONSUMER_KEY = '84807B0PDDfuoNRqJQPHrJWrb'
CONSUMER_SECRET = 'xqzQSFRNndyK80nByRjBfivrgD52s6ZbPG8xWsqcYrumoaZkAH'
ACCESS_TOKEN_KEY = '211253736-EPwl1euBiQAIMaFUG40CyGkSKaYSdsyds0RqdrVO'
ACCESS_TOKEN_SECRET = 'rdcJR4RD2uQJqDJdOSd6WDK3aNBLrdUNMMCQh1Xp6PuAD'

# objeto da API
twitter_api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/query_twitter/<hashtag>', defaults={'depth': 1})
@app.route('/query_twitter/<hashtag>/<int:depth>')
def query_twitter(hashtag, depth):
    print('Querying hashtag %s with depth %s' % (hashtag, depth))

    #requisição
    r = twitter_api.request('search/tweets', {'q': '#'+hashtag.strip(), 'count':(10 * depth)})

    #impressão
    tweets = [item['user']['name'] + ' - ' + item['text'] if 'text' in item else item for item in r]

    return jsonify(tweets=tweets)
