import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
import logging
from flask_jwt_extended import JWTManager
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from api.utils.db import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.author import author_routes
from api.routes.book import book_routes
from api.routes.user import user_routes


def create_app(config):
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(config)
    conf_from_env = {**os.environ}
    app.config.update(conf_from_env)
    CORS(app)
    JWTManager(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    logging.basicConfig(
        stream=sys.stdout,
        datefmt="%Y-%m-%d %I:%M:%S %p",
        format="%(asctime)s | %(levelname)s | %(filename)s : %(lineno)s | %(message)s",
        level=logging.DEBUG,
    )

    @app.route("/")
    def home():
        return jsonify({"app_name": "Flask Author DB", "version": "1.0"})

    @app.route("/api/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["base"] = "http://localhost:5000"
        swag["info"]["version"] = "1.0"
        swag["info"]["title"] = "Flask Author DB"
        return jsonify(swag)

    swaggerui_blueprint = get_swaggerui_blueprint(
        # "/api/docs", "/static/swagger.json", config={"app_name": "Flask Author DB"}
        "/api/docs",
        "/api/spec",
        config={"app_name": "Flask Author DB"},
    )
    app.register_blueprint(author_routes, url_prefix="/api/v1/authors")
    app.register_blueprint(book_routes, url_prefix="/api/v1/books")
    app.register_blueprint(user_routes, url_prefix="/api/v1/users")
    app.register_blueprint(swaggerui_blueprint)

    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    return app
