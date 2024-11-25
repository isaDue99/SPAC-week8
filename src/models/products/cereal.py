# cereal class for week 8 assignment

from dataclasses import dataclass
from .product import Product


@dataclass(kw_only=True)
class Cereal(Product):
    """A product of cereal"""
    Brand: str
    Shape: str
    NetWeight: int
    Ingredients: list[str]
    Nutrition: Nutrition


class Nutrition():
    """Nutritional info per 100 grams"""
    Calories: int
    Fat: float
    Carbs: float
    Protein: float
    Fiber: float
    Salt: float