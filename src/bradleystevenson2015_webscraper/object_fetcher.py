from .common_webscraper_functions import get_element
from .parser import DataDictParser


class HTMLObjectIteratorFactory:


    def _get_narrow_down_function(self, function_name):
        if function_name == 'row_has_link':
            return row_has_link
        elif function_name == 'true':
            return true
        else:
            raise Exception("No match for narrow down function")
        
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def create(self):
        base_object_fetcher = ObjectFetcherFactory(self.data_dict['base_object'])
        children_object_fetcher = ChildrenObjectFetcher(self.data_dict['children_objects'])
        narrow_down_function = self._get_narrow_down_function(self.data_dict['narrow_down_function'])
        return HTMLObjectIterator(base_object_fetcher, children_object_fetcher, narrow_down_function)


class HTMLObjectIterator:

    def __init__(self, base_object_fetcher, children_object_fetcher, narrow_down_function):
        self.base_object_fetcher = base_object_fetcher
        self.children_object_fetcher = children_object_fetcher 
        self.narrow_down_function = narrow_down_function 

    def get_valid_elements(self, soup):
        return_array = []
        base_object = self.base_object_fetcher(soup)
        for eligible_element in self.children_object_fetcher.fetch_children(base_object):
            if self.narrow_down_function(eligible_element):
                return_array.append(eligible_element)
        return retunr_array




class ObjectFetcherFactory:

    def __init__(self, definition_dict):
        self.definition_dict = definition_dict

    def get_object_fetcher(self):
        child_fetcher = None
        if 'child' in self.definition_dict.keys():
            child_fetcher = ObjectFetcherFactory(self.definition_dict['child']).get_object_fetcher()
        return ObjectFetcher(self.definition_dict, child_fetcher)

class ObjectFetcher:

    def __init__(self, definition_dict, child_fetcher=None):
        self.element_function = get_element(definition_dict)
        self.child_fetcher = child_fetcher 


    def fetch(self, soup): 
        return_element = self.element_function(soup)
        if self.child_fetcher is not None:
            return_element =  self.child_fetcher.fetch(return_element)  
        return return_element

class ChildrenObjectFetcher:

    def __init___(self, definition_dict):
        self.children_element_function = get_children_element(definition_dict)

    def fetch_children(self, soup):
        return self.children_element_function(soup)