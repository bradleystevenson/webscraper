from object import Object
from table import ObjectTable
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from data_dict_from_object import DataDictFromObject
from common_parser_functions import *


class Coaches(Object):


    def __init__(self, create_from_web):
        self.coaches_table = ObjectTable('coaches', ['coach_id', 'coach_url', 'name', 'start_year', 'end_year', 'active'], 'coach_id')
        super().__init__(create_from_web, [self.coaches_table])

    def _create_from_web(self):
        soup = fetch_soup_from_page("https://www.pro-football-reference.com/coaches/")
        table_parser = TableParser(soup.find(id="coaches"), is_header_numeric, DataDictFromObject({'coach_url': get_url_of_element_with_attributes({'data-stat': 'coach'}),
                                                                                                   'name': get_text_of_element_with_attributes({'data-stat': 'coach'}),
                                                                                                   'active': does_html_object_contain_bold,
                                                                                                   'start_year': get_text_of_element_with_attributes({'data-stat': 'year_min'}),
                                                                                                   'end_year': get_text_of_element_with_attributes({'data-stat': 'year_max'})}))
        self.coaches_table.extend(table_parser.data)