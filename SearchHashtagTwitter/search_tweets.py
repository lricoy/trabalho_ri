from TwitterAPI import TwitterAPI

#entrada da pesquisa desejada
SEARCH_TERM = input('Digite a tag que deseja : ')

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
r = api.request('search/tweets', {'q': '#'+SEARCH_TERM.strip()})

#impressão
for item in r:
    print( '\n' )
    print( ascii(item['user']['name'] + ' - ' + item['text']) if 'text' in item else item)

#resultados estatisticos
print('\nQUOTA: %s' % r.get_rest_quota())
 
