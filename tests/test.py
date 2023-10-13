import unittest
import sys
sys.path.insert(0, '/Users/bradleystevenson/Programs/python-database-wrapper/src/bradleystevenson2015_database')

from database import Database

class TestDatabase(unittest.TestCase):

    def test_initialization(self):
        assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()