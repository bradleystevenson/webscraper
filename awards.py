from object import Object
from table import Table
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from data_dict_from_object import DataDictFromObject
from common_parser_functions import row_has_link, get_element_with_attributes, get_text_of_element_with_attributes

class Awards(Object):


    def __init__(self, create_from_web, players, coaches):
        self.players = players
        self.coaches = coaches
        self.hall_of_fame_players_table = Table('hall_of_fame_players', ['player_id', 'year_inducted', 'position'])
        self.hall_of_fame_coaches_table = Table('hall_of_fame_coaches', ['coach_id', 'year_inducted'])
        self.hall_of_fame_contributors_table = Table('hall_of_fame_contributors', ['contributor_name', 'year_inducted', 'start_year', 'last_year', 'induction_role', 'roles'])
        self.hall_of_fame_ballots_table = Table('hall_of_fame_ballots', ['year', 'ballot', 'role', 'coach_id', 'player_id', 'inducted'])
        super().__init__(create_from_web, [self.hall_of_fame_players_table, self.hall_of_fame_coaches_table, self.hall_of_fame_contributors_table])

    def _create_from_web(self):
        #self._create_hall_of_fame()
        links = self._create_links()
        self._create_hall_of_fame_ballots(links['hall_of_fame_ballots'])

    def _create_links(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/awards/")
        hall_of_fame_ballot_links = []
        for p in soup.find(text="Pro Football Hall of Fame Balloting").parent.parent.find_all("p"):
            hall_of_fame_ballot_links.append({'year': p.text, 'url': p.find("a")['href']})
        print(hall_of_fame_ballot_links)

        return {'hall_of_fame_ballots': hall_of_fame_ballot_links}


    def _create_hall_of_fame_ballots(self, links):
        for link in links:
            soup = fetch_soup_from_page(f"https://www.pro-football-reference.com{link['url']}")
            table_parser = TableParser(soup.find(id="hofers"), row_has_link, DataDictFromObject({'ballot': get_text_of_element_with_attributes({'data-stat': 'ballot'}),
                                                                                                 'person': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                 'role': get_text_of_element_with_attributes({'data-stat': 'role'})}))
            for data_dict in table_parser.data:
                print(link)
                print(data_dict)
                ballot_dict = {'ballot': data_dict['ballot'], 'role': data_dict['role'], 'inducted': 0, 'coach_id': -1, 'player_id': -1}
                if '*' in data_dict['person'].text:
                    ballot_dict['inducted'] = 1
                if 'coaches' in data_dict['person'].find("a")['href']:
                    ballot_dict['coach_id'] = self.coaches.coaches_table.get_primary_key_by_columns_search({'coach_url': data_dict['person'].find("a")['href']})
                else:
                    ballot_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['person'].find("a")['href']})
                self.hall_of_fame_ballots_table.append(ballot_dict)

    def _create_hall_of_fame(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/hof/")
        table_parser = TableParser(soup.find(id="hof_players"), row_has_link, DataDictFromObject({'player': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                  'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                                                                  'year_inducted': get_text_of_element_with_attributes({'data-stat': 'year_induction'})}))
        for data_dict in table_parser.data:
            hall_of_fame_dict = {'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player'].find("a")['href']}),
                                 'year_inducted': data_dict['year_inducted'], 'position': data_dict['position']}
            self.hall_of_fame_players_table.append(hall_of_fame_dict)
        table_parser = TableParser(soup.find(id="hof_coach"), row_has_link, DataDictFromObject({'coach': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                  'year_inducted': get_text_of_element_with_attributes({'data-stat': 'year_induction'})}))
        for data_dict in table_parser.data:
            hall_of_fame_dict = {'coach_id': self.coaches.coaches_table.get_primary_key_by_columns_search({'coach_url': data_dict['coach'].find("a")['href']}),
                                 'year_inducted': data_dict['year_inducted']}
            self.hall_of_fame_coaches_table.append(hall_of_fame_dict)
        table_parser = TableParser(soup.find(id="hof_exec"), row_has_link, DataDictFromObject({'contributor_name': get_text_of_element_with_attributes({'data-stat': 'player'}),
                                                                                               'year_inducted': get_text_of_element_with_attributes({'data-stat': 'year_induction'}),
                                                                                               'start_year': get_text_of_element_with_attributes({'data-stat': 'year_min'}),
                                                                                               'last_year': get_text_of_element_with_attributes({'data-stat': 'year_max'}),
                                                                                               'induction_role': get_text_of_element_with_attributes({'data-stat': 'role_induction'}),
                                                                                               'roles': get_text_of_element_with_attributes({'data-stat': 'roles'})}))
        self.hall_of_fame_contributors_table.extend(table_parser.data)