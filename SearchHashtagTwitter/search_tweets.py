# -*- coding: utf-8 -*-
from TwitterAPI import TwitterAPI, TwitterRestPager

#entrada da pesquisa desejada
SEARCH_TERM = raw_input('Digite a tag que deseja : ')
SEARCH_SIZE = raw_input('Digite a profundidade da busca (1-10): ')
SEARCH_SIZE = int(SEARCH_SIZE)

#dados da API
CONSUMER_KEY = '84807B0PDDfuoNRqJQPHrJWrb'
CONSUMER_SECRET = 'xqzQSFRNndyK80nByRjBfivrgD52s6ZbPG8xWsqcYrumoaZkAH'
ACCESS_TOKEN_KEY = '211253736-EPwl1euBiQAIMaFUG40CyGkSKaYSdsyds0RqdrVO'
ACCESS_TOKEN_SECRET = 'rdcJR4RD2uQJqDJdOSd6WDK3aNBLrdUNMMCQh1Xp6PuAD'

api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

#requisição
r = api.request('search/tweets', {'q': '#'+SEARCH_TERM.strip(), 'count':(10 * SEARCH_SIZE)})

count = 0
#impressão
for item in r:
    count += 1
    print(item['user']['name'] + ' - ' + item['text'] if 'text' in item else item)

"""
r = TwitterRestPager(api, 'search/tweets', {'q':SEARCH_TERM, 'count':10 })

for item in r.get_iterator():
    if 'text' in item:
        print item['text']
    elif 'message' in item and item['code'] == 88:
        print 'SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message']
        break
"""
#resultados estatisticos
print('\nQUOTA: %s' % r.get_rest_quota())
print('\LENGTH: %s' % count)
