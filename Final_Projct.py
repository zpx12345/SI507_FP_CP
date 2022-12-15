import Data_Extract as DE
import Data_Process as DP
import json
import pprint
import logging
logging.basicConfig(level=logging.DEBUG)
pp = pprint.PrettyPrinter(indent=4)
class tree:
    root_player_id = None
    Player_tree = (None, [], [])
    season_name = None
    season_id = None

def build_tree(player_id, team_id, season_id):
    DP.process_fixture(player_id, team_id, tree.season_name)
    teammate_ids = DE.get_teammate(player_id, team_id, season_id)
    teammate_trees = []
    dig_into_teammates = None
    skip_teamates = None
    while  skip_teamates not in ['y','n']:
        skip_teamates = input(f"do you want to skip {DE.cache.player_id_to_name[player_id]}'s teammates?(y/n)")
        
    if skip_teamates == 'n':
        while dig_into_teammates not in ['y','n']:
            dig_into_teammates = input(f"do you want to dig into {DE.cache.player_id_to_name[player_id]}'s teammates?(y/n)")
        if dig_into_teammates == 'y':
            for teammate_id in teammate_ids:
                teammate_trees.append(build_teammate_tree(teammate_id, season_id, team_id, False))
        else:
            for teammate_id in teammate_ids:
                DP.process_fixture(teammate_id, team_id, tree.season_name)
                teammate_trees.append((teammate_id, None, None))
    else:
        teammate_trees = None
    compititor_trees = build_compititor_trees(team_id, season_id, player_id)
    return(player_id, teammate_trees, compititor_trees)

def build_teammate_tree(player_id, season_id, team_id, build_teammate):
    DP.process_fixture(player_id, team_id, tree.season_name)
    compititor_trees = None
    dig_into_compititors = None
    while dig_into_compititors not in ['y', 'n']:
        dig_into_compititors = input(f"do you want to dig into {DE.cache.player_id_to_name[player_id]}'s compitors?(y/n)")
    if dig_into_compititors == 'y':
        compititor_trees = build_compititor_trees(team_id, season_id, player_id)
    else:
        compititor_trees = None
    return(player_id, None, compititor_trees)

def build_compititor_trees(except_team_id, season_id, father_player_id):
    ans = []
    while True:
        add_more = input(f"add more {DE.cache.player_id_to_name[father_player_id]}'s compititors?(y/n)")
        if add_more == 'n':
            break
        if add_more == 'y':
            DE.get_team(except_team_id,  get_season_=False, get_league_=False)
            team_id, nomatter, nomatter, player_id = DE.get_team_player(season_id, choose_season=False)
            ans.append(build_tree(player_id, team_id, season_id))
    if ans == []:
        return None
    return ans



def main():
    DE.get_league()
    DE.get_team()
    team_id, tree.season_name, tree.season_id, player_id = DE.get_team_player()
    tree.root_player_id = player_id
    tree.Player_tree = build_tree(player_id, team_id, tree.season_id)
    while True:
        save = input("do you want to save this tree structure?(y/n)")
        if save in ['n', 'y']:
            break
    if save == 'y':
        with open('tree', 'w') as file:
            json.dump(tree.Player_tree, file)
    DP.compare_average_critical_goal(tree.Player_tree)
if __name__ == "__main__":
    main()