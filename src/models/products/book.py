from dataclasses import dataclass
from .product import Product


@dataclass(kw_only=True)
class Book(Product):
    Genre: str
    PageCount: int
