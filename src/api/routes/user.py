import logging
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import exc
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.user import User, UserSchema
from api.utils.db import db

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("", methods=["POST"])
def create_user():
    """
    Create a new user
    ---
    tags:
      - users
    # definitions:
    #   - schema:
    #       id: Group
    #       properties:
    #         name:
    #          type: string
    #          description: the group's name
    parameters:
      - in: body
        name: body
        description: "create user by supplying username and password"
        required: true
        schema:
          id: User
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: name for user
            password:
              type: string
              description: email for user
    responses:
      201:
        description: User created
    """
    try:
        data = request.get_json()
        data["password"] = User.generate_hash(data["password"])
        schema = UserSchema()
        user = schema.load(data, session=db.session)
        created_user = user.create()
        result_schema = UserSchema(exclude=["password"])
        result = result_schema.dump(created_user)
        return response_with(resp.SUCCESS_201, value={"user": result})
    except Exception as e:
        db.session.rollback()
        logging.error(str(e))
        return response_with(resp.INVALID_INPUT_422, None, None, error=str(e))


@user_routes.route("/login", methods=["POST"])
def authenticate_user():
    try:
        data = request.get_json()
        user = User.find_by_username(data["username"])
        if not user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data["password"], user.password):
            access_token = create_access_token(identity=data["username"])
            return response_with(
                resp.SUCCESS_200,
                value={
                    "message": f"Logged in as {user.username}",
                    "access_token": access_token,
                },
            )
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        logging.error(str(e))
        return response_with(resp.INVALID_INPUT_422)
