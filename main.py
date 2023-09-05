from bs4 import BeautifulSoup
import os
from table import Table, ObjectTable
from selenium import webdriver
import selenium
import sys
import threading
from string import ascii_uppercase


franchises = Table('franchises', ['franchise_id', 'franchise_name', 'franchise_url', 'active'])
leagues = ObjectTable('leagues', ['league_id', 'league_name'], 'league_id')
league_years = ObjectTable('league_years', ['league_year_id', 'league_name', 'year', 'league_year_url'],
                           'league_year_id')
teams = ObjectTable('teams', ['franchise_id', 'year', 'team_url', 'league_year_id', 'team_id'], 'team_id')
players = ObjectTable('players', ['player_id', 'hall_of_fame', 'active', 'player_url', 'player_name', 'position'], 'player_id')
drafts = ObjectTable('drafts', ['year', 'league_year_id', 'draft_url', 'draft_id'], 'draft_id')
draft_picks = ObjectTable('draft_picks', ['year', 'draft_id', 'round', 'pick', 'player_id', 'team_id', 'draft_pick_id'], 'draft_pick_id')
def fetch_soup_from_page(url):
    while True:
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            page = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except selenium.common.exceptions.TimeoutException:
            print("Timed out loading page, trying again")
        except selenium.common.exceptions.WebDriverException:
            print("Web Driver Error, trying again")

def create_franchises():
    url = 'https://www.pro-football-reference.com/teams/'
    soup = fetch_soup_from_page(url)
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
    league_names = []
    for league_year_data in league_years_array:
        if league_year_data['league_name'] not in league_names:
            league_names.append(league_year_data['league_name'])
    for league_name in league_names:
        leagues.append({'league_name': league_name})
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



def create_teams_for_franchise(franchise):
    soup = fetch_soup_from_page("https://www.pro-football-reference.com/" + franchise['franchise_url'])
    teams_rows = soup.find(id="team_index").find("tbody").find_all("tr")
    return_array = []
    for team_row in teams_rows:
        if team_row.find('a') is not None and team_row.find('a').text.isnumeric():
            team_dict = {'year': int(team_row.find('a').text), 'team_url': team_row.find('a')['href'],
                         'league_year_id': league_years.get_primary_key_by_column_search('league_year_url', team_row.find_all('a')[1]['href']),
                         'franchise_id': franchise['franchise_id']}
            return_array.append(team_dict)
    return return_array
def create_teams():
    teams_array = []
    for franchise in franchises.data:
        teams_array.extend(create_teams_for_franchise(franchise))
    for team in teams_array:
        teams.append(team)

def create_players():
    for letter in ascii_uppercase:
        print(letter)
        soup = fetch_soup_from_page(f'https://www.pro-football-reference.com/players/{letter}')
        player_rows = soup.find(id="div_players").find_all('p')
        for player_row in player_rows:
            player = {'player_url': player_row.find('a')['href'], 'player_name': player_row.find('a').text, 'position': player_row.text.split('(')[1].split(')')[0]}
            active = 0
            if player_row.find('b') is not None:
                active = 1
            player['active'] = active
            hall_of_fame = 0
            if '+' in player_row.text:
                hall_of_fame = 1
            player['hall_of_fame'] = hall_of_fame
            players.append(player)

def create_draft_picks_for_draft(draft):
    soup = fetch_soup_from_page("https://www.pro-football-reference.com/" + draft['draft_url'])
    print(soup)
    draft_rows = soup.find(id="drafts").find("tbody").find_all("tr")
    for draft_row in draft_rows:
        if draft_row.find('th').text.isnumeric():
            print(draft_row)
            draft_pick = {'round': int(draft_row.find('th').text), 'pick': int(draft_row.find_all('td')[0].text),
                          'team_id': teams.get_primary_key_by_columns_search({'team_url': draft_row.find('a')['href'].replace('_draft', '')}),
                          'player_id': players.get_primary_key_by_columns_search({'player_url', draft_row.find_all('a')[1]['href']})}
            print(draft_row.find('a')['href'])
            print(draft_pick)
def create_draft_picks():
    for draft in drafts.data:
        create_draft_picks_for_draft(draft)
def create_drafts():
    soup = fetch_soup_from_page("https://www.pro-football-reference.com/draft/")
    draft_rows = soup.find(id="draft_years").find('tbody').find_all('tr')
    for draft_row in draft_rows:
        if draft_row.find('a') is not None:
            league_name = draft_row.find('td').text
            year = int(draft_row.find('a').text)
            draft_dict = {'draft_url': draft_row.find('a')['href'], 'year': draft_row.find('a').text, 'league_year_id': league_years.get_primary_key_by_columns_search({'year': year, 'league_name': league_name})}
            drafts.append(draft_dict)


if __name__ == '__main__':
    which_dicts = {'franchises': False, 'leagues': False, 'teams': False, 'players': False, 'drafts': False}
    for argument in sys.argv:
        which_dicts[argument] = True
    if 'all' in sys.argv:
        for key in which_dicts.keys():
            which_dicts[key] = True
    if which_dicts['franchises']:
        create_franchises()
    else:
        franchises.create_from_table()
    if which_dicts['leagues']:
        create_years()
    else:
        leagues.create_from_table()
        league_years.create_from_table()
    if which_dicts['teams']:
        create_teams()
    else:
        teams.create_from_table()
    if which_dicts['players']:
        create_players()
    else:
        players.create_from_table()
    if which_dicts['drafts']:
        create_drafts()
    else:
        drafts.create_from_table()
    #create_draft_picks_for_draft({'draft_url': "/years/2023/draft.htm"})
    franchises.insert_data()
    leagues.insert_data()
    league_years.insert_data()
    teams.insert_data()
    players.insert_data()
    drafts.insert_data()
