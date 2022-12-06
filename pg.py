import requests
import pprint
pp = pprint.PrettyPrinter(indent=2)
headers = {'Ocp-Apim-Subscription-Key': 'a1530b41-8e22-47c0-9585-dee9914e39eb',
            'languageId': '2'
            }
#ENDPOINT = 'https://www.globalsportsapi.com/ODATAv1/FootballSample/leagues?gsaappkey=61f1a51d359e461eaefd557dd6d4edde'
ENDPOINT = 'https://s0-sports-data-api.broadage.com/soccer/tournament/list'
leagues = requests.get(ENDPOINT, headers=headers).json()
[pp.pprint(f"{league['name']}: {league['id']}") for league in leagues]