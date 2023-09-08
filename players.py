from object import Object
from table import ObjectTable
from webscraper import fetch_soup_from_page
from string import ascii_uppercase
from common_parser_functions import *
from data_dict_from_object import DataDictFromObject

class Players(Object):

    def __init__(self, create_from_web):
        self.players_table = ObjectTable('players', ['player_id', 'hall_of_fame', 'active', 'player_url', 'player_name', 'position'], 'player_id')
        super().__init__(create_from_web, [self.players_table])


    def _create_from_web(self):
        data_dict_from_object = DataDictFromObject({'player_url': first_link_url, 'player_name': first_link_text,
                                                    'position': get_text_in_parantheses,
                                                    'active': does_html_object_contain_bold,
                                                    'hall_of_fame': is_plus_in_html_object_text})
        for letter in ascii_uppercase:
            soup = fetch_soup_from_page(f'https://www.pro-football-reference.com/players/{letter}')
            player_rows = soup.find(id="div_players").find_all('p')
            for player_row in player_rows:
                self.players_table.append(data_dict_from_object.parse(player_row))

    def create_player(self, player_url, player_position):
        soup = fetch_soup_from_page(f'https://www.pro-football-reference.com{player_url}')
        print(soup)
        data_dict = {'player_url': player_url, 'player_name': soup.find("h1").text, 'position': player_position, 'hall_of_fame': 0, 'active': 0}
