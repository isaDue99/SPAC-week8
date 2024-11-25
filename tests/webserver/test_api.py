# unit tests of webserver/api.py, the backend letting clients interact with the database

import unittest

from src.webserver.api import api
api.testing = True

from src.db.db_connection import DbConnection
from src.db.db_item_descriptor import DbItemDescriptor
from src.db.migrate import migrate_db
from src.models import products as p
from tests.config import db_config


class Testapi(unittest.TestCase):
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

    def tearDown(self):
        # remove testing database after each test
        with self.db_conn.get_cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS `{db_config["database"]}`")


    # get_product()
    def test_get_product(self):
        """Add, then get product. The request should return status code 200 and the Product and DbItemDescriptor objects"""
        with api.test_client() as client:
            data = {"Type": "Product", "Product": self.config_product}
            client.post('/api/product', json=data)
            
            res = client.get('/api/product/1')
            self.assertEqual(res.status_code, 200)
            product = p.Product.create_from_dict("Product", eval(res.data)[0]["Product"])
            # dbid wont be used for assert but this is just to check if the returned dict is valid
            dbid = DbItemDescriptor.create_from_dict(eval(res.data)[0]["Descriptor"])

            # eval() doesn't convert the float in the response to a float type
            # so this typecasting is just to help out
            # ideally there should be a function that unwraps backend responses properly
            product.Price = float(product.Price)
            self.assertEqual(product, p.Product(**self.config_product))

    def test_get_product_nonexistant(self):
        """Get a product that doesnt exists. Should give errorcode 400"""
        with api.test_client() as client:            
            res = client.get('/api/product/500')
            self.assertEqual(res.status_code, 400)


    # get_products()
    def test_get_products(self):
        with api.test_client() as client:
            client.post('/api/product', json={"Type": "Product", "Product": self.config_product})
            res = client.get('/api/products')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(eval(res.data)), 1)
            product = p.Product.create_from_dict("Product", eval(res.data)[0]["Product"])
            # eval() doesn't convert the float in the response to a float type
            # so this typecasting is just to help out
            # ideally there should be a function that unwraps backend responses properly
            product.Price = float(product.Price)
            self.assertEqual(product, p.Product(**self.config_product))

    def test_get_products_several(self):
        with api.test_client() as client:
            # add 2 products
            client.post('/api/product', json={"Type": "Product", "Product": self.config_product})
            client.post('/api/product', json={"Type": "Clothing", "Product": self.config_clothing})
            # check that we get 2 back
            res = client.get('/api/products')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(eval(res.data)), 2)

    def test_get_products_filter(self):
        with api.test_client() as client:
            # add 2 products
            client.post('/api/product', json={"Type": "Product", "Product": self.config_product})
            client.post('/api/product', json={"Type": "Clothing", "Product": self.config_clothing})
            # get only one of them
            res = client.get('/api/products?type_filter=Clothing')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(eval(res.data)), 1)
            # check that it's the right one
            product = p.Product.create_from_dict("Clothing", eval(res.data)[0]["Product"])
            # eval() doesn't convert the float in the response to a float type
            # so this typecasting is just to help out
            # ideally there should be a function that unwraps backend responses properly
            product.Price = float(product.Price)
            self.assertEqual(product, p.Clothing(**self.config_clothing))

    def test_get_products_bad_filter(self):
        with api.test_client() as client:
            client.post('/api/product', json={"Type": "Product", "Product": self.config_product})
            res = client.get('/api/products?type_filter=bad_filter_string')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(eval(res.data)), 0)
            

    # add_product()
    def test_add_product(self):
        with api.test_client() as client:
            data = {"Type": "Product", "Product": self.config_product}
            res = client.post('/api/product', json=data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), "Success")

    def test_add_product_duplicate(self):
        """Add the same product twice, should return status 400"""
        with api.test_client() as client:
            data = {"Type": "Product", "Product": self.config_product}
            client.post('/api/product', json=data)
            res = client.post('/api/product', json=data)
            self.assertEqual(res.status_code, 400)


    # set_product()
    def test_set_product(self):
        with api.test_client() as client:
            # add a product
            prod = p.Product(**self.config_product)
            data = {"Type": "Product", "Product": prod}
            client.post('/api/product', json=data)

            # change our product, and set it
            prod.Name = "I've been changed"
            res = client.put('/api/product/1', json=data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), "Success")

            # get it and check its the updated one we get
            res = client.get('api/product/1')
            product = p.Product.create_from_dict("Product", eval(res.data)[0]["Product"])

            # eval() doesn't convert the float in the response to a float type
            # so this typecasting is just to help out
            # ideally there should be a function that unwraps backend responses properly
            product.Price = float(product.Price)
            self.assertEqual(product, prod)

    def test_set_product_nonexistant(self):
        with api.test_client() as client:
            # set a product that hasnt been added first
            prod = p.Product(**self.config_product)
            data = {"Type": "Product", "Product": prod}
            res = client.put('/api/product/1', json=data)
            self.assertEqual(res.status_code, 400)


    # delete_product()
    def test_delete_product(self):
        with api.test_client() as client:
            # add a product
            prod = p.Product(**self.config_product)
            data = {"Type": "Product", "Product": prod}
            client.post('/api/product', json=data)

            # delete it
            res = client.delete('/api/product/1')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_data(as_text=True), "Success")

            # trying to get it should give 400
            res = client.get('api/product/1')
            self.assertEqual(res.status_code, 400)

    def test_delete_product_nonexistant(self):
        with api.test_client() as client:
            # delete a product that doesnt exist
            res = client.delete('/api/product/500')
            # should give 400
            self.assertEqual(res.status_code, 400)

    # _validate_product_request()

    # _validate_product_request_fields()


if __name__ == "__main__":
    unittest.main()
