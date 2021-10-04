from sqlalchemy.orm import backref
from api.models.book import BookSchema
from api.utils.db import db
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow.fields import Integer, String, Nested


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', back_populates="author",
                            cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, books=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AuthorSchema(SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True

    id = Integer(dump_only=True)
    first_name = String(required=True)
    last_name = String(required=True)
    created = String(dump_only=True)
    books = Nested(BookSchema, many=True, only=['id', 'title', 'year'])
