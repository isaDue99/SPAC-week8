# unit tests of products module

import unittest

from src.models import products as p


class TestProducts(unittest.TestCase):
    config_product = dict(
        Name="product", 
        Description="description", 
        Quantity=1, 
        Price=1.00
    )
    config_clothing = dict(
        Name="clothing", 
        Description="description", 
        Quantity=1, 
        Price=1.00, 
        Material="cotton", 
        Size="L", 
        Color="blue"
    )

    def setUp(self):
        # example instances from products module, 
        # created "traditionally" using their constructors
        self.product = p.Product(**self.config_product)
        self.clothing = p.Clothing(**self.config_clothing)
    
    # create()
    def test_create(self):
        obj = p.Product.create("Product", **self.config_product)
        # is the object returned equal to self.product?
        self.assertEqual(obj, self.product)

    def test_create_subclass(self):
        obj = p.Product.create("Clothing", **self.config_clothing)
        # is the same true for a subclass of Product?
        self.assertEqual(obj, self.clothing)

    def test_create_bad_type(self):
        with self.assertRaises(ValueError):
            p.Product.create("This is not a valid product type", Name="", Description="", Quantity=0, Price=0.0)


    # create_from_dict()
    def test_create_from_dict(self):
        obj = p.Product.create_from_dict("Product", self.config_product)
        self.assertEqual(obj, self.product)

    def test_create_from_dict_subclass(self):
        obj = p.Product.create_from_dict("Clothing", self.config_clothing)
        self.assertEqual(obj, self.clothing)

    def test_create_from_dict_bad_type(self):
        with self.assertRaises(ValueError):
            p.Product.create_from_dict("This is not a valid product type", self.config_product)

    def test_create_from_dict_bad_dict(self):
        with self.assertRaises(KeyError):
            p.Product.create_from_dict("Product", {"This dict contains invalid keys, such as this one!": "Who cares"})


    # _get_product_class_dynamically()
    def test_get_product_class_dynamically(self):
        c = p.product._get_product_class_dynamically("Product")
        self.assertEqual(c, p.Product)

    def test_get_product_class_dynamically_subclass(self):
        c = p.product._get_product_class_dynamically("Clothing")
        self.assertEqual(c, p.Clothing)


if __name__ == "__main__":
    unittest.main()
