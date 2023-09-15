import webscraper
from object import Object
from table import Table, ObjectTable, NoMatchException
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from data_dict_from_object import DataDictFromObject
from common_parser_functions import row_has_link, get_element_with_attributes, get_text_of_element_with_attributes, is_header_numeric, get_url_of_element_with_attributes

class Awards(Object):


    def __init__(self, create_from_web, players, coaches, executives):
        self.players = players
        self.coaches = coaches
        self.executives = executives
        self.hall_of_fame_players_table = Table('hall_of_fame_players', ['player_id', 'year_inducted', 'position'])
        self.hall_of_fame_coaches_table = Table('hall_of_fame_coaches', ['coach_id', 'year_inducted'])
        self.hall_of_fame_contributors_table = Table('hall_of_fame_contributors', ['contributor_name', 'year_inducted', 'start_year', 'last_year', 'induction_role', 'roles'])
        self.hall_of_fame_ballots_table = Table('hall_of_fame_ballots', ['year', 'ballot', 'role', 'name', 'coach_id', 'player_id', 'executive_id', 'inducted'])
        self.top_100_players_table = Table('top_100_players', ['year', 'player_id'])
        self.all_pro_awards_table = ObjectTable('all_pro_awards', ['all_pro_award_id', 'award_name'], 'all_pro_award_id')
        self.all_pro_players_table = Table('all_pro_players', ['player_id', 'team_tier', 'all_pro_award_id', 'year', 'position'])
        self.other_all_pro_players_table = Table('other_all_pro_players', ['player_id', 'team_tier', 'all_pro_award_id', 'year', 'position', 'league'])
        self.awards_table = ObjectTable('awards', ['award_name', 'award_id'], 'award_id')
        self.awards_voting_summary_table = Table('awards_voting_summary', ['award_id', 'year', 'player_id', 'coach_id', 'vote_points', 'first_place_votes', 'share'])
        self.all_decade_teams_table = ObjectTable('all_decade_teams', ['all_decade_team_name', 'all_decade_team_id'], 'all_decade_team_id')
        self.all_decade_team_players_table = Table('all_decade_team_players', ['all_decade_team_id', 'year', 'position', 'player_id'])
        self.all_rookie_teams_table = Table('all_rookie_teams', ['player_id', 'position', 'year'])
        self.player_of_the_weeks_table = Table('player_of_the_weeks', ['player_id', 'year', 'month', 'conference', 'unit'])
        self.player_of_the_months_table = Table('player_of_the_months', ['player_id', 'year', 'month', 'unit'])
        self.rookie_of_the_months_table = Table('player_of_the_months', ['player_id', 'year', 'month', 'unit'])
        self.players_of_the_week_table = Table('players_of_the_week', ['player_id', 'year', 'week', 'unit', 'text'])
        super().__init__(create_from_web, [self.hall_of_fame_players_table, self.hall_of_fame_coaches_table, self.hall_of_fame_contributors_table,
                                           self.hall_of_fame_ballots_table, self.top_100_players_table, self.all_pro_awards_table,
                                           self.all_pro_players_table, self.other_all_pro_players_table,
                                           self.awards_table, self.awards_voting_summary_table,
                                           self.all_decade_teams_table, self.all_decade_team_players_table,
                                           self.all_rookie_teams_table])

    def _create_from_web(self):
        # self._create_hall_of_fame()
        # links = self._create_links()
        # self._create_players_of_the_week()
        # self._create_top_100(links['top_100_players'])
        # self._create_hall_of_fame_ballots(links['hall_of_fame_ballots'])
        # self._create_nfl_all_pros(links['all_pros'])
        # self._create_other_all_pros(links['other_all_pros'])
        # self._create_voting_summaries(links['voting_summaries'])
        # self._create_all_decade_teams(links['all_decade_teams'])
        # self._create_all_rookie_teams([{'year': '2022', 'url': '/awards/nfl-all-rookie-2022.htm'}])
        # self._create_rookies_of_the_month()
        self._create_players_of_the_week()
        pass

    def _create_players_of_the_week(self):
        soup = fetch_soup_from_page('https://www.pro-football-reference.com/awards/players-of-the-week.htm')
        table_parser = TableParser(soup.find(id="nfl_potw"), is_header_numeric,
                                   DataDictFromObject({'year': get_text_of_element_with_attributes({'data-stat': 'year_id'}),
                                                       'week': get_text_of_element_with_attributes({'data-stat': 'week_num'}),
                                                       'afc_offensive_player': get_element_with_attributes({'data-stat': 'afc_offense'}),
                                                       'afc_defensive_player': get_element_with_attributes({'data-stat': 'afc_defense'}),
                                                       'afc_special_teams_player': get_element_with_attributes({'data-stat': 'afc_st'}),
                                                       'nfc_offensive_player': get_element_with_attributes({'data-stat': 'nfc_offense'}),
                                                       'nfc_defensive_player': get_element_with_attributes({'data-stat': 'nfc_defense'}),
                                                       'nfc_special_teams_player': get_element_with_attributes({'data-stat': 'nfc_st'})
                                                       }))
        for data_dict in table_parser.data:
            if data_dict['afc_offensive_player'].find('a') is not None:
                try:
                    self.players_of_the_week_table.append({
                                                       'player_id': self.players.players_table.get_primary_key_by_columns_search(
                                                           {'player_url': data_dict['afc_offensive_player'].find("a")[
                                                               'href']}),
                                                       'year': data_dict['year'], 'week': data_dict['week'],
                                                       'conference': 'AFC', 'unit': 'Offense', 'text': ''})
                except NoMatchException:
                    print("No match for url" + data_dict['afc_offensive_player'].find("a")['href'])
            else:
                self.players_of_the_week_table.append({
                    'player_id': -1,
                    'year': data_dict['year'], 'week': data_dict['week'],
                    'conference': 'AFC', 'unit': 'Offense', 'text': data_dict['afc_offensive_player'].text})
            if data_dict['afc_defensive_player'].find('a') is not None:
                try:
                    self.players_of_the_week_table.append({
                                                       'player_id': self.players.players_table.get_primary_key_by_columns_search(
                                                           {'player_url': data_dict['afc_defensive_player'].find("a")[
                                                               'href']}),
                                                       'year': data_dict['year'], 'week': data_dict['week'],
                                                       'conference': 'AFC', 'unit': 'Defense', 'text': ''})
                except NoMatchException:
                    print("No match for " + data_dict['afc_defensive_player'].find('a')['href'])
            else:
                self.players_of_the_week_table.append({
                    'player_id': -1,
                    'year': data_dict['year'], 'week': data_dict['week'],
                    'conference': 'AFC', 'unit': 'Defense', 'text': data_dict['afc_defensive_player'].text})

            if data_dict['nfc_offensive_player'].find('a') is not None:
                try:
                    self.players_of_the_week_table.append({
                                                           'player_id': self.players.players_table.get_primary_key_by_columns_search(
                                                           {'player_url': data_dict['nfc_offensive_player'].find("a")[
                                                               'href']}),
                                                       'year': data_dict['year'], 'week': data_dict['week'],
                                                       'conference': 'NFC', 'unit': 'Offense', 'text': ''})
                except NoMatchException:
                    print("Player URL doesnt exist")
            else:
                self.players_of_the_week_table.append({
                    'player_id': -1,
                    'year': data_dict['year'], 'week': data_dict['week'],
                    'conference': 'NFC', 'unit': 'Offense', 'text': data_dict['nfc_offensive_player'].text})

            if data_dict['nfc_defensive_player'].find('a') is not None:
                try:
                    self.players_of_the_week_table.append({
                                                       'player_id': self.players.players_table.get_primary_key_by_columns_search(
                                                           {'player_url': data_dict['nfc_defensive_player'].find("a")[
                                                               'href']}),
                                                       'year': data_dict['year'], 'week': data_dict['week'],
                                                       'conference': 'NFC', 'unit': 'Defense', 'text': ''})
                except NoMatchException:
                    print("no match exception")
            else:
                self.players_of_the_week_table.append({
                    'player_id': -1,
                    'year': data_dict['year'], 'week': data_dict['week'],
                    'conference': 'NFC', 'unit': 'Defense', 'text': data_dict['nfc_defensive_player'].text})
            if data_dict['afc_special_teams_player'] is not None:
                try:
                    self.players_of_the_week_table.append({
                                                           'player_id': self.players.players_table.get_primary_key_by_columns_search(
                                                               {'player_url':
                                                                    data_dict['afc_special_teams_player'].find("a")[
                                                                        'href']}),
                                                           'year': data_dict['year'], 'week': data_dict['week'],
                                                           'conference': 'AFC', 'unit': 'Special Teams'})
                except NoMatchException:
                    print("No match exception")
            if data_dict['nfc_special_teams_player'] is not None:
                try:
                    self.players_of_the_week_table.append({
                                                           'player_id': self.players.players_table.get_primary_key_by_columns_search(
                                                               {'player_url':
                                                                    data_dict['nfc_special_teams_player'].find("a")[
                                                                        'href']}),
                                                           'year': data_dict['year'], 'week': data_dict['week'],
                                                           'conference': 'NFC', 'unit': 'Special Teams'})
                except NoMatchException:
                    print("No match exception")
    def _create_rookies_of_the_month(self):
        table_parser = TableParser(fetch_soup_from_page('https://www.pro-football-reference.com/awards/rookies-of-the-month.htm').find(id="potm_rookie"), is_header_numeric,
                                   DataDictFromObject({'year': get_text_of_element_with_attributes({'data-stat': 'year_id'}),
                                                       'month': get_text_of_element_with_attributes({'data-stat': 'month_num'}),
                                                       'offensive_player_url': get_url_of_element_with_attributes({'data-stat': 'off'}),
                                                       'defensive_player_url': get_url_of_element_with_attributes({'data-stat': 'def'})}))
        for data_dict in table_parser.data:
            self.rookie_of_the_months_table.append({'year': data_dict['year'], 'month': data_dict['month'],
                                                    'unit': 'Offense',
                                                    'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['offensive_player_url']})})
            self.rookie_of_the_months_table.append({'year': data_dict['year'], 'month': data_dict['month'],
                                                    'unit': 'Defense',
                                                    'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['defensive_player_url']})})


    def _create_players_of_the_month(self):
        table_parser = TableParser(fetch_soup_from_page('https://www.pro-football-reference.com/awards/players-of-the-month.htm').find(id="potm"), row_has_link,
                                                        DataDictFromObject({'year': get_text_of_element_with_attributes({'data-stat': 'year_id'}),
                                                                            'month': get_text_of_element_with_attributes({'data-stat': 'month_num'}),
                                                                            'afc_offensive_player': get_element_with_attributes({'data-stat': 'afc_off'}),
                                                                            'afc_defensive_player': get_element_with_attributes({'data-stat': 'afc_def'}),
                                                                            'afc_special_teams_player': get_element_with_attributes({'data-stat': 'afc_st'}),
                                                                            'nfc_offensive_player': get_element_with_attributes({'data-stat': 'nfc_off'}),
                                                                            'nfc_defensive_player': get_element_with_attributes({'data-stat': 'nfc_def'}),
                                                                            'nfc_special_teams_player': get_element_with_attributes({'data-stat': 'nfc_st'})
                                                                            }))
        for data_dict in table_parser.data:
            self.player_of_the_months_table.append({'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['afc_offensive_player'].find("a")['href']}),
                                                   'year': data_dict['year'], 'month': data_dict['month'],
                                                   'conference': 'AFC', 'unit': 'Offense'})
            self.player_of_the_months_table.append({'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['afc_defensive_player'].find("a")['href']}),
                                                   'year': data_dict['year'], 'month': data_dict['month'],
                                                   'conference': 'AFC', 'unit': 'Defense'})
            self.player_of_the_months_table.append({'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['nfc_offensive_player'].find("a")['href']}),
                                                   'year': data_dict['year'], 'month': data_dict['month'],
                                                   'conference': 'NFC', 'unit': 'Offense'})
            self.player_of_the_months_table.append({'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['nfc_defensive_player'].find("a")['href']}),
                                                   'year': data_dict['year'], 'month': data_dict['month'],
                                                   'conference': 'NFC', 'unit': 'Defense'})
            if data_dict['afc_special_teams_player'].find('a') is not None:
                self.player_of_the_months_table.append({'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['afc_special_teams_player'].find("a")['href']}),
                                                        'year': data_dict['year'], 'month': data_dict['month'],
                                                        'conference': 'AFC', 'unit': 'Special Teams'})
            if data_dict['nfc_special_teams_player'].find('a') is not None:
                self.player_of_the_months_table.append({'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['nfc_special_teams_player'].find("a")['href']}),
                                                        'year': data_dict['year'], 'month': data_dict['month'],
                                                        'conference': 'NFC', 'unit': 'Special Teams'})


    def _create_all_rookie_teams(self, links):
        for link in links:
            table_parser = TableParser(webscraper.fetch_soup_from_page('https://www.pro-football-reference.com' + link['url']).find(id="all_rookie"), row_has_link,
                                       DataDictFromObject({'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                           'player_url': get_url_of_element_with_attributes({'data-stat': 'player'})},
                                                          {'year': link['year']}))
            for data_dict in table_parser.data:
                data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']})
                self.all_rookie_teams_table.append(data_dict)
    def _create_all_decade_teams(self, links):
        for link in links:
            table_parser = TableParser(webscraper.fetch_soup_from_page('https://www.pro-football-reference.com' + link['url']).find(id="all_decade"), row_has_link,
                                       DataDictFromObject({'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                           'player_url': get_url_of_element_with_attributes({'data-stat': 'player'})}))

            try:
                all_decade_team_id = self.all_decade_teams_table.get_primary_key_by_columns_search({'all_decade_team_name': link['award']})
            except NoMatchException:
                all_decade_team_id = self.all_decade_teams_table.append({'all_decade_team_name': link['award']})
            for data_dict in table_parser.data:
                data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']})
                data_dict['all_decade_team_id'] = all_decade_team_id
                self.all_decade_teams_table.append(data_dict)

    def _create_voting_summaries(self, links):
        for link in links:
            soup = webscraper.fetch_soup_from_page(f'https://www.pro-football-reference.com{link["url"]}')
            for table_wrapper in soup.find_all("div", {'class': "table_wrapper"}):
                award_name = table_wrapper.find("h2").text.replace(' Voting', '')
                try:
                    award_id = self.awards_table.get_primary_key_by_columns_search({'award_name': award_name})
                except NoMatchException:
                    award_id = self.awards_table.append({'award_name': award_name})
                table_parser = TableParser(table_wrapper.find("table"), is_header_numeric, DataDictFromObject({'player_element': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                               'coach_element': get_element_with_attributes({'data-stat': 'coach'}),
                                                                                            'vote_points': get_text_of_element_with_attributes({'data-stat': 'votes'}),
                                                                                            'first_place_votes': get_text_of_element_with_attributes({'data-stat': 'votes_first'}),
                                                                                            'share': get_text_of_element_with_attributes({'data-stat': 'share'})}))
                for data_dict in table_parser.data:
                    data_dict['player_id'] = -1
                    data_dict['coach_id'] = -1
                    data_dict['award_id'] = award_id
                    if data_dict['player_element'] is not None:
                        data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_element'].find('a')['href']})
                    if data_dict['coach_element'] is not None:
                        data_dict['coach_id'] = self.coaches.coaches_table.get_primary_key_by_columns_search({'coach_url': data_dict['coach_element'].find('a')['href']})
                    self.awards_voting_summary_table.append(data_dict)


    def _create_other_all_pros(self, links):
        for link in links:
            table_parser = TableParser(fetch_soup_from_page(f'https://www.pro-football-reference.com{link["url"]}').find(id="all_pro"),
                                       row_has_link, DataDictFromObject({'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                                         'player_url': get_url_of_element_with_attributes({'data-stat': 'player'}),
                                                                         'all_pros': get_text_of_element_with_attributes({'data-stat': 'all_pro_string'})}))
            for data_dict in table_parser.data:
                for all_pro in data_dict['all_pros'].split(', '):
                    all_pro_name = all_pro.split(':')[0]
                    team_tier = all_pro.split(':')[1]
                    try:
                        all_pro_award_id = self.all_pro_awards_table.get_primary_key_by_columns_search({'award_name': all_pro_name})
                    except NoMatchException:
                        all_pro_award_id = self.all_pro_awards_table.append({'award_name': all_pro_name})
                    self.all_pro_players_table.append({'all_pro_award_id': all_pro_award_id, 'team_tier': team_tier, 'year': link['year'],
                                                       'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']}),
                                                       'position': data_dict['position'], 'league': link['league']})

    def _create_nfl_all_pros(self, links):
        for link in links:
            table_parser = TableParser(fetch_soup_from_page(f'https://www.pro-football-reference.com{link["url"]}').find(id="all_pro"),
                                       row_has_link, DataDictFromObject({'position': get_text_of_element_with_attributes({'data-stat': 'pos'}),
                                                                         'player_url': get_url_of_element_with_attributes({'data-stat': 'player'}),
                                                                         'all_pros': get_text_of_element_with_attributes({'data-stat': 'all_pro_string'})}))
            for data_dict in table_parser.data:
                for all_pro in data_dict['all_pros'].split(', '):
                    print(all_pro)
                    all_pro_name = all_pro.split(':')[0]
                    team_tier = all_pro.split(':')[1]
                    try:
                        all_pro_award_id = self.all_pro_awards_table.get_primary_key_by_columns_search({'award_name': all_pro_name})
                    except NoMatchException:
                        all_pro_award_id = self.all_pro_awards_table.append({'award_name': all_pro_name})
                    self.all_pro_players_table.append({'all_pro_award_id': all_pro_award_id, 'team_tier': team_tier, 'year': link['year'],
                                                       'player_id': self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']}),
                                                       'position': data_dict['position']})


    def _create_top_100(self, links):
        for link in links:
            table_parser = TableParser(fetch_soup_from_page('https://www.pro-football-reference.com' + link['url']).find(id="top_100"),
                                       is_header_numeric,
                                       DataDictFromObject({'player_url': get_url_of_element_with_attributes({'data-stat': 'player'})}, hardcoded_dict={'year': link['year']}))
            for data_dict in table_parser.data:
                print(data_dict)
                data_dict['player_id'] = self.players.players_table.get_primary_key_by_columns_search({'player_url': data_dict['player_url']})
                self.top_100_players_table.append(data_dict)

    def _create_links(self):
        return_dict = {'hall_of_fame_ballots': [], 'top_100_players': [], 'all_pros': [], 'other_all_pros': [],
                       'voting_summaries': [], 'all_decade_teams': [], 'all_rookie_teams': [], 'defunct_awards': [], 'awards': []}
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/awards/")
        for p in soup.find(text="Pro Football Hall of Fame Balloting").parent.parent.find_all("p"):
            return_dict['hall_of_fame_ballots'].append({'year': p.text, 'url': p.find("a")['href']})
        for p in soup.find(text="NFL Top 100 Players").parent.parent.find_all("p"):
            return_dict['top_100_players'].append({'url': p.find("a")['href'], 'year': p.text.split(' ')[0]})
        for p in soup.find(text="NFL All-Pros").parent.parent.find_all("p"):
            return_dict['all_pros'].append({'url': p.find("a")['href'], 'year': p.text})
        for p in soup.find(text="Other All-Pros").parent.parent.find_all("p"):
            return_dict['other_all_pros'].append({'year': p.text.split(' ')[0], 'league': p.text.split(' ')[1], 'url': p.find("a")['href']})
        for p in soup.find(text='Football Award Voting Summaries').parent.parent.find_all('p'):
            return_dict['voting_summaries'].append({'year': p.text, 'url': p.find('a')['href']})
        for p in soup.find(text="All-Decade Teams").parent.parent.find_all('p'):
            return_dict['all_decade_teams'].append({'year': p.text.split('-')[1], 'url': p.find('a')['href'],
                                                    'award': p.text.split(' All')[0]})
        for p in soup.find(text="NFL All-Rookie Teams").parent.parent.find_all('p'):
            return_dict['all_rookie_teams'].append({'year': p.text.split(' ')[0], 'url': p.find('a')['href']})
        for p in soup.find(text="Defunct Awards").parent.parent.find_all('p'):
            return_dict['defunct_awards'].append({'url': p.find('a')['href'], 'award_name': p.find('a').text, 'leagues': p.find('span').text.split(', ')[0].split(',')})
        for p in soup.find(text="Pro Football Awards").parent.parent.find_all("p"):
            return_dict['awards'].append({'url': p.find('a')['href'], 'award_name': p.text})
        return return_dict



    def _create_hall_of_fame_ballots(self, links):
        for link in links:
            soup = fetch_soup_from_page(f"https://www.pro-football-reference.com{link['url']}")
            table_parser = TableParser(soup.find(id="hofers"), is_header_numeric, DataDictFromObject({'ballot': get_text_of_element_with_attributes({'data-stat': 'ballot'}),
                                                                                                 'person': get_element_with_attributes({'data-stat': 'player'}),
                                                                                                 'role': get_text_of_element_with_attributes({'data-stat': 'role'})}))
            for data_dict in table_parser.data:
                ballot_dict = {'ballot': data_dict['ballot'], 'role': data_dict['role'], 'inducted': 0, 'coach_id': -1, 'player_id': -1, 'executive_id': -1, 'name': ''}
                if '*' in data_dict['person'].text:
                    ballot_dict['inducted'] = 1
                if data_dict['person'].find("a") is None:
                    ballot_dict['name'] = data_dict['person'].text.replace('*', '')
                else:
                    if 'coaches' in data_dict['person'].find("a")['href']:
                        try:
                            ballot_dict['coach_id'] = self.coaches.coaches_table.get_primary_key_by_columns_search({'coach_url': data_dict['person'].find("a")['href']})
                        except NoMatchException:
                            ballot_dict['name'] = data_dict['person'].text.replace('*', '')
                    elif 'executives' in data_dict['person'].find("a")['href']:
                        if data_dict['person'].find("a")['href'] == '/executives/.htm':
                            ballot_dict['name'] = data_dict['person'].text.replace('*', '')
                        else:
                            ballot_dict['executive_id'] = self.executives.executives_table.get_primary_key_by_columns_search({'executive_url': data_dict['person'].find("a")['href']})
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