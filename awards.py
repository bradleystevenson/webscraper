from object import Object
from table import Table
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from data_dict_from_object import DataDictFromObject
from common_parser_functions import row_has_link, get_element_with_attributes, get_text_of_element_with_attributes

class Awards(Object):


    def __init__(self, create_from_web, players):
        self.players = players
        self.hall_of_fame_players_table = Table('hall_of_fame_players', ['player_id', 'year_inducted', 'position'])
        super().__init__(create_from_web, [self.hall_of_fame_players_table])

    def _create_from_web(self):
        self._create_hall_of_fame_players()


    def _create_hall_of_fame_players(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/hof/")
        table_parser = TableParser(soup.find(id="hof_players"), row_has_link, DataDictFromObject({'player': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                  'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                                                                  'year_inducted': get_text_of_element_with_attributes({'data-stat': 'year_induction'})}))
        for data_dict in table_parser.data:
            hall_of_fame_dict = {'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player'].find("a")['href']}),
                                 'year_inducted': data_dict['year_inducted'], 'position': data_dict['position']}
            self.hall_of_fame_players_table.append(hall_of_fame_dict)
        table_parser = TableParser(soup.find(id="hof_players"), row_has_link, DataDictFromObject({'player': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                  'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                                                                  'year_inducted': get_text_of_element_with_attributes({'data-stat': 'year_induction'})}))

