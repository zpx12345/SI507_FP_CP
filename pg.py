import requests
import json
import pprint
SCOOER_ENDPOINT = 'https://s0-sports-data-api.broadage.com/soccer'

pp = pprint.PrettyPrinter(indent=4)
token_string = 'dihqMk5ZpoCapBhCULM4KFoLlCAw44NDGSI4pnZ7NlOyWVxa0ZcZPNrkEZ6P'
headers = {'api_token': 'dihqMk5ZpoCapBhCULM4KFoLlCAw44NDGSI4pnZ7NlOyWVxa0ZcZPNrkEZ6P'}
TOURNAMENT_LIST_ENDPOINT = SCOOER_ENDPOINT + '/tournament/list'
TOURNAMENT_TEAM_LIST_ENDPOINT = SCOOER_ENDPOINT + '/tournament/teams'
TOURNAMENT_TEAM_ENDPOINT = SCOOER_ENDPOINT + '/team/squad/stats'
a = requests.get('https://soccer.sportmonks.com/api/v2.0/seasons', params={'league_id': 271,'api_token': 'dihqMk5ZpoCapBhCULM4KFoLlCAw44NDGSI4pnZ7NlOyWVxa0ZcZPNrkEZ6P'}).json()
pp.pprint(a)