import unittest
import sys
sys.path.insert(0, '/Users/bradleystevenson/Programs/webscraper/src/bradleystevenson2015_webscraper')

from webscraper_object import WebscraperObjectCollection
from url_generator import URLGeneratorFactory

class TestDatabase(unittest.TestCase):

    def test_initialization(self):
        webscraperObjects = WebscraperObjectCollection("webscraper_schema.json", "../../databases/webscraper-database.db", "database_schema.json", [])
        webscraperObjects.run(['main.py'])

    def test_url_generator_base_only(self):
        url_generator = URLGeneratorFactory({ "base_url": "https://www.basketball-reference.com"}).get_url_generator()
        self.assertEqual(url_generator.generate_urls(None), ["https://www.basketball-reference.com"])

    def test_url_generator_hardcoded(self):
        url_generator = URLGeneratorFactory({"base_url": "https://www.basketball-reference.com/players/{replace}/", 'iterator': {'hardcoded': ['a', 'b']}}).get_url_generator()
        self.assertEqual(url_generator.generate_urls(None), ['https://www.basketball-reference.com/players/a/', 'https://www.basketball-reference.com/players/b/'])
if __name__ == '__main__':
    unittest.main()