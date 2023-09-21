from object import Object
from table import Table, NoMatchException
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from common_parser_functions import *
from data_dict_from_object import DataDictFromObject
class Rosters(Object):

    def __init__(self, create_from_web, players, teams):
        self.players = players
        self.teams = teams
        self.rosters_table = Table('rosters', ['player_id', 'team_id', 'position', 'jersey_number'])
        super().__init__(create_from_web, [self.rosters_table])

    def _create_from_web(self):
        for team in self.teams.teams_table.data:
            print(team)
            url = 'https://www.pro-football-reference.com' + team['team_url'].replace('.htm', '_roster.htm')
            print(url)
            soup = fetch_soup_from_page(url)
            if soup.find(id="roster") is not None:
                table_parser = TableParser(soup.find(id="roster"), is_header_numeric,
                                           DataDictFromObject({'jersey_number': get_text_of_element_with_attributes({'data-stat': 'uniform_number'}),
                                                               'player_url': get_url_of_element_with_attributes({'data-stat': 'player'}),
                                                               'position': get_text_of_element_with_attributes({'data-stat': 'pos'})}, {'team_id': team['team_id']}))
                for data_dict in table_parser.data:
                    try:
                        data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']})
                        self.rosters_table.append(data_dict)
                    except NoMatchException:
                        pass
                    print(data_dict)