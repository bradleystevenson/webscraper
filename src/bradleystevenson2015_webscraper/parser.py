from .common_webscraper_functions import fetch_soup_from_page, row_has_link, get_tr_of_stats_table, get_tr_of_table_with_id, true
from .field_parser import FieldParserFactory
from .object_fetcher import ObjectFetcherFactory, HTMLObjectIterator, HTMLObjectIteratorFactory
import logging

class CreateFromPageParserFactory:

    def __init__(self, create_from_page_parser_dict) -> None:
        self.create_from_page_parser = CreateFromPageParser(create_from_page_parser_dict['base_url'], DataDictParserFactory(create_from_page_parser_dict['parser']).create())


class CreateFromPageParser:

    def __init__(self, base_url, data_dict_parser) -> None:
        self.base_url = base_url
        self.data_dict_parser = data_dict_parser

    def parse(self, url, webscraperObjectCollection):
        soup = fetch_soup_from_page(self.base_url + url)
        data_dict = self.data_dict_parser.parse(soup, {}, webscraperObjectCollection)
        data_dict['url'] = url
        return data_dict

class TableParserObject:

    def __init__(self, all_object_selection_function, narrow_down_function, data_dict_parser):
        self.all_object_selection_function = all_object_selection_function
        self.narrow_down_function = narrow_down_function
        self.data_dict_parser = data_dict_parser

    def parse_page(self, soup, data_dict, webscraperObjectCollection):
        return_array = []
        for eligible_element in self.all_object_selection_function(soup):
            if self.narrow_down_function(eligible_element):
                return_array.append(self.data_dict_parser.parse(eligible_element, data_dict, webscraperObjectCollection))
        return return_array

class GenericParserObject:

    def __init__(self, html_object_iterator: HTMLObjectIterator, data_dict_parser):
        self.html_object_iterator = html_object_iterator
        self.data_dict_parser = data_dict_parser

    def parse_page(self, soup, data_dict, webscraper_object_collection):
        return_array = []
        for eligible_element in self.html_object_iterator.get_valid_elements(soup):
            return_array.append(self.data_dict_parser.parse(eligible_element, data_dict, webscraper_object_collection))
        return return_array 

class ParserObject:

    def __init__(self, base_object_function, children_element_function):
        self.base_object_function = base_object_function
        self.children_element_function = children_element_function

    def parse_page(self, soup, data_dict, webscraperObjectCollection):
        return_array = []
        for eligible_element in self.children_element_function(self.base_object_function(soup)):
            return_array.append(self.data_dict_parser.parse(eligible_element, data_dict, webscraperObjectCollection))
        return return_array

class ParserObjectFactory:

    def __init__(self, parser_dict):
        self.parser_dict = parser_dict
        html_object_iterator = HTMLObjectIteratorFactory(parser_dict['html_object_iterator']).create()
        data_dict_parser = DataDictParserFactory(parser_dict['data_dict_parser']).create()
        self.parser = GenericParserObject(html_object_iterator, data_dict_parser)


class DataDictParserFactory:

    def __init__(self, data_dict_parser_dict):
        self.data_dict_parser_dict = data_dict_parser_dict

    def create(self):
        field_parsers = []
        for field_dict in self.data_dict_parser_dict:
            field_parsers.append(FieldParserFactory(field_dict).create())
        return DataDictParser(field_parsers)

class DataDictParser:

    def __init__(self, field_parsers):
        self.field_parsers = field_parsers

    def parse(self, html_object, data_dict, webscraperObject):
        return_dict = {}
        for field_parser in self.field_parsers:
            return_dict[field_parser.field_name] = field_parser.parse(html_object, data_dict, webscraperObject)
        return return_dict