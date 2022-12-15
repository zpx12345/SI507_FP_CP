import json
import Data_Extract as DE

def process_fixture(player_id, team_id, season_name):
    fixtures = DE.get_team_fixrues(team_id, season_name)
    data = []
    for fixture in fixtures:
        fix = get_important_data_from_game(player_id, fixture)
        if fix['attendence'] != 0:
            data.append(fix)
    with open (f"./player_processed_data/{player_id}.txt", 'w') as file:
        json.dump(data, file)
    return data

def extract_averae_critical_goal(player_id):
    with open(f"./player_processed_data/{player_id}.txt", 'r') as  file:
        games = json.load(file)
    critical_goals = [len(game['goal_classes']['goals']['critica_goal']) for game in games]
    times = [game['time'] for game in games]
    try:
        average_goals_per_game = sum(critical_goals)/len(critical_goals)
    except:
        average_goals_per_game = None
    try:
        minute_per_goal = sum(times)/sum(critical_goals)
    except:
        minute_per_goal = None
    return average_goals_per_game, minute_per_goal

def compare_average_critical_goal(tree):
    while True:
        dig_teammate_further = input(f"do you want to also evaluate the teammates linked to {DE.cache.player_id_to_name[tree[0]]}?(y/n)")
        if dig_teammate_further in ['y', 'n']:
            break
    if dig_teammate_further == 'y':
        for teammate in tree[1]:
            compare_average_critical_goal(teammate)
    while True:
        dig_compititor_further = input(f"do you want to also evaluate the compititors linked to {DE.cache.player_id_to_name[tree[0]]}?(y/n)")
        if dig_compititor_further in ['y', 'n']:
            break
    if dig_compititor_further == 'y':
        for compititor in tree[2]:
            compare_average_critical_goal(compititor)
    average_goals_per_game, minute_per_goal = extract_averae_critical_goal(tree[0])
    print(f"{DE.cache.player_id_to_name[tree[0]]:<20}'s average critical goals per game is {average_goals_per_game}, minute to critical goal is {minute_per_goal}")       
    print(f"{DE.cache.player_id_to_name[tree[0]]}'s teammates' situation")
    try:
        for teammate in tree[1]:
            average_goals_per_game, minute_per_goal = extract_averae_critical_goal(teammate[0])
            print(f"{DE.cache.player_id_to_name[teammate[0]]:<20}'s average critical goals per game is {average_goals_per_game}, minute to critical goal is {minute_per_goal}")
    except:
        print("no teammates")
    print(f"{DE.cache.player_id_to_name[tree[0]]}'s compititors' situation")
    try:
        for compititor in tree[2]:
            average_goals_per_game, minute_per_goal = extract_averae_critical_goal(compititor[0])
            print(f"{DE.cache.player_id_to_name[compititor[0]]:<20}'s average critical goals per game is {average_goals_per_game}, minute to critical goal is {minute_per_goal}")
    except:
        print("no compititors")

def get_important_data_from_game(player_id, fixture, useless_range=(-2,3)):
    '''
    attendence
    goals:
    shots:
    shot on target:
    goal type:  
            critical goal:
            useless goal:
            critical assist:
            useless assist:
    time:
    dribble:
    aerial_won:
    duel:
        total
        won
    ''' 
    ans = {
        'fixture_id': fixture['id'],
        'attendence': 0,
        'point': 0,
        'host': 1,
        'goals': None,
        'shots': None,
        'shot_on_target': None,
        'assists': None,
        'pass': None,
        'rating': None,
        'goal_classes': {
            'goals': {
                'useless_goal':[],
                'critica_goal':[],
                'plain_goal':[],
            },
            'assists': {
                'useless_assist':[],
                'critica_assist':[],
                'plain_assist':[],
            },
        },
        'time': fixture['time']['minute'],
        # 'dribble': None,
        # 'aerial_won': None,
        # 'duel': None
    }
    
    for player in fixture['lineup']['data']:
        if player['player_id'] == player_id:
            ans['attendence'] = 1
            if player['team_id'] == fixture['winner_team_id']:
                ans['point'] = 3
            if player['team_id'] == None:
                ans['point'] = 1
            try:
                ans['rating'] = float(player['stats']['rating'])
            except:
                pass
            ans['goals'] = player['stats']['goals']['scored']
            ans['shots'] = player['stats']['shots']['shots_total']
            ans['assists'] = player['stats']['goals']['assists']
            ans['pass'] = player['stats']['passing']['passes']
            ans['shot_on_target'] = player['stats']['shots']['shots_on_goal']
            if player['team_id'] != fixture['localTeam']['data']['id']:
                ans['host'] = 0
            for sub in fixture['substitutions']['data']:
                if sub['player_out_id'] == player_id:
                    ans['time'] = sub['minute']
                    break
            break
    for sub in fixture['substitutions']['data']:
        if sub['player_in_id'] == player_id:
            ans['attendence'] = 2
            ans['time'] = ans['time'] - sub['minute']
        for player in fixture['bench']['data']:
            if player['player_id'] == player_id:
                try:
                    ans['rating'] = float(player['stats']['rating'])
                except:
                    pass
                ans['goals'] = player['stats']['goals']['scored']
                ans['shots'] = player['stats']['shots']['shots_total']
                ans['pass'] = player['stats']['passing']['passes']
                ans['shot_on_target'] = player['stats']['shots']['shots_on_goal']
                if player['team_id'] != fixture['localTeam']['data']['id']:
                    ans['host'] = 0
    if ans['attendence'] != 0:
        for goal in fixture['goals']['data']:
            if player_id == goal['player_assist_id']:
                if ans['host']:
                    try:
                        diff =  int(goal['result'].split('-')[0]) - int(goal['result'].split('-')[1])
                    except:
                        ans['attendence'] = 0
                        break
                else:
                    try:
                        diff =  -int(goal['result'].split('-')[0]) - int(goal['result'].split('-')[1])
                    except:
                        ans['attendence'] = 0
                        break
                if diff in [0,1]:
                    ans['goal_classes']['assists']['critica_assist'].append({'minute': goal['minute']})
                elif diff >= useless_range[1] or diff <= useless_range[0]:
                    ans['goal_classes']['assists']['useless_assist'].append({'minute': goal['minute']})
                else:
                    ans['goal_classes']['assists']['plain_assist'].append({'minute': goal['minute']})
            if player_id == goal['player_id']:
                if ans['host']:
                    try:
                        diff =  int(goal['result'].split('-')[0]) - int(goal['result'].split('-')[1])
                    except:
                        ans['attendence'] = 0
                        break
                else:
                    try:
                        diff =  -int(goal['result'].split('-')[0]) - int(goal['result'].split('-')[1])
                    except:
                        ans['attendence'] = 0
                        break
                if diff in [0,1]:
                    ans['goal_classes']['goals']['critica_goal'].append({'minute': goal['minute']})
                elif diff >= useless_range[1] or diff <= useless_range[0]:
                    ans['goal_classes']['goals']['useless_goal'].append({'minute': goal['minute']})
                else:
                    ans['goal_classes']['goals']['plain_goal'].append({'minute': goal['minute']})
   
        # for comment in fixture['comments']['data']:
        #     if DE.player_name[player_id] in comment['comment']:


    return ans