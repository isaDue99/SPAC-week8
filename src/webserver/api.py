from typing import Any
from flask import Flask, Request, jsonify, request, Response
from ..models.products import Product
from ..db.adapters.product_adapter import ProductAdapter
from ..db.db_connection import DbConnection
from ..db.db_product import DatabaseProduct
from ..db import error as db_err

api = Flask(__name__)


def _validate_product_request_fields(
    product_data: dict[str, Any]
) -> tuple[Response, int] | None:
    """
    Validate that the request data has the minimum required fields.
    """

    required_fields = ["Type", "Product"]
    if not all(field in product_data for field in required_fields):
        return (
            jsonify(
                {
                    "error": f"Missing required fields. Required fields are: {required_fields}"
                }
            ),
            400,
        )


def _validate_product_request(request: Request) -> tuple[Response, int] | dict:
    # Ensure the request body is JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    json = request.get_json()
    product_data = json
    validate_error = _validate_product_request_fields(product_data)
    if validate_error:
        return validate_error

    return product_data


@api.route("/api/products", methods=["GET"])
def get_products() -> list[DatabaseProduct]:
    db = DbConnection()
    product_adapter = ProductAdapter(db)

    type_filter = request.args.get("type_filter", None)

    try:
        product_iter = product_adapter.get_all_products(type_filter)
    except db_err.DbError as err:
        return jsonify({"error": err.message}), 400
    # We need to return a list and not an iterator.
    return list(product_iter)


@api.route("/api/product/<int:id>", methods=["GET"])
def get_product(id: int):
    db = DbConnection()
    product_adapter = ProductAdapter(db)

    try:
        product = product_adapter.get_product(id)
    except db_err.DbError as err:
        return jsonify({"error": err.message}), 400

    return [product]


@api.route("/api/product", methods=["POST"])
def add_product():
    """
    Insert a product defined by the body of this request.
    """

    assert_result = _validate_product_request(request)
    if isinstance(assert_result, tuple):  # Is result an error response tuple?
        return assert_result

    db = DbConnection()
    product_adapter = ProductAdapter(db)

    type_str = assert_result["Type"]
    product_dict = assert_result["Product"]
    product = Product.create_from_dict(type_str, product_dict)

    try:
        product_adapter.insert_product(product)
        db.commit()
    except db_err.DbError as err:
        return jsonify({"error": err.message}), 400

    return "Success"


@api.route("/api/product/<int:id>", methods=["PUT"])
def set_product(id: int):
    """
    Replace a particular product by ID with the body of this request.
    """

    assert_result = _validate_product_request(request)
    if isinstance(assert_result, tuple):  # Is result an error response tuple?
        return assert_result

    db = DbConnection()
    product_adapter = ProductAdapter(db)

    type_str = assert_result["Type"]
    product_dict = assert_result["Product"]
    product = Product.create_from_dict(type_str, product_dict)

    try:
        product_adapter.update_product(id, product)
        db.commit()
    except db_err.DbError as err:
        return jsonify({"error": err.message}), 400

    return "Success"


@api.route("/api/product/<int:id>", methods=["DELETE"])
def delete_product(id: int):
    db = DbConnection()
    product_adapter = ProductAdapter(db)

    try:
        product_adapter.delete_product(id)
        db.commit()
    except db_err.DbError as err:
        return jsonify({"error": err.message}), 400

    return "Success"
