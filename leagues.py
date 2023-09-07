from table import ObjectTable
from webscraper import fetch_soup_from_page


class Leagues:


    def __init__(self, create_from_web):
        self.leagues = ObjectTable('leagues', ['league_id', 'league_name'], 'league_id')
        self.league_years = ObjectTable('league_years', ['league_year_id', 'league_name', 'year', 'league_year_url'],
                                   'league_year_id')
        if create_from_web:
            self._create_from_web()
        else:
            self.leagues.create_from_table()
            self.league_years.create_from_table()

    def insert_data(self):
        self.leagues.insert_data()
        self.league_years.insert_data()

    def _create_from_web(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/years/")
        year_rows = soup.find(id="years").find('tbody').find_all("tr")
        league_years_array = []
        for year_row in year_rows:
            if year_row.find_all("th")[0].text.isnumeric():
                year = int(year_row.find_all("th")[0].text)
                for league_td in year_row.find_all("td")[0].find_all("a"):
                    league_year = {'league_name': league_td.text, 'year': year, 'league_year_url': league_td['href']}
                    league_years_array.append(league_year)
        league_names = []
        for league_year_data in league_years_array:
            if league_year_data['league_name'] not in league_names:
                league_names.append(league_year_data['league_name'])
        for league_name in league_names:
            self.leagues.append({'league_name': league_name})
        for league_year in league_years_array:
            league_id = self.leagues.get_primary_key_by_column_search('league_name', league_year['league_name'])
            league_year['league_id'] = league_id
            self.league_years.append(league_year)