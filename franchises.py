from table import ObjectTable
from common_parser_functions import *
from table_parser import TableParser
from webscraper import fetch_soup_from_page
from data_dict_from_object import DataDictFromObject
class Franchises:

    def __init__(self, create_from_web):
        self.franchises_table = ObjectTable('franchises', ['franchise_id', 'franchise_name', 'franchise_url', 'active'], 'franchise_id')
        if create_from_web:
            self._create_from_web()
        else:
            self.franchises_table.create_from_table()
    def _create_from_web(self):
        url = 'https://www.pro-football-reference.com/teams/'
        soup = fetch_soup_from_page(url)
        table_parser = TableParser(soup.find(id="teams_active"), row_has_link, DataDictFromObject(
            {'franchise_name': first_link_text, 'franchise_url': first_link_url, 'active': one}))
        for franchise_row in table_parser.data:
            self.franchises_table.append(franchise_row)
        table_parser = TableParser(soup.find(id="teams_inactive"), row_has_link, DataDictFromObject({'franchise_name': first_link_text, 'franchise_url': first_link_url, 'active': zero}))
        for franchise_row in table_parser.data:
            self.franchises_table.append(franchise_row)

    def insert_data(self):
        self.franchises_table.insert_data()