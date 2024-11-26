# cereal class for week 8 assignment

from dataclasses import dataclass
from .product import Product


@dataclass(kw_only=True)
class Nutrition:
    """Nutritional info per 100 grams"""
    Calories: int
    Fat: float
    Carbs: float
    Protein: float
    Fiber: float
    Salt: float

@dataclass(kw_only=True)
class Cereal(Product):
    """A product of cereal"""
    NetWeight: int
    Ingredients: list[str]
    # This one was too much.
    # Nutrition: Nutrition
    Calories: int
    Fat: float
    Carbs: float
    Protein: float
    Fiber: float
    Salt: float