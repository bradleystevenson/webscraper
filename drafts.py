from object import Object
from table import ObjectTable
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from common_parser_functions import *
from data_dict_from_object import DataDictFromObject
from exceptions import NoMatchException

class Drafts(Object):


    def __init__(self, create_from_web, leagues, teams, players):
        self.drafts_table = ObjectTable('drafts', ['year', 'league_year_id', 'draft_url', 'draft_id'], 'draft_id')
        self.draft_picks_table = ObjectTable('draft_picks', ['year', 'draft_id', 'round', 'pick', 'player_id', 'team_id', 'draft_pick_id', 'player_name'], 'draft_pick_id')
        self.draft_transactions_table = ObjectTable('draft_transactions', ['draft_transaction_id', 'draft_id', 'transaction_date', 'transaction_string'], 'draft_transaction_id')
        self.teams = teams
        self.players = players
        self.leagues = leagues
        super().__init__(create_from_web, [self.drafts_table, self.draft_picks_table, self.draft_transactions_table])

    def _create_from_web(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/draft/")
        table_parser = TableParser(soup.find(id="draft_years"), row_has_link, DataDictFromObject({'draft_url': get_url_of_element_at_index("a", 0), 'year': get_text_of_element_at_index("a", 0), 'league_name': get_text_of_element_at_index("td", 0)}))
        for data_dict in table_parser.data:
            data_dict['year'] = int(data_dict['year'])
            data_dict['league_year_id'] = self.leagues.league_years.get_primary_key_by_columns_search({'year': data_dict['year'], 'league_name': data_dict['league_name']})
            self.drafts_table.append(data_dict)
        for draft_data in self.drafts_table.data:
            self._create_draft_picks_for_draft(draft_data)

    def _create_draft_picks_for_draft(self, draft):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/" + draft['draft_url'])
        table_parser = TableParser(soup.find(id="drafts"), is_header_numeric, DataDictFromObject({'round': get_text_of_element_with_attributes({'data-stat': 'draft_round'}),
                                                                                                  'team_url': get_url_of_element_at_index("a", 0),
                                                                                                  'pick': get_text_of_element_with_attributes(
                                                                                                      {'data-stat': 'draft_pick'}),
                                                                                                  'player': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                  'position': get_text_of_element_with_attributes({'data-stat': 'pos'})}))
        for data_dict in table_parser.data:
            data_dict['team_id'] = self.teams.teams_table.get_primary_key_by_columns_search({'team_url': data_dict['team_url'].replace('_draft', '')})
            if data_dict['player'].find('a') is not None:
                data_dict['player_name'] = ''
                try:
                    data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search(
                        {'player_url': data_dict['player_url']})
                except NoMatchException:
                    data_dict['player_id'] = self.players.create_player(data_dict['player_url'], data_dict['position'])
            else:
                data_dict['player_name'] = data_dict['player'].text
                data_dict['player_id'] = -1
            self.draft_picks_table.append(data_dict)
        transactions = soup.find(id='div_transactions')
        data_dict_from_object = DataDictFromObject({'transaction_date': get_text_of_element_at_index("b", 0), 'transaction_string': get_text_after_colon})
        for p in transactions.find_all('p'):
            draft_transaction_dict = data_dict_from_object.parse(p)
            draft_transaction_dict['draft_id'] = draft['draft_id']
            self.draft_transactions_table.append(draft_transaction_dict)
