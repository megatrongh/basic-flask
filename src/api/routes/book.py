from flask import Blueprint, request
import logging

from marshmallow.utils import EXCLUDE
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.book import Book, BookSchema
from api.utils.db import db

book_routes = Blueprint("book_routes", __name__)


@book_routes.route("", methods=["POST"])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data, session=db.session)
        result = book_schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print(e)
        logging.error(e)
        return response_with(resp.INVALID_INPUT_422)


@book_routes.route("", methods=["GET"])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, exclude=["author_id"])
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route("/<int:id>")
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    book_schema = BookSchema(exclude=["author_id"])
    book = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:id>", methods=["PUT"])
def update_book_detail(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.title = data["title"]
    book.year = data["year"]
    db.session.add(book)
    db.session.commit()
    book_schema = BookSchema(exclude=["author_id"])
    updated_book = book_schema.dump(book)
    return response_with(resp.SUCCESS_200, value={"book": updated_book})


@book_routes.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
