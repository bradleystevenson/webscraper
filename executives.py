from object import Object
from table import ObjectTable
from webscraper import fetch_soup_from_page
from table_parser import TableParser
from data_dict_from_object import DataDictFromObject
from common_parser_functions import *
class Executives(Object):


    def __init__(self, create_from_web):
        self.executives_table = ObjectTable('executives', ['executive_id', 'name', 'executive_url'], 'executive_id')
        super().__init__(create_from_web, [self.executives_table])

    def _create_from_web(self):
        table_parser = TableParser(fetch_soup_from_page("https://www.pro-football-reference.com/executives/").find(id="executives"), is_header_numeric,
                                   DataDictFromObject({'name': get_text_of_element_with_attributes({'data-stat': 'exec'}),
                                                       'executive_url': get_url_of_element_with_attributes({'data-stat': 'exec'})}))
        self.executives_table.extend(table_parser.data)