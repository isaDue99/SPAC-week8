# unit tests of db_item_descriptor class

import unittest
import datetime

from src.db.db_item_descriptor import DbItemDescriptor


class TestDbItemDescriptor(unittest.TestCase):
    config = dict(
        ID=1,
        Type="Product",
        CreatedAt= datetime.datetime.now,
        LastUpdatedAt= datetime.datetime.now
    )

    def setUp(self):
        # example instance
        # created "traditionally" using constructor
        self.dbid = DbItemDescriptor(**self.config)
    
    # create_from_dict():
    def test_create_from_dict(self):
        obj = DbItemDescriptor.create_from_dict(self.config)
        self.assertEqual(obj, self.dbid)
    
    def test_create_from_dict_bad_dict(self):
        with self.assertRaises(KeyError):
            DbItemDescriptor.create_from_dict({"Not a valid DbItemDescriptor dict": "Not at all"})


if __name__ == "__main__":
    unittest.main()