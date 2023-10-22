from bradleystevenson2015_database import database
import json
from bradleystevenson2015_webscraper.common_webscraper_functions import fetch_soup_from_page
from bradleystevenson2015_webscraper.parser import CreateFromPageParserFactory, ParserObjectFactory
from bradleystevenson2015_webscraper.url_generator import URLGeneratorFactory
import logging


class WebscraperObjectCollection:

    def __init__(self, webscraper_schema_filepath, database_path, database_schema_filepath, custom_objects):
        self.databaseObject = database.Database(database_path, database_schema_filepath)
        self._create_webscraper_objects(webscraper_schema_filepath, custom_objects)


    def _create_webscraper_objects(self, webscraper_schema_filepath, custom_objects):
        self.webscrapers = []
        file = open(webscraper_schema_filepath)
        data = json.load(file)
        file.close()
        for webscraper_object in data['objects']:
            self.webscrapers.append(WebscraperObjectFactory(webscraper_object, custom_objects).webscraper)


    def get_webscraper_object_with_name(self, object_name):
        for webscraper in self.webscrapers:
            if webscraper.object_name == object_name:
                return webscraper

    def run(self, arguments):
        if '--create-tables' in arguments:
            self.databaseObject.create_tables()
            exit(0)
        create_from_web_dict = self._parse_arguments(arguments)
        for webscraper in self.webscrapers:
            webscraper.create(create_from_web_dict[webscraper.object_name], self)
        self.databaseObject.insert_into_database()

    def _parse_arguments(self, arguments):
        logging.info("[WEBSCRAPER] [_PARSE_ARGUMENTS] " + str(arguments))
        return_dict = {}
        for webscraper in self.webscrapers:
            return_dict[webscraper.object_name] = False
        for argument in arguments[1:]:
            if argument not in return_dict.keys() and argument != 'all':
                raise Exception("No match for object name")
            return_dict[argument] = True
        if 'all' in arguments[1:]:
            for key in return_dict.keys():
                return_dict[key] = True
        return return_dict


class WebscraperObject:

    def __init__(self, object_name, tables, create_from_page_parser=None):
        self.object_name = object_name
        self.tables = tables
        self.create_from_page_parser = create_from_page_parser

    def create(self, create_from_web, webscraperObjectCollection):
        logging.info("[WebscraperObject] [create] " + self.object_name + " " + str(create_from_web))
        if create_from_web:
            self.create_from_web(webscraperObjectCollection)
        else:
            self.create_from_database(webscraperObjectCollection)

    def create_from_web(self, webscraperObjectCollection):
        pass

    def create_from_database(self, webscraperObjectCollection):
        for table_name in self.tables:
            webscraperObjectCollection.databaseObject.tables[table_name].generate_from_database()

    def create_from_page(self, url, webscraperObjectCollection):
        if self.create_from_page_parser is None:
            raise Exception("We have no way to create this object")
        data_dict = self.create_from_page_parser.parse(url, webscraperObjectCollection)
        data_dict['url'] = url
        return webscraperObjectCollection.databaseObject.tables[self.tables[0]].append(data_dict)
    
class NewWebscraperObject(WebscraperObject):

    def __init__(self, object_name, parsers, url_generator, create_from_page_parser):
        self.object_name = object_name
        self.parsers = parsers
        self.create_from_page_parser = create_from_page_parser
        self.url_generator = url_generator
        super().__init__(object_name, [object_name], create_from_page_parser)

    def create_from_web(self, webscraperObjectCollection):
        for url_dict in self.url_generator.generate_urls(webscraperObjectCollection):
            soup = fetch_soup_from_page(url_dict['url'])
            for parser in self.parsers:
                data = parser.parse_page(soup, url_dict['data_dict'], webscraperObjectCollection)
                for data_dict in data:
                    webscraperObjectCollection.databaseObject.tables[self.object_name].append(data_dict)


class WebscraperObjectFactory:

    def __init__(self, webscraper_object_dict, custom_objects):
        self.create_from_page_parser = None
        if 'create_from_page_parser' in webscraper_object_dict.keys():
            self.create_from_page_parser =  CreateFromPageParserFactory(webscraper_object_dict['create_from_page_parser']).create_from_page_parser
        if 'object_type' not in webscraper_object_dict.keys():
            parsers = []
            for parser_dict in webscraper_object_dict['parsers']:
                parsers.append(ParserObjectFactory(parser_dict).parser)
            url_generator = URLGeneratorFactory(webscraper_object_dict['urls'])
            self.webscraper = NewWebscraperObject(webscraper_object_dict['object_name'], parsers, url_generator.get_url_generator(), self.create_from_page_parser)
        elif webscraper_object_dict['object_type'] == 'custom_object':
            for custom_object in custom_objects:
                if custom_object.object_name == webscraper_object_dict['object_name']:
                    self.webscraper = custom_object
        else:
            raise Exception("No match for object type")