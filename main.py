import sys
from franchises import Franchises
from leagues import Leagues
from teams import Teams
from players import Players
from drafts import Drafts
from games import Games
from awards import Awards
from coaches import Coaches
from executives import Executives

if __name__ == '__main__':
    which_dicts = {'franchises': False, 'leagues': False, 'teams': False, 'players': False, 'drafts': False, 'games': False,
                   'awards': False, 'coaches': False, 'executives': False}
    for argument in sys.argv:
        which_dicts[argument] = True
    if 'all' in sys.argv:
        for key in which_dicts.keys():
            which_dicts[key] = True
    objects = {'franchises': Franchises(which_dicts['franchises']),
               'leagues': Leagues(which_dicts['leagues']),
               'players': Players(which_dicts['players']),
               'coaches': Coaches(which_dicts['coaches']),
               'executives': Executives(which_dicts['executives'])
               }
    objects['teams'] = Teams(which_dicts['teams'], objects['franchises'], objects['leagues'])
    objects['drafts'] = Drafts(which_dicts['drafts'], objects['leagues'], objects['teams'], objects['players'])
    objects['awards'] = Awards(which_dicts['awards'], objects['players'], objects['coaches'], objects['executives'])
    #games = Games(which_dicts['games'], leagues, teams)
    #awards = Awards(which_dicts['awards'], players, coaches)
    for key in objects.keys():
        objects[key].insert_data()