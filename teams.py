from table import ObjectTable
from object import Object
from webscraper import fetch_soup_from_page

class Teams(Object):


    def __init__(self, create_from_web, franchises, leagues):
        self.teams_table = ObjectTable('teams', ['franchise_id', 'year', 'team_url', 'league_year_id', 'team_id'], 'team_id')
        self.franchises = franchises
        self.leagues = leagues
        super().__init__(create_from_web, [self.teams_table])

    def create_teams_for_franchise(self, franchise):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/" + franchise['franchise_url'])
        teams_rows = soup.find(id="team_index").find("tbody").find_all("tr")
        return_array = []
        for team_row in teams_rows:
            if team_row.find('a') is not None and team_row.find('a').text.isnumeric():
                team_dict = {'year': int(team_row.find('a').text), 'team_url': team_row.find('a')['href'],
                             'league_year_id': self.leagues.league_years.get_primary_key_by_column_search('league_year_url',
                                                                                             team_row.find_all('a')[1][
                                                                                                 'href']),
                             'franchise_id': franchise['franchise_id']}
                return_array.append(team_dict)
        return return_array
    def _create_from_web(self):
        teams_array = []
        for franchise in self.franchises.franchises_table.data:
            teams_array.extend(self.create_teams_for_franchise(franchise))
        for team in teams_array:
            self.teams_table.append(team)