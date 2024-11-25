from dataclasses import dataclass
import dataclasses

from .db_item_descriptor import DbItemDescriptor
from ..models.products import Product


@dataclass(kw_only=True)
class DatabaseProduct:
    Product: Product
    Descriptor: DbItemDescriptor

    @classmethod
    def create_from_dict(
        cls, descriptor: DbItemDescriptor, dict: dict, extra_attributes: dict
    ):
        descriptor_fields = dataclasses.asdict(descriptor)
        fields_to_add = {
            key: value for key, value in dict.items() if key not in descriptor_fields
        }
        extra_attributes.update(fields_to_add)
        product = Product.create(descriptor.Type, **extra_attributes)

        db_product = cls(Product=product, Descriptor=descriptor)
        return db_product
