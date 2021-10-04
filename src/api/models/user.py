from api.utils.db import db
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow.fields import Integer, String
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.username}"

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = Integer(dump_only=True)
    username = String(required=True)
    password = String(required=True)
