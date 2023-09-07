import os
from table import Table, ObjectTable
import sys
from string import ascii_uppercase
from webscraper import fetch_soup_from_page
from franchises import Franchises
from leagues import Leagues
from teams import Teams

franchises = None
leagues = None
teams = None
teams = ObjectTable('teams', ['franchise_id', 'year', 'team_url', 'league_year_id', 'team_id'], 'team_id')
players = ObjectTable('players', ['player_id', 'hall_of_fame', 'active', 'player_url', 'player_name', 'position'], 'player_id')
drafts = ObjectTable('drafts', ['year', 'league_year_id', 'draft_url', 'draft_id'], 'draft_id')
draft_picks = ObjectTable('draft_picks', ['year', 'draft_id', 'round', 'pick', 'player_id', 'team_id', 'draft_pick_id'], 'draft_pick_id')



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
                          'player_id': players.get_primary_key_by_columns_search({'player_url': draft_row.find_all('a')[1]['href']})}
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
    franchises = Franchises(which_dicts['franchises'])
    leagues = Leagues(which_dicts['leagues'])
    teams = Teams(which_dicts['teams'], franchises, leagues)
    if which_dicts['players']:
        create_players()
    else:
        players.create_from_table()
    if which_dicts['drafts']:
        create_drafts()
    else:
        drafts.create_from_table()
    # create_draft_picks_for_draft({'draft_url': "/years/2023/draft.htm"})
    franchises.insert_data()
    leagues.insert_data()
    teams.insert_data()
    players.insert_data()
    drafts.insert_data()
