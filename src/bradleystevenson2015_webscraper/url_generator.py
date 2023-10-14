class URLGenerator:

    def __init__(self, base_url, iterator=None):
        self.iterator = iterator
        self.base_url = base_url

    def generate_urls(self, webscraper_object_collection):
        return_strings = []
        if self.iterator is None:
            return_strings.append(self.base_url)
            return return_strings
        for iteration_string in self.iterator.generate_iterations(webscraper_object_collection):
            return_strings.append(self.base_url.replace('{replace}', iteration_string))
        return return_strings

class URLIteratorFactory():

    def __init__(self, url_iterator_dict):
        self.url_iterator_dict = url_iterator_dict

    def get_url_iterator(self):
        if 'hardcoded' in self.url_iterator_dict.keys():
            return HardcodedURLIterator(self.url_iterator_dict['hardcoded'])
        elif 'object' in self.url_iterator_dict.keys():
            return ObjectURLIterator(self.url_iterator_dict['object'])
        else:
            raise Exception("No match for url iterator type")

class URLIterator():

    def __init__(self):
        pass

    def generate_iterations(self, webscraper_object_collection):
        pass

class HardcodedURLIterator(URLIterator):

    def __init__(self, hardcoded_strings):
        self.hardcoded_strings = hardcoded_strings
        super().__init__()
    
    def generate_iterations(self, webscraper_object_collection):
        return self.hardcoded_strings

class ObjectURLIterator(URLIterator):

    def __init__(self, object_name):
        self.object_name = object_name
        super().__init__()

    def generate_iterations(self, webscraper_object_collection):
        return_strings = []
        for data_dict in webscraper_object_collection.databaseObject.tables[self.object_name].data:
            return_strings.append(data_dict['url'])
        return return_strings
    
class URLGeneratorFactory:

    def __init__(self, url_dict):
        self.url_dict = url_dict

    def get_url_generator(self):
        if 'iterator' in self.url_dict.keys():
            return URLGenerator(self.url_dict['base_url'], URLIteratorFactory(self.url_dict['iterator']).get_url_iterator())
        else:
            return URLGenerator(self.url_dict['base_url'])