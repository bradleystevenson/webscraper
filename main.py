import sys
from franchises import Franchises
from leagues import Leagues
from teams import Teams
from players import Players
from drafts import Drafts
from games import Games

if __name__ == '__main__':
    which_dicts = {'franchises': False, 'leagues': False, 'teams': False, 'players': False, 'drafts': False, 'games': False}
    for argument in sys.argv[1:]:
        if argument not in which_dicts.keys() and argument != 'all':
            print(f'Argument {argument} is not a valid object, failing')
            exit(1)
    for argument in sys.argv:
        which_dicts[argument] = True
    if 'all' in sys.argv:
        for key in which_dicts.keys():
            which_dicts[key] = True
    franchises = Franchises(which_dicts['franchises'])
    print('Finished franchises')
    leagues = Leagues(which_dicts['leagues'])
    print('Finished leagues')
    teams = Teams(which_dicts['teams'], franchises, leagues)
    print('Finished teams')
    players = Players(which_dicts['players'])
    print('Finished players')
    drafts = Drafts(which_dicts['drafts'], leagues, teams, players)
    print('Finished drafts')
    games = Games(which_dicts['games'], leagues, teams)
    print('Finished games')
    franchises.insert_data()
    leagues.insert_data()
    teams.insert_data()
    players.insert_data()
    drafts.insert_data()
