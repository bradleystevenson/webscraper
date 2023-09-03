from bs4 import BeautifulSoup
import requests
import os
from table import Table
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

def create_teams():
    url = "https://www.sofascore.com/pt/futebol/2018-09-18"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')

    teams = Table('teams', ['team_id', 'team_name', 'team_url', 'active'])
    team_rows = soup.find(id="div_teams_active").find_all("th")
    team_id = 1
    for team_row in team_rows:
        if team_row.find("a") is not None:
            team = {'team_name': team_row.text, 'team_url': team_row.find('a')['href'], 'team_id': team_id, 'active': 1}
            team_id += 1
            teams.append(team)
    page = requests.get('https://www.pro-football-reference.com/teams/')
    soup = BeautifulSoup(page.content, "html.parser")
    team_rows = soup.find(id="teams_inactive")
    print(team_rows)
    return teams

def remove_old_database():
    try:
        os.remove("/Users/administrator/Programs/football_grid_trainer/database.db")
    except OSError:
        print("Could not remove file")

if __name__ == '__main__':
    remove_old_database()
    teams = create_teams()
    teams.create_table()
    teams.insert_data()
