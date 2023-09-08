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
        # self.draft_picks_table = ObjectTable('draft_picks', ['year', 'draft_id', 'round', 'pick', 'player_id', 'team_id', 'draft_pick_id'], 'draft_pick_id')
        self.teams = teams
        self.players = players
        self.leagues = leagues
        super().__init__(create_from_web, [self.drafts_table])
        self._create_draft_picks_for_draft({'draft_url': "/years/2023/draft.htm"})

    def _create_from_web(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/draft/")
        table_parser = TableParser(soup.find(id="draft_years"), row_has_link, DataDictFromObject({'draft_url': first_link_url, 'year': first_link_text, 'league_name': first_td_text}))
        for data_dict in table_parser.data:
            data_dict['year'] = int(data_dict['year'])
            data_dict['league_year_id'] = self.leagues.league_years.get_primary_key_by_columns_search({'year': data_dict['year'], 'league_name': data_dict['league_name']})
            self.drafts_table.append(data_dict)

    def _create_draft_picks_for_draft(self, draft):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/" + draft['draft_url'])
        table_parser = TableParser(soup.find(id="drafts"), is_header_numeric, DataDictFromObject({'round': get_first_th_text, 'team_url': first_link_url, 'pick': first_td_text, 'player_url': get_second_link_url, 'position': get_third_td_text}))
        for data_dict in table_parser.data:
            data_dict['team_id'] = self.teams.teams_table.get_primary_key_by_columns_search({'team_url': data_dict['team_url'].replace('_draft', '')})
            try:
                data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']})
            except NoMatchException:
                self.players.create_player(data_dict['player_url'], data_dict['position'])
