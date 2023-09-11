import sys
from franchises import Franchises
from leagues import Leagues
from teams import Teams
from players import Players
from drafts import Drafts
from games import Games
from awards import Awards

if __name__ == '__main__':
    which_dicts = {'franchises': False, 'leagues': False, 'teams': False, 'players': False, 'drafts': False, 'games': False,
                   'awards': False}
    for argument in sys.argv:
        which_dicts[argument] = True
    if 'all' in sys.argv:
        for key in which_dicts.keys():
            which_dicts[key] = True
    franchises = Franchises(which_dicts['franchises'])
    leagues = Leagues(which_dicts['leagues'])
    teams = Teams(which_dicts['teams'], franchises, leagues)
    players = Players(which_dicts['players'])
    drafts = Drafts(which_dicts['drafts'], leagues, teams, players)
    #games = Games(which_dicts['games'], leagues, teams)
    awards = Awards(which_dicts['awards'], players)
    franchises.insert_data()
    leagues.insert_data()
    teams.insert_data()
    players.insert_data()
    drafts.insert_data()
    #games.insert_data()
    awards.insert_data()