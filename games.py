import webscraper
from object import Object
from table import ObjectTable
from table_parser import TableParser
from common_parser_functions import *
from data_dict_from_object import DataDictFromObject
from table import NoMatchException

class Games(Object):

    def __init__(self, create_from_web, leagues, teams):
        self.games_table = ObjectTable('games', ['game_id', 'home_team_id', 'away_team_id', 'day_of_week', 'date', 'time', 'home_team_score', 'away_team_score', 'boxscore_url', 'home_team_name', 'away_team_name', 'league_year_id', 'home_team_name', 'away_team_name'], 'game_id')
        self.weeks_table = ObjectTable('weeks', ['week_id', 'week_name', 'week_count', 'league_year_id'], 'week_id')
        self.leagues = leagues
        self.teams = teams
        super().__init__(create_from_web, [self.games_table, self.weeks_table])

    def _create_from_web(self):
        for league_dict in self.leagues.league_years.data:
            soup = webscraper.fetch_soup_from_page(f'https://www.pro-football-reference.com/{league_dict["league_year_url"]}games.htm')
            table_parser = TableParser(soup.find(id="games"), does_element_not_have_strong_and_does_tr_not_have_thead_class,
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
            for data in table_parser.data:
                if data['winner'].find("a") is not None:
                    winning_team_id = self.teams.teams_table.get_primary_key_by_columns_search({'team_url': data['winner'].find("a")['href']})
                    winning_team_name = ''
                else:
                    winning_team_id = -1
                    winning_team_name = data['winner'].text
                if data['loser'].find("a") is not None:
                    losing_team_id = self.teams.teams_table.get_primary_key_by_columns_search({'team_url': data['loser'].find("a")['href']})
                    losing_team_name = ''
                else:
                    losing_team_id = -1
                    losing_team_name = data['loser'].text

                if data['game_location'] == '@':
                    home_team_id = losing_team_id
                    home_team_score = data['loser_score']
                    home_team_name = losing_team_name
                    away_team_id = winning_team_id
                    away_team_score = data['winner_score']
                    away_team_name = winning_team_name
                elif data['game_location'] == '':
                    home_team_id = winning_team_id
                    home_team_score = data['winner_score']
                    home_team_name = winning_team_name
                    away_team_id = losing_team_id
                    away_team_score = data['loser_score']
                    away_team_name = losing_team_name
                else:
                    raise Exception("No match for game location")
                boxscore_url = ''
                if data['boxscore']:
                    boxscore_url = data['boxscore'].find("a")['href']
                game_dict = {'day_of_week': data['day'], 'date': data['date'], 'time': data['time'],
                             'week_id': self.weeks_table.get_primary_key_by_columns_search(
                                 {'league_year_id': league_dict['league_year_id'],
                                  'week_name': data['week']}),
                             'home_team_id': home_team_id,
                             'away_team_id': away_team_id,
                             'home_team_score': home_team_score,
                             'away_team_score': away_team_score,
                             'home_team_name': home_team_name,
                             'away_team_name': away_team_name,
                             'league_year_id': league_dict['league_year_id'],
                             'boxscore_url': boxscore_url}
