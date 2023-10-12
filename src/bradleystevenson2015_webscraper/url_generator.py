class URLGenerator:

    def __init__(self, base_url, iterator=None):
        self.iterator = iterator
        self.base_url = base_url

    def generate_urls(self, webscraper_object_collection):
        return_strings = []
        if self.iterator is None:
            return_strings.append(self.base_url)

class URLGeneratorFactory:

    def __init__(self, url_dict):
        self.url_dict = url_dict

    def get_url_generator(self):
        if 'iterator' in url_dict.keys():
            pass
        else:
            return URLGenerator(self.url_dict['base_url'])