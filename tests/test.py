import unittest
import sys
sys.path.insert(0, '/Users/bradleystevenson/Programs/webscraper/src/bradleystevenson2015_webscraper')

from webscraper_object import WebscraperObjectCollection

class TestDatabase(unittest.TestCase):

    def test_initialization(self):
        webscraperObjects = WebscraperObjectCollection("webscraper_schema.json", "../../databases/webscraper-database.db", "database_schema.json", [])
        webscraperObjects.run(['main.py'])

if __name__ == '__main__':
    unittest.main()