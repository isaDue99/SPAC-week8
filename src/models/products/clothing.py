from dataclasses import dataclass
from .product import Product


@dataclass(kw_only=True)
class Clothing(Product):
    Material: str
    Size: str
    Color: str
