from flask import Blueprint, request
import logging
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.author import Author, AuthorSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.db import db

author_routes = Blueprint("author_routes", __name__)


@author_routes.route("")
@jwt_required()
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=["id", "first_name", "last_name"])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route("/<int:author_id>", methods=["GET"])
@jwt_required()
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_author_detail(id):
    data = request.get_json()
    author = Author.query.get_or_404(id)
    author.first_name = data["first_name"]
    author.last_name = data["last_name"]
    db.session.add(author)
    db.session.commit()
    author_schema = AuthorSchema()
    result = author_schema.dump(author)
    return response_with(resp.SUCCESS_200, value={"author": result})


@author_routes.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def modify_author_detail(id):
    data = request.get_json()
    author = Author.query.get_or_404(id)
    if data.get("first_name"):
        author.first_name = data["first_name"]
    if data.get("last_name"):
        author.last_name = data["last_name"]
    db.session.add(author)
    db.session.commit()
    author_schema = AuthorSchema()
    result = author_schema.dump(author)
    return response_with(resp.SUCCESS_200, value={"author": result})


@author_routes.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


@author_routes.route("", methods=["POST"])
@jwt_required()
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data, session=db.session)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        logging.error(e)
        return response_with(resp.INVALID_INPUT_422)
