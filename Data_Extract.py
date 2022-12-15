import requests
import json
import logging
import pprint
logging.basicConfig(level=logging.CRITICAL)
pp = pprint.PrettyPrinter(indent=4)
game_include = 'localTeam,visitorTeam,goals,cards,corners,lineup,highlights,substitutions,other,bench,sidelined,comments,'
SCOOER_ENDPOINT = 'https://soccer.sportmonks.com/api/v2.0'
token = 'dihqMk5ZpoCapBhCULM4KFoLlCAw44NDGSI4pnZ7NlOyWVxa0ZcZPNrkEZ6P'
headers = {'api_token': token}
TOURNAMENT_LIST_ENDPOINT = SCOOER_ENDPOINT + '/leagues/'
COUNTRY_ENDPOINT = SCOOER_ENDPOINT + '/countries/'
TEAM_ENDPOINT = SCOOER_ENDPOINT + '/teams/'
SEASON_LIST = SCOOER_ENDPOINT + '/seasons/'
class cache:
    tournament_list_cache = []
    league_team_list_cache = []
    country_team_list_cache = []
    team_player_cache = []
    player_cache = []
    season_list_cache = []
    season_league_list_cache = []
    position_list = []
    player_id_to_name = {}
    league_id = None
    country_id = None

tournament_list_fp = 'tournament_list.json'
country_team_list_fp = 'country_team_list.json'
tournament_team_list_fp = 'tournament_team_list.json'
team_player_list_fp = 'team_player_list.json'
players_list_fp = 'player_list.json'
season_fp = 'season_list.json'
season_league_fp = 'season_league_list.json'
team_fixture_fp = 'team_fixture.json'
position_list_fp = 'position_list.json'
def exact_fp(fp, ap=None):
    if type(ap) != list:
        ap = [ap]
    ans = fp[:-5]
    for a in ap:
        ans += f"_{a}"
    ans += fp[-5:]
    return ans

def get_position():
    try:
        with open(position_list_fp, 'r') as file:
            cache.position_list = json.load(file)
    except:
        cache.position_list = requests.get()


def get_league():
    retrive_from_internet = None
    while retrive_from_internet not in ['y', 'n']:
        retrive_from_internet = input("want to know new league?(y/n)")
    if retrive_from_internet == 'y':
        logging.debug('intended retirve data from internet')
        cache.tournament_list_cache = requests.get(TOURNAMENT_LIST_ENDPOINT, params=headers).json()['data']
        with open(tournament_list_fp, 'w') as file:
            json.dump(cache.tournament_list_cache, file)
    else:
        try:
            logging.debug('retrive data from file')
            with open(tournament_list_fp, 'r') as file:
                cache.tournament_list_cache = json.load(file)
        except:
            logging.debug('file illegal, get data from internet')
            cache.tournament_list_cache = requests.get(TOURNAMENT_LIST_ENDPOINT, params=headers).json()['data']
            with open(tournament_list_fp, 'w') as file:
                json.dump(cache.tournament_list_cache, file)
    for index, tournament in enumerate(cache.tournament_list_cache):
        print(f"{index+1}: {tournament['name']}")
    

def get_team(except_team_id = None, league_id=None, get_season_=True, get_league_=True):
    if get_league_:
        league_idx = float('inf')
        while type(league_idx) != int or league_idx > len(cache.tournament_list_cache):
            try:
                league_idx = int(input(f"Please instert the index of which league, range is {min(len(cache.tournament_list_cache),1)} to {len(cache.tournament_list_cache)} :"))
                logging.debug(f"max length is {len(cache.tournament_list_cache)}")
            except:
                league_idx = float('inf')
        league_id = cache.tournament_list_cache[league_idx-1]['id']
        country_id = cache.tournament_list_cache[league_idx-1]['country_id']
        cache.league_id = league_id
        cache.country_id = country_id
    else:
        league_id = cache.league_id
        country_id = cache.country_id
    try:
        with open(exact_fp(country_team_list_fp, country_id), 'r') as file:
                cache.country_team_list_cache = json.load(file)
        logging.debug("there is a file contain the teams")
    except:
        logging.debug("there is no file contain the teams")
        cache.country_team_list_cache = requests.get(COUNTRY_ENDPOINT+str(country_id)+'/teams', params={'api_token': token, 'include': 'league'}).json()['data']
        with open(exact_fp(country_team_list_fp, country_id), 'w') as file:
                json.dump(cache.country_team_list_cache, file)
    
    if get_league_:
        real_idx = 0
        for index, team in enumerate(cache.country_team_list_cache):
            if team['league']['data']['id'] == league_id:
                cache.league_team_list_cache.append(team)
                real_idx += 1
                print(f"{real_idx}: {team['name']}")
        with open(exact_fp(tournament_team_list_fp, league_id), 'w') as file:
            json.dump(cache.league_team_list_cache, file)
    else:
        for index, team in enumerate(cache.league_team_list_cache):
            if team['id'] != except_team_id:
                print(f"{index+1:<2}: {team['name']:<20}")
    if get_season_:
        get_season(league_id)

def get_season(league_id):
    try: 
         with open(exact_fp(season_league_fp, league_id), 'r') as file:
            cache.season_league_list_cache = json.load(file)
    except:
        try:
            with open(season_fp, 'r') as file:
                cache.season_list_cache = json.load(file)
        except:
            cache.season_list_cache = requests.get(SCOOER_ENDPOINT+'/seasons/', params=headers).json()['data']
            with open(season_fp, 'w') as file:
                json.dump(cache.season_list_cache, file)
        cache.season_league_list_cache = [season for season in cache.season_list_cache if season['league_id'] == league_id]
        with open(exact_fp(season_league_fp, league_id), 'w') as file:
                json.dump(cache.season_league_list_cache, file)
    for index, season in enumerate(cache.season_league_list_cache):
        print(f"{index+1}, {season['name']}")


def get_team_player(season_id=0, choose_season=True):
    team_idx = float('inf')
    while type(team_idx) != int or team_idx > len(cache.league_team_list_cache):
        try:
            team_idx = int(input(f"Please instert the index of which team, range is {min(len(cache.league_team_list_cache),1)} to {len(cache.league_team_list_cache)} :"))
            logging.debug(f"max length is {len(cache.league_team_list_cache)}")
        except:
            team_idx = float('inf')
    team_id = cache.league_team_list_cache[team_idx-1]['id']
    
    if choose_season:
        season_idx = float('inf')
        while type(season_idx) != int or season_idx > len(cache.league_team_list_cache):
            try:
                season_idx = int(input(f"Please instert the index of which season, range is {min(len(cache.season_league_list_cache),1)} to {len(cache.season_league_list_cache)} :"))
                logging.debug(f"max length is {len(cache.season_league_list_cache)}")
            except:
                season_idx = float('inf')
        season_id = cache.season_league_list_cache[season_idx-1]['id']
    else:
        for index, season in enumerate(cache.season_league_list_cache):
            if season['id'] == season_id:
                season_idx = index + 1
    get_team_fixrues(team_id, cache.season_league_list_cache[season_idx-1]['name'])

    try:
        with open(exact_fp(team_player_list_fp, [team_id, season_id]), 'r') as file:
            cache.team_player_cache = json.load(file)
        logging.debug("there is a file contain the player")
    except:
        logging.debug("there is no file contain the player")
        cache.team_player_cache = [player['player']['data'] for player in requests.get(SCOOER_ENDPOINT+f'/squad/season/{season_id}/team/{team_id}/', params={'api_token': token, 'include': 'player'}).json()['data']]
        with open(exact_fp(team_player_list_fp, [team_id, season_id]), 'w') as file:
            json.dump(cache.team_player_cache, file)
    if cache.team_player_cache != None:
        for index, player in enumerate(cache.team_player_cache):
            cache.player_id_to_name[player['player_id']] = player['display_name']
            print(f"{index+1:<2}: {player['display_name']:<20}position: {player['position_id']}")
    else:
        print("No players have data")
    player_idx = float('inf')
    while type(player_idx) != int or player_idx > len(cache.team_player_cache):
        try:
            player_idx = int(input(f"Please instert the index of which player, range is {min(len(cache.team_player_cache),1)} to {len(cache.team_player_cache)} :"))
            logging.debug(f"max length is {len(cache.team_player_cache)}")
        except:
            player_idx = float('inf')
    player_id = cache.team_player_cache[player_idx-1]['player_id']
    return team_id, cache.season_league_list_cache[season_idx-1]['name'], season_id, player_id

def get_team_fixrues(team_id, season_name):
    start_date = season_name.split('/')[0]+'-07-01'
    end_date = season_name.split('/')[1]+'-07-01'
    try:
        with open(exact_fp(team_fixture_fp, [team_id, start_date, end_date]), 'r') as file:
            data = json.load(file)
    except:
        data = requests.get(SCOOER_ENDPOINT+f'/fixtures/between/{start_date}/{end_date}/{team_id}', params={'api_token': token, 'include': game_include}).json()['data']
        with open(exact_fp(team_fixture_fp, [team_id, start_date, end_date]), 'w') as file: 
            json.dump(data, file)
    return data

def get_teammate(player_id, team_id, season_id):
    ans = []
    with open(exact_fp(team_player_list_fp, [team_id, season_id]), 'w') as file:
            json.dump(cache.team_player_cache, file)
    for player in cache.team_player_cache:
        if player['player_id'] != player_id:
            ans.append(player['player_id'])
    return ans

# def load_players():
#     try:
#         with open(players_list_fp) as file:
#             cache.player_cache = json.load(file)
#         logging.debug('have a file cotain')
#         return True
#     except:
#         return False

# def show_players_list():
#     for item, player in enumerate(cache.player_cache):
#         print(f"{item + 1}: {player}")

# def league_team_mode():
#     get_league()
#     get_team()
#     get_team_player()

# def people_from_file():
#     if load_players():
#         show_players_list()
#         return True
#     else:
#         print("No data found")
#         return False
# if __name__ == "__main__":
#     league_team_mode()