import dataclasses
from typing import Any, Iterable
import mysql.connector as sql
from ...models.products import Product
from ..db_connection import DbConnection, DbMySQLCursor
from ..db_item_descriptor import DbItemDescriptor
from ..db_product import DatabaseProduct
from ..error import IdNotPresentError

PRODUCT_TABLE_NAME = "products"
PRODUCT_ATTRIBUTE_TABLE_NAME = "product_attributes"


class ProductAdapter:
    """
    An "adapter" that goes on top of the databse so provide a better API for
    operations regarding products.
    """

    def __init__(self, db: DbConnection) -> None:
        self._db = db

    def _assert_id_exists(self, cursor: DbMySQLCursor, id: int):
        cursor.execute(f"SELECT * FROM `{PRODUCT_TABLE_NAME}` WHERE ID = %s", (id,))
        results = cursor.fetchall()
        if not results:
            raise IdNotPresentError()

    def insert_product(self, product: Product):
        """
        Inserts the product into the products table.
        """

        # Transform dataclass to dictionary of field name -> value.
        attributes = dataclasses.asdict(product)

        with self._db.get_cursor() as cur:
            # We first need to insert the product into the products table before the dynamic attributes.
            cur.execute(
                f"INSERT INTO `{PRODUCT_TABLE_NAME}` VALUES (DEFAULT, %s, %s, %s, %s, %s, DEFAULT, DEFAULT)",
                (
                    product.__class__.__name__,  # Use class name as the product type
                    attributes["Name"],
                    attributes["Description"],
                    attributes["Quantity"],
                    attributes["Price"],
                ),
            )

            # The base fields of the Product class.
            # Used to filter for the fields in subclasses.
            base_fields = [x.name for x in dataclasses.fields(Product)]

            # Then for each attribute, add an attribute row in the db.
            for name, value in attributes.items():
                # Skip the base fields from the Product class
                if name in base_fields:
                    continue

                cur.execute(
                    f"INSERT INTO `{PRODUCT_ATTRIBUTE_TABLE_NAME}` VALUES (LAST_INSERT_ID(), %s, %s)",
                    (name, value),
                )

    def update_product(self, id: int, product: Product):
        """
        Updates the product in the database.
        """

        # Transform dataclass to dictionary of field name -> value.
        attrs = dataclasses.asdict(product)

        with self._db.get_cursor() as cur:
            self._assert_id_exists(cur, id)

            # Update the manually set parts of the products table
            cur.execute(
                f"""
                UPDATE `{PRODUCT_TABLE_NAME}`
                SET
                    Name = %s,
                    Description = %s,
                    Quantity = %s,
                    Price = %s
                WHERE
                    ID = %s;
                """,
                (
                    attrs["Name"],
                    attrs["Description"],
                    attrs["Quantity"],
                    attrs["Price"],
                    id,
                ),
            )

            # Now set the other attribute values (if they exist for the product)
            for name, value in attrs.items():

                cur.execute(
                    f"""
                    UPDATE `{PRODUCT_ATTRIBUTE_TABLE_NAME}`
                    SET
                        AttributeValue = %s
                    WHERE
                        ProductID = %s AND
                        AttributeName = %s
                    """,
                    (value, id, name),
                )

    def _get_extra_attributes(
        self, cursor: sql.connection.MySQLCursor, product_id: int
    ) -> dict[str, Any]:
        """
        Get all attribute rows associated the the product id.
        """

        cursor.execute(
            f"SELECT * FROM `{PRODUCT_ATTRIBUTE_TABLE_NAME}` WHERE ProductID = %s",
            (product_id,),
        )
        attributes = cursor.fetchall()

        # Transform the attribute rows to dictionary of attribute_name -> attribute_value
        attributeDict = {}
        for attr in attributes:
            name = attr["AttributeName"]
            value = attr["AttributeValue"]
            attributeDict[name] = value

        return attributeDict

    def get_all_products(self, type: str | None) -> Iterable[DatabaseProduct]:
        """
        Get all the matching products from the database.

        New products are created with data from the products table,
        and additional attributes from product_attributes.
        """

        # Important to get the cursor as a dictionary cursor.
        # otherwise we can't get values by column name.
        with self._db.get_cursor(dictionary=True) as cur:

            # Determine whether we need to filter or not.
            if type is None:
                cur.execute(f"SELECT * FROM `{PRODUCT_TABLE_NAME}`")
            else:
                cur.execute(
                    f"SELECT * FROM `{PRODUCT_TABLE_NAME}` WHERE Type = %s", (type,)
                )

            # Get our products
            products = cur.fetchall()
            for row in products:
                descriptor = DbItemDescriptor.create_from_dict(row)
                attributes = self._get_extra_attributes(cur, descriptor.ID)
                db_product = DatabaseProduct.create_from_dict(
                    descriptor, row, attributes
                )
                yield db_product

    def get_product(self, id: int) -> DatabaseProduct:
        # Important to get the cursor as a dictionary cursor.
        # otherwise we can't get values by column name.
        with self._db.get_cursor(dictionary=True) as cur:
            self._assert_id_exists(cur, id)

            cur.execute(f"SELECT * FROM `{PRODUCT_TABLE_NAME}` WHERE ID = %s", (id,))

            product_row = cur.fetchone()

            descriptor = DbItemDescriptor.create_from_dict(product_row)
            attributes = self._get_extra_attributes(cur, descriptor.ID)
            db_product = DatabaseProduct.create_from_dict(
                descriptor, product_row, attributes
            )

            return db_product

    def delete_product(self, id: int):
        with self._db.get_cursor() as cur:
            self._assert_id_exists(cur, id)

            cur.execute(
                f"DELETE FROM `{PRODUCT_ATTRIBUTE_TABLE_NAME}` WHERE ProductID = %s",
                (id,),
            )
            cur.execute(f"DELETE FROM `{PRODUCT_TABLE_NAME}` WHERE ID = %s", (id,))
