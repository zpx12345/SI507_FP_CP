import requests
import json
import logging
import pprint
logging.basicConfig(level=logging.CRITICAL)
pp = pprint.PrettyPrinter(indent=4)
api_dic = {

}
SCOOER_ENDPOINT = 'https://s0-sports-data-api.broadage.com/soccer'
headers = {'Ocp-Apim-Subscription-Key': 'a1530b41-8e22-47c0-9585-dee9914e39eb',
            'languageId': '2'
            }
TOURNAMENT_LIST_ENDPOINT = SCOOER_ENDPOINT + '/tournament/list'
TOURNAMENT_TEAM_LIST_ENDPOINT = SCOOER_ENDPOINT + '/tournament/teams'
TOURNAMENT_TEAM_ENDPOINT = SCOOER_ENDPOINT + '/team/squad/stats'
class cache:
    tournament_list_cache = {}
    tournament_team_list_cache = {}
    team_player_cache = {}
tournament_list_fp = 'tournament_list.json'
tournament_team_list_fp = 'tournament_team_list.json'
team_player_list_fp = 'team_player_list.json'
player_list_fp = 'player_list.json'
def exact_fp(fp, ap=None):
    return fp[:-5]+f"_{ap}"+fp[-5:]

def get_league():
    retrive_from_internet = None
    while retrive_from_internet not in ['y', 'n']:
        retrive_from_internet = input("want to know new league?(y/n)")
    if retrive_from_internet == 'y':
        logging.debug('intended retirve data from internet')
        cache.tournament_list_cache = requests.get(TOURNAMENT_LIST_ENDPOINT, headers=headers).json()
        with open(tournament_list_fp, 'w') as file:
            json.dump(cache.tournament_list_cache, file)
    else:
        try:
            logging.debug('retrive data from file')
            with open(tournament_list_fp, 'r') as file:
                cache.tournament_list_cache = json.load(file)
        except:
            logging.debug('file illegal, get data from internet')
            cache.tournament_list_cache = requests.get(TOURNAMENT_LIST_ENDPOINT, headers=headers).json()
            with open(tournament_list_fp, 'w') as file:
                json.dump(cache.tournament_list_cache, file)
    for index, tournament in enumerate(cache.tournament_list_cache):
        print(f"{index+1}: {tournament['name']}")
    

def get_team():
    league_idx = float('inf')
    while type(league_idx) != int or league_idx > len(cache.tournament_list_cache):
        try:
            league_idx = int(input(f"Please instert the index of which league, range is {min(len(cache.tournament_list_cache),1)} to {len(cache.tournament_list_cache)} :"))
            logging.debug(f"max length is {len(cache.tournament_list_cache)}")
        except:
            league_idx = float('inf')
    league_id = cache.tournament_list_cache[league_idx-1]['id']
    try:
        with open(exact_fp(tournament_team_list_fp, league_id), 'r') as file:
                cache.tournament_team_list_cache = json.load(file)
        logging.debug("there is a file contain the teams")
    except:
        logging.debug("there is no file contain the teams")
        cache.tournament_team_list_cache = requests.get(TOURNAMENT_TEAM_LIST_ENDPOINT, headers=headers, params={"tournamentId": league_id}).json()
        with open(exact_fp(tournament_team_list_fp, league_id), 'w') as file:
                json.dump(cache.tournament_team_list_cache, file)
    for index, team in enumerate(cache.tournament_team_list_cache):
        print(f"{index+1}: {team['name']}")

def get_team_player():
    team_idx = float('inf')
    while type(team_idx) != int or team_idx > len(cache.tournament_team_list_cache):
        try:
            team_idx = int(input(f"Please instert the index of which player, range is {min(len(cache.tournament_team_list_cache),1)} to {len(cache.tournament_team_list_cache)} :"))
            logging.debug(f"max length is {len(cache.tournament_team_list_cache)}")
        except:
            team_idx = float('inf')
    team_id = cache.tournament_team_list_cache[team_idx-1]['id']
    try:
        with open(exact_fp(team_player_list_fp, team_id), 'r') as file:
            cache.team_player_cache = json.load(file)
        logging.debug("there is a file contain the player")
    except:
        logging.debug("there is no file contain the player")
        cache.team_player_cache = requests.get(TOURNAMENT_TEAM_ENDPOINT, headers=headers, params={"teamId": team_id}).json()
        with open(exact_fp(team_player_list_fp, team_id), 'w') as file:
                json.dump(cache.team_player_cache, file)
    if cache.team_player_cache != None:
        for index, player in enumerate(cache.team_player_cache):
            print(f"{index+1}: {player['player']['knownName']}")
    else:
        print("No players have data")

def league_team_mode():
    get_league()
    get_team()
    get_team_player()
    
league_team_mode()