from table import ObjectTable
from common_parser_functions import *
from table_parser import TableParser
from webscraper import fetch_soup_from_page
from data_dict_from_object import DataDictFromObject
from object import Object


class Franchises(Object):

    def __init__(self, create_from_web):
        self.franchises_table = ObjectTable('franchises', ['franchise_id', 'franchise_name', 'franchise_url', 'active'], 'franchise_id')
        super().__init__(create_from_web, [self.franchises_table])

    def _create_from_web(self):
        url = 'https://www.pro-football-reference.com/teams/'
        soup = fetch_soup_from_page(url)
        table_parser = TableParser(soup.find(id="teams_active"), row_has_link, DataDictFromObject(
            {'franchise_name': get_text_of_element_at_index("a", 0), 'franchise_url': get_url_of_element_at_index("a", 0), 'active': one}))
        for franchise_row in table_parser.data:
            self.franchises_table.append(franchise_row)
        table_parser = TableParser(soup.find(id="teams_inactive"), row_has_link, DataDictFromObject(
            {'franchise_name': get_text_of_element_at_index("a", 0), 'franchise_url': get_url_of_element_at_index("a", 0), 'active': zero}))
        for franchise_row in table_parser.data:
            self.franchises_table.append(franchise_row)
