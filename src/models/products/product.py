# classes detailing products in the storage system

from dataclasses import dataclass
from typing import Any, Self

# For the getattr function
from .. import products


def _get_product_class_dynamically(type: str):
    product_class = getattr(products, type)
    return product_class


@dataclass(kw_only=True)
class Product:
    Name: str
    Description: str
    Quantity: int  # in storage / in stock
    Price: float

    @staticmethod
    def create(type: str, **attributes) -> Self:
        try:
            product_class = _get_product_class_dynamically(type)
            product_instance = product_class(**attributes)

            return product_instance
        except AttributeError:
            raise ValueError(f"Unknown product type")

    """
    The base generic product class

    This class only has one field to make it easier to iterate over the fields of the subclasses,
    as only the Descriptor here needs to be ignored to get all the child fields.
    """

    @staticmethod
    def create_from_dict(type: str, dict: dict[str, Any]) -> Self:
        """
        Create the product dynamically fron a dictionary of fields.

        Requires that it matches an existing product type.
        """
        product = Product.create(type, **dict)
        return product
