import webscraper
from object import Object
from table import ObjectTable
from table_parser import TableParser
from common_parser_functions import *
from data_dict_from_object import DataDictFromObject

class Games(Object):

    def __init__(self, create_from_web, leagues, teams):
        self.games_table = ObjectTable('games', ['game_id', 'home_team_id', 'away_team_id', 'date', 'time', 'home_team_score', 'away_team_score', 'boxscore_url'], 'game_id')
        self.weeks_table = ObjectTable('weeks', ['week_id', 'week_name', 'week_count', 'league_year_id'], 'week_id')
        self.leagues = leagues
        self.teams = teams
        super().__init__(create_from_web, [self.games_table, self.weeks_table])

    def _create_from_web(self):
        for league_dict in self.leagues.league_years.data:
            soup = webscraper.fetch_soup_from_page(f'https://www.pro-football-reference.com/{league_dict["league_year_url"]}games.htm')
            table_parser = TableParser(soup.find(id="games"), does_tr_not_have_thead_class,
                                       DataDictFromObject({
                                           'week': get_text_of_element_at_index("th", 0),
                                            'day': get_text_of_element_with_attributes({"data-stat": 'game_day_of_week'}),
                                            'date': get_text_of_element_with_attributes({"data-stat": "game_date"}),
                                           'time': get_text_of_element_with_attributes({"data-stat": "gametime"}),
                                           'winner': get_element_with_attributes({"data-stat": "winner"}),
                                           'game_location': get_text_of_element_with_attributes({'data-stat': 'game_location'}),
                                           'loser': get_element_with_attributes({'data-stat': 'loser'}),
                                           'winner_score': get_text_of_element_with_attributes({'data-stat': 'pts_win'}),
                                           'loser_score': get_text_of_element_with_attributes({'data-stat': 'pts_lose'}),
                                           'boxscore': get_element_with_attributes({'data-stat': 'boxscore_word'})
                                       }))
            weeks = []
            for data in table_parser.data:
                if data['week'] not in weeks:
                    weeks.append(data['week'])
            week_count = 1
            for week in weeks:
                week_dict = {'week_count': week_count, 'week_name': week, 'league_year_id': league_dict['league_year_id']}
                week_count += 1
                self.weeks_table.append(week_dict)
            print(self.weeks_table.data)