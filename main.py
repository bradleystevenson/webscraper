from bs4 import BeautifulSoup
import os
from table import Table, ObjectTable
from selenium import webdriver

def fetch_soup_from_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def create_franchises():
    url = 'https://www.pro-football-reference.com/teams/'
    soup = fetch_soup_from_page(url)
    franchises = Table('franchises', ['franchise_id', 'franchise_name', 'franchise_url', 'active'])
    franchise_rows = soup.find(id="div_teams_active").find_all("th")
    franchise_id = 1
    for franchise_row in franchise_rows:
        if franchise_row.find("a") is not None:
            franchise = {'franchise_name': franchise_row.text, 'franchise_url': franchise_row.find('a')['href'], 'franchise_id': franchise_id, 'active': 1}
            franchise_id += 1
            franchises.append(franchise)
    franchise_rows = soup.find(id="teams_inactive").find_all("th")
    for franchise_row in franchise_rows:
        if franchise_row.find("a") is not None:
            franchise = {'franchise_name': franchise_row.text, 'franchise_url': franchise_row.find('a')['href'], 'franchise_id': franchise_id, 'active': 0}
            franchise_id += 1
            franchises.append(franchise)
    return franchises

def create_years():
    soup = fetch_soup_from_page("https://www.pro-football-reference.com/years/")
    year_rows = soup.find(id="years").find('tbody').find_all("tr")
    league_years_array = []
    for year_row in year_rows:
        if year_row.find_all("th")[0].text.isnumeric():
            year = int(year_row.find_all("th")[0].text)
            for league_td in year_row.find_all("td")[0].find_all("a"):
                league_year = {'league_name': league_td.text, 'year': year, 'league_year_url': league_td['href']}
                league_years_array.append(league_year)
    leagues = ObjectTable('leagues', ['league_id', 'league_name'], 'league_id')
    league_names = []
    for league_year_data in league_years_array:
        if league_year_data['league_name'] not in league_names:
            league_names.append(league_year_data['league_name'])
    for league_name in league_names:
        leagues.append({'league_name': league_name})
    league_years = ObjectTable('league_years', ['league_year_id', 'league_name', 'year', 'league_year_url'], 'league_year_id')
    for league_year in league_years_array:
        league_id = leagues.get_primary_key_by_column_search('league_name', league_year['league_name'])
        league_year['league_id'] = league_id
        league_years.append(league_year)
    return {'leagues': leagues, 'league_years': league_years}
def remove_old_database():
    try:
        os.remove("/Users/administrator/Programs/football_grid_trainer/database.db")
    except OSError:
        print("Could not remove file")

if __name__ == '__main__':
    remove_old_database()
    #franchises = create_franchises()
    temp = create_years()
    league_years = temp['league_years']
    leagues = temp['leagues']
    leagues.create_table()
    leagues.insert_data()
    league_years.create_table()
    league_years.insert_data()
    #franchises.create_table()
    #franchises.insert_data()
