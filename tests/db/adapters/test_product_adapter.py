# unit tests of ProductAdapter class

import unittest

from src.db.adapters.product_adapter import ProductAdapter
from src.db.db_connection import DbConnection
from src.db.migrate import migrate_db
from src.db import error
from src.models import products as p

from tests.config import db_config

class TestProductAdapter(unittest.TestCase):
    config_product = dict(
        Name="testProduct", 
        Description="Test description", 
        Quantity=1, 
        Price=1.00
    )
    config_clothing = dict(
        Name="testClothing", 
        Description="Test description", 
        Quantity=5, 
        Price=6.50, 
        Material="Cotton", 
        Size="L", 
        Color="Blue"
    )

    def setUp(self):
        # start each test from a fresh database
        self.db_conn = DbConnection(**db_config)
        self.db_conn._assert_database(db_config["database"])
        migrate_db(self.db_conn, "migrations/")
        self.pa = ProductAdapter(self.db_conn)


    def tearDown(self):
        # remove testing database after each test
        with self.db_conn.get_cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS `{db_config["database"]}`")


    # get_product()
    # testing side effects of insert(), update(), delete()
    def test_get_product(self):
        """
        Inserts, then gets, a product.
        Tests whether the returned product is identical to the inserted one
        """
        product = p.Product(**self.config_product)
        self.pa.insert_product(product)
        obj = self.pa.get_product(1)
        self.assertEqual(obj.Product, product)

    def test_get_product_updated(self):
        """
        Inserts, updates, and gets a product.
        Tests whether the returned product is identical to the updated one
        """
        product = p.Product(**self.config_product)
        self.pa.insert_product(product)
        product.Price = 1000000.95
        self.pa.update_product(1, product)
        obj = self.pa.get_product(1)
        # float() necessary to convert from MySQL Decimal type, for equality check
        self.assertEqual(float(obj.Product.Price), product.Price)

    def test_get_product_deleted(self):
        """
        Inserts, deletes and tries to get a product.
        Should throw an exception.
        (Equivalent to trying to get an ID that doesn't exist in database)
        """
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.delete_product(1)
        with self.assertRaises(error.IdNotPresentError):
            self.pa.get_product(1)

    def test_get_product_several(self):
        obj1 = p.Product(**self.config_product)
        obj2 = p.Clothing(**self.config_clothing)
        self.pa.insert_product(obj1)
        self.pa.insert_product(obj2)
        # getting in reverse order for the heck of it
        robj2 = self.pa.get_product(2)
        robj1 = self.pa.get_product(1)
        self.assertEqual(robj1.Product, obj1)
        self.assertEqual(robj2.Product, obj2)
        self.assertNotEqual(robj1.Product, robj2.Product)


    # insert_product()
    def test_insert_product(self):
        self.pa.insert_product(p.Product(**self.config_product))

    def test_insert_product_subclass(self):
        self.pa.insert_product(p.Clothing(**self.config_clothing))

    def test_insert_product_several(self):
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.insert_product(p.Clothing(**self.config_clothing))

    def test_insert_product_repeats(self):
        self.pa.insert_product(p.Product(**self.config_product))
        with self.assertRaises(error.DuplicateEntryError):
            self.pa.insert_product(p.Product(**self.config_product))


    # update_product()
    def test_update_product(self):
        self.pa.insert_product(p.Product(**self.config_product))

        new_product = p.Product(**self.config_product)
        new_product.Price = 10000.5
        self.pa.update_product(1, new_product)

    def test_update_product_new_class(self):
        """
        Updating Product class product with an instance of a Product subclass.
        This should probably throw an exception.
        """
        self.pa.insert_product(p.Product(**self.config_product))

        actually_clothing = p.Clothing(**self.config_clothing)
        self.pa.update_product(1, actually_clothing)

        obj = self.pa.get_product(1)
        self.assertEqual(obj.Product, actually_clothing)

    def test_update_product_nonexistant(self):
        with self.assertRaises(error.IdNotPresentError):
            self.pa.update_product(500, p.Product(**self.config_product))


    # delete_product()
    def test_delete_product(self):
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.delete_product(1)

    def test_delete_product_reinsert(self):
        """Shouldn't throw a DuplicateEntryError"""
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.delete_product(1)
        self.pa.insert_product(p.Product(**self.config_product))

    def test_delete_product_reinsert_more(self):
        """
        Insert, delete ID 1, insert, delete ID 1 again. 
        Do the auto-incrementing ID's get confused?
        """
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.delete_product(1)
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.delete_product(1)

    def test_delete_product_and_get_newer(self):
        """
        Insert 2 products, delete the first. 
        Can the second be gotten with get_product(2)?
        """
        obj = p.Clothing(**self.config_clothing)
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.insert_product(obj)
        self.pa.delete_product(1)
        robj = self.pa.get_product(2)
        self.assertEqual(robj.Product, obj)

    def test_delete_product_nonexistant(self):
        with self.assertRaises(error.IdNotPresentError):
            self.pa.delete_product(500)


    # get_all_products()
    def test_get_all_products(self):
        self.pa.insert_product(p.Product(**self.config_product))

        items = self.pa.get_all_products(type=None)
        count = 0
        for _ in items:
            count += 1
        self.assertEqual(count, 1)

    def test_get_all_products_several(self):
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.insert_product(p.Clothing(**self.config_clothing))

        items = self.pa.get_all_products(type=None)
        count = 0
        for _ in items:
            count += 1
        self.assertEqual(count, 2)

    def test_get_all_products_one_type(self):
        self.pa.insert_product(p.Product(**self.config_product))
        self.pa.insert_product(p.Clothing(**self.config_clothing))

        items = self.pa.get_all_products(type="Clothing")
        count = 0
        for _ in items:
            count += 1
        self.assertEqual(count, 1)

    def test_get_all_products_bad_filter(self):
        self.pa.insert_product(p.Product(**self.config_product))

        items = self.pa.get_all_products(type="bad_filter_string")
        count = 0
        for _ in items:
            count += 1
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()