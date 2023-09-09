import webscraper
from object import Object
from table import ObjectTable
class Games(Object):

    def __init__(self, create_from_web, leagues, teams):
        self.games_table = ObjectTable('games', ['game_id', 'home_team_id', 'away_team_id', 'date', 'time', 'home_team_score', 'away_team_score', 'boxscore_url'], 'game_id')
        self.leagues = leagues
        self.teams = teams
        super().__init__(create_from_web, [self.games_table])

    def _create_from_web(self):
        for league_dict in self.leagues.league_years.data:
            print(league_dict)
            soup = webscraper.fetch_soup_from_page(f'https://www.pro-football-reference.com/{league_dict["league_year_url"]}/games.htm')
            print(soup.find(id="games"))